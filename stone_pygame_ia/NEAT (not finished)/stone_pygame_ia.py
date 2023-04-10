from stone_pygame_ia_support import *
import pygame
import time
import neat

# Ajustes para IA jogando
#STAT_FONT = pygame.font.SysFont("comicsans", 50)
STAT_FONT = pygame.font.SysFont('arial', 25)
AI_JOGANDO = True
GEN = 0
SCORE = 0

# Pygame init
pygame.display.set_caption('Stone Automata Maze Challenge')
pygame.init()

# Window size
window_x = 87 * BLOCK_SIZE[0]
window_y = 67 * BLOCK_SIZE[1]
screen = pygame.display.set_mode((window_x,window_y))

clock = pygame.time.Clock()
screen.fill("white")

# Movements control
movements_history = [] #Ainda não usando as informações de movimento

def main(genomas, config):
    global GEN
    GEN += 1
    genoma = genomas[1]

    if AI_JOGANDO:
        rede = neat.nn.FeedForwardNetwork.create(genoma, config)
        genoma.fitness = 0

    # Clear possible previous commands
    pygame.event.clear()

    #Controle para a função restart
    lost_game = False

    # Player initial
    player_position = START_POSITION
    movements_count = 0
    movements_list = []

    # Initial maze display
    maze = load_maze(INITIAL_MAZE)
    display_maze(screen, SCORE, GEN, maze, player_position)

    while True:
        # Process player inputs.
        command = ''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            
            if not AI_JOGANDO:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        command = 'w'

                    elif event.key == pygame.K_a:
                        command = 'a'

                    elif event.key == pygame.K_s:
                        command = 's'

                    elif event.key == pygame.K_d:
                        command = 'd'

                    elif event.key == pygame.K_p:
                        show_legal_direction(get_legal_directions(change_maze(maze),player_position))
                        
                    elif event.key == pygame.K_r:
                        restart_game(lost_game, movements_list)

                    elif event.key == pygame.K_q:
                        quit_game(maze, player_position)

                    elif event.key == pygame.K_h or event.key == pygame.K_SLASH or event.key == pygame.K_QUESTION:
                        help_game()

        # Do logical updates here.
        if command != '':
            if command in DIRECTIONS: #Testing if the comand is a direction
                maze_bk = maze
                player_position_bk = player_position
                maze = change_maze(maze)
                player_position, square = move(maze, player_position, command)

                if square == WALL:
                    genoma.fitness -= 1
                    maze = maze_bk
                    player_position = player_position_bk

                elif square not in GOOD_POSITION + BAD_POSITION:
                    danger_up = 0 if 'w' in get_legal_directions(maze, player_position) else 1
                    danger_down = 0 if 's' in get_legal_directions(maze, player_position) else 1
                    danger_left = 0 if 'a' in get_legal_directions(maze, player_position) else 1
                    danger_right = 0 if 'd' in get_legal_directions(maze, player_position) else 1
                    dist_x_to_end = abs(player_position[0] - 87)
                    dist_y_to_end = abs(player_position[1] - 67)

                    movements_count += 1
                    genoma.fitness += 1
                    output = rede.activate((danger_up,
                                            danger_down,
                                            danger_left,
                                            danger_right,
                                            dist_x_to_end,
                                            dist_y_to_end))
                    # -1 e 1-> se output < -0.5 left, de 0 a -0.5 down de 0 a 0.5 right, de 0.5 a 1 up
                    #if output[0] PAREI AQUI. Ficou esquisito.
                    movements_list.append(command.upper())
                    maze = change_maze(maze)

                if square in GOOD_POSITION:
                    movements_count += 1
                    genoma.fitness += 100
                    movements_list.append(command.upper())
                    print(WIN_TEXT)
                    print(movements_list)
                    maze = change_maze(maze)
                    break

                if square in BAD_POSITION:
                    movements_count += 1
                    genoma.fitness -= 10
                    movements_list.append(command.upper())
                    maze = change_maze(maze)
                    lost_game = True
                    #restart_game(lost_game, movements_list) #recomeçar
                    break

                display_maze(screen, SCORE, GEN, maze, player_position)

            command = ''

        # Render the graphics here.
        # ...

        pygame.display.flip()  # Refresh on-screen display
        clock.tick(1000)         # wait until next frame (at 60 FPS)

    return 0

def display_maze(win, score, gen, maze, player_position):
    """
    takes a maze string and the position of the player, and prints the
    maze with the player shown as an red cricle.
    """

    player_in_maze = position_to_index(player_position, maze_columns(maze))
    maze = maze[:int(player_in_maze)] + PLAYER + maze[int(player_in_maze)+1:]

    screen_x, screen_y = 0, 0
    screen_position = (screen_x, screen_y)
    for char in maze:
        if char == PLAYER:
            pygame.draw.rect(screen, 'red', ((screen_position),BLOCK_SIZE))
            screen_x += BLOCK_SIZE[0]

        elif char == OPEN:
            pygame.draw.rect(screen, 'white', ((screen_position),BLOCK_SIZE))
            screen_x += BLOCK_SIZE[0]

        elif char == START or char == END:
            pygame.draw.rect(screen, 'yellow', ((screen_position),BLOCK_SIZE))
            screen_x += BLOCK_SIZE[0]

        elif char == BAD_POSITION:
            pygame.draw.rect(screen, 'green', ((screen_position),BLOCK_SIZE))
            screen_x += BLOCK_SIZE[0]
        
        elif char == WALL:
            pygame.draw.rect(screen, 'black', ((screen_position),BLOCK_SIZE))
            screen_x += BLOCK_SIZE[0]

        else:
            screen_x = 0
            screen_y += BLOCK_SIZE[1]

        screen_position = (screen_x, screen_y)
    
    if AI_JOGANDO:
        # score
        score_label = STAT_FONT.render("Score: " + str(score),1,(255,255,255))
        win.blit(score_label, (window_x - score_label.get_width() - 15, 10))

        # generations
        gen_label = STAT_FONT.render("Gens: " + str(gen-1),1,(255,255,255))
        win.blit(gen_label, (10, 10))


    return


def change_maze(maze):
    # Regra do movimento
    # '0' cells turn '1' if they have a number of adjacent '1' cells greater than 1 and less than 5. Otherwise,
    #  they remain '0'.

    # '1' cells remain '1' if they have a number of '1' adjacent cells greater than 3 and less than 6. Otherwise,
    #  they become '0'.

    # Set height and weight
    height = maze_rows(maze) #67
    width = maze_columns(maze) #87

    # Convert to list
    maze = maze.split('\n')
    maze_cp = []

    for row in range(height):
        tmp = ''
        for col in range(width):
            if maze[row][col] == '0':
                count_1 = 0
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if (row + i < 0 or row + i >= height or col + j < 0 or col + j >= width or (i == 0 and j == 0)):
                            continue
                        else:
                            if maze[row + i][col + j] == '1':
                                count_1 += 1
                if count_1 > 1 and count_1 < 5:
                    tmp += '1'
                else:
                    tmp += '0'

            elif maze[row][col] == '1':
                count_1 = 0
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if (row + i < 0 or row + i >= height or col + j < 0 or col + j >= width or (i == 0 and j == 0)):
                            continue
                        else:
                            if maze[row + i][col + j] == '1':
                                count_1 += 1
                if count_1 > 3 and count_1 < 6:
                    tmp += '1'
                else:
                    tmp += '0'

            else:
                tmp += maze[row][col]
        tmp += '\n'
        maze_cp.append(tmp)

    #maze_cp list to maze_cp str
    maze_cp = ''.join(maze_cp)

    #clear the last \n
    maze_cp = maze_cp[:-1]

    return maze_cp


def get_position_in_direction(position,direction):

    """
    Takes a row, column pair representing a position, and a direction character (one of w, a, s, d), and returns the position of the adjacent square
in the given direction. It does not matter whether or not the direction is legal.

    get_position_in_direction((tuple,tuple),str) -> (tuple,tuple)
    """

    delta = DIRECTION_DELTAS[direction]
    new_position = (position[0]+delta[0],position[1]+delta[1])

    return new_position



def move(maze, position, direction):
    """
    takes a maze string, a position of a square and a direction and
    returns a pair of the form (position, square) where position is
    the position after the move and square is the resulting square
    after the move. When the move is invalid, the new position returned
    is the same as the old position.
    """

    T1=maze_columns(maze)
    T2=get_position_in_direction(position, direction)
    T3=position_to_index(T2,T1)

    square=maze[T3]
    
    if square == WALL:
        return position, square
    else:
        return get_position_in_direction(position,direction), square


def get_legal_directions(maze, position):
    """
    takes a maze string and a position, and returns a list of
    legal directions for that square.
    """
    moves=[]
    for c in DIRECTIONS:
        #if move(maze,position,c)[1] not in WALL:
        if move(maze,position,c)[1] not in WALL and move(maze,position,c)[1] != '1':
            moves.append(c)
    return moves


# displaying legal direction
def show_legal_direction(moves):

    # creating font object score_font
    legal_font = pygame.font.SysFont('times new roman', 20)
    
    # create the display surface object
    # legal_surface
    legal_surface = legal_font.render('Moves : ' + str(moves), True, 'purple')
    
    # create a rectangular object for the text
    # surface object
    legal_rect = legal_surface.get_rect()
    
    # setting position of the text
    legal_rect.topleft = (12,10)
        
    # displaying text
    screen.blit(legal_surface, legal_rect)

def restart_game(lost_game, match_movements):

    # creating font object my_font
    my_font = pygame.font.SysFont('times new roman', 50)
    
    # creating a text surface on which text
    # will be drawn
    restart_game_surface = my_font.render(
        'Restarting the game...', True, 'red')
    
    # create a rectangular object for the text
    # surface object
    restart_game_rect = restart_game_surface.get_rect()
    
    # setting position of the text
    restart_game_rect.midtop = (window_x/2, window_y/4)
    
    # blit will draw the text on screen
    screen.blit(restart_game_surface, restart_game_rect)

    if lost_game:
        restart_lost_game_surface = my_font.render(
            f'{LOSE_TEXT}', True, 'red')
        restart_lost_game_rect = restart_lost_game_surface.get_rect()
        restart_lost_game_rect.midtop = (window_x/2, window_y/4 - 50)
        screen.blit(restart_lost_game_surface, restart_lost_game_rect)

    pygame.display.flip()
    
    # after 2 seconds we will restart the game
    time.sleep(1)
    
    # Movements settings
    global movements_history
    movements_history.append(match_movements)

    # restart game through main function
    main()


def quit_game(maze, player_position):

    # creating font object my_font
    my_font = pygame.font.SysFont('times new roman', 50)
    
    # creating a text surface on which text
    # will be drawn
    quit_game_surface_1 = my_font.render(
        'You will quit the game and the', True, 'red')
    quit_game_surface_2 = my_font.render(
        'current game will be lost.', True, 'red')
    quit_game_surface_3 = my_font.render(
        'Are you sure you want to quit?', True, 'red')
    quit_game_surface_4 = my_font.render(
        '[y] or n', True, 'red')
    
    # create a rectangular object for the text
    # surface object
    quit_game_rect_1 = quit_game_surface_1.get_rect()
    quit_game_rect_2 = quit_game_surface_2.get_rect()
    quit_game_rect_3 = quit_game_surface_3.get_rect()
    quit_game_rect_4 = quit_game_surface_4.get_rect()
    
    # setting position of the text
    quit_game_rect_1.midtop = (window_x/2, window_y/4 - 50)
    quit_game_rect_2.midtop = (window_x/2, window_y/4)
    quit_game_rect_3.midtop = (window_x/2, window_y/4 + 80)
    quit_game_rect_4.midtop = (window_x/2, window_y/4 + 80 + 50)
    
    # blit will draw the text on screen
    screen.blit(quit_game_surface_1, quit_game_rect_1)
    screen.blit(quit_game_surface_2, quit_game_rect_2)
    screen.blit(quit_game_surface_3, quit_game_rect_3)
    screen.blit(quit_game_surface_4, quit_game_rect_4)

    pygame.display.flip()    

    # exit game through main function
    while True:
        # Process player inputs.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    pygame.quit()
                    raise SystemExit
                else:
                    # Refresh screen and return
                    display_maze(screen, SCORE, GEN, maze, player_position)
                    return
        
def help_game():
    #print(HELP_TEXT)
    # creating font object score_font
    legal_font = pygame.font.SysFont('times new roman', 20)
    
    sentences = HELP_TEXT.split('\n')
    
    # Respecting the space for the legal movements.
    next_line = 30
    
    for sentence in sentences:
        # create the display surface object legal_surface
        legal_surface = legal_font.render(str(sentence), True, 'purple')
    
        # create a rectangular object for the text surface object
        legal_rect = legal_surface.get_rect()
        
        # setting position of the text
        legal_rect.topleft = (12,10 + next_line)
        
        # displaying text
        screen.blit(legal_surface, legal_rect)
        next_line += 30


if __name__ == "__main__":
    main()