from stone_pygame_ia_support import *
import pygame

pygame.init()
font = pygame.font.SysFont('arial', 25)

class MazeChallenge:

    def __init__(self, w=870, h=670):
        # init display
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Stone Automata Maze Challenge')
        self.clock = pygame.time.Clock()
        self.reset()
        self._update_ui()

    
    def reset(self):
        # init game state
        self.players = []
        self.players_temp = []
        self.players.append(Player(player_position=(START_POSITION[0], START_POSITION[1]), movements_list=[], square=START)) #Inicia um jogador
        self.frame_iteration = 0
        self.maze = load_maze()
        self.maze_with_players = load_maze()
        self.update_maze_with_players()

    
    def update_maze_with_players(self, position=None):
        """
        Takes a player position and insert the player into the maze with players. If no given position,
        it will update the maze with players with all available players.
        """
        if position == None:
            for player in self.players:
                if player.player_position != None:
                    player_in_maze = position_to_index(player.player_position, maze_columns(self.maze))
                    self.maze_with_players = self.maze_with_players[:int(player_in_maze)] + PLAYER + self.maze_with_players[int(player_in_maze)+1:]
        
        else:
            player_in_maze = position_to_index(position, maze_columns(self.maze))
            self.maze_with_players = self.maze_with_players[:int(player_in_maze)] + PLAYER + self.maze_with_players[int(player_in_maze)+1:]
        


    def play_maze(self):
        """
        Updates the main maze and the maze_with_players to the next maze. This last maze comes with
        no players on it. Also updates the frame_iteraction counter.
        """
        self.change_maze() #change main maze
        self.maze_with_players = self.maze[:] #limpo e mudo a maze with players
        self.frame_iteration += 1


    def play_step(self, player):
        """
        Gets a players and make all possible moves. If no legal move available, it's marked to be removed
        from the game. If more than one way is available, the player will be cloned to these ways and the actual
        player is marked to be deleted.
        """
        
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            pygame.event.clear()
        
        # 2. move
        # Play in all legal available directions.
        legal_directions = self.get_legal_directions(player.player_position)
        if len(legal_directions) > 1:
            for direction in legal_directions:
                new_player = Player()
                pos, pos_list, square = player.get_player_info()
                new_player.player_position = (pos[0], pos[1])
                new_player.movements_list = pos_list[:]
                new_player.square = square
                
                # Making the available legal movement
                new_player.movements_list.append(direction.upper())
                new_player.player_position = self.get_position_in_direction(new_player.player_position, direction)
                
                # Takes the square after the movement
                square_pos = position_to_index(new_player.player_position, maze_columns(self.maze))
                new_player.square = self.maze_with_players[square_pos]

                # Add player to the maze_with_players
                self.players_temp.append(new_player)
                
            # Mark the player to be deleted
            player.remove_player = True
            player.position = None

        elif len(legal_directions) == 1:
            direction = legal_directions[0]

            # Making the available legal movement
            player.movements_list.append(direction.upper())
            player.player_position = self.get_position_in_direction(player.player_position, direction)
            
            # Takes the square after the movement
            square_pos = position_to_index(player.player_position, maze_columns(self.maze))
            player.square = self.maze_with_players[square_pos]
            
        else:
            # If no legal movements available, remove player position and marks it to be deleted
            player.remove_player = True
            player.position = None



    def get_legal_directions(self, position):
        """
        takes a maze string and a position, and returns a list of
        legal directions for that square.
        """
        maze = self.maze_with_players[:]
        moves=[]
        for c in DIRECTIONS:
            square = self.move(maze,position,c)
            if square != WALL and square != BAD_POSITION and square != PLAYER:
                moves.append(c)
        return moves
    

    def move(self, maze, position, direction):
        """
        takes a maze string, a position of a square and a direction and
        returns the resulting square after the move.
        """

        T1 = maze_columns(self.maze)
        T2 = self.get_position_in_direction(position, direction)
        T3 = position_to_index(T2, T1)

        square = maze[T3]

        return square


    def get_position_in_direction(self, position, direction):

        """
        Takes a row, column pair representing a position, and a direction character (one of w, a, s, d), and returns the position of the adjacent square
        in the given direction. It does not matter whether or not the direction is legal.

        get_position_in_direction((tuple,tuple),str) -> (tuple,tuple)
        """

        delta = DIRECTION_DELTAS[direction]
        new_position = (position[0]+delta[0],position[1]+delta[1])

        return new_position


    def change_maze(self):
        """
        Get the game maze and changes it to the next maze according to the rules bellow.
        '0' cells turn '1' if they have a number of adjacent '1' cells greater than 1 and less than 5. Otherwise,
         they remain '0'.

        '1' cells remain '1' if they have a number of '1' adjacent cells greater than 3 and less than 6. Otherwise,
         they become '0'.
        """

        # Set height and weight
        height = maze_rows(self.maze) #67
        width = maze_columns(self.maze) #87

        # Convert to list
        maze = self.maze[:]
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

        self.maze = maze_cp
    

    def check(self):
        # Insert players_temp to players and clean it
        for player in self.players_temp:
            self.players.append(player)
        self.players_temp = []

        # Remove marked players and those in wrong square. Return True if won game.
        self.players_temp = self.players
        self.players = []
        added_player_pos = []

        for player in self.players_temp:
            if not player.remove_player:
                if player.square != WALL and player.square not in BAD_POSITION and player.square != PLAYER and player.player_position not in added_player_pos:
                    self.players.append(player)
                    added_player_pos.append(player.player_position)
                if player.square == GOOD_POSITION:
                    print(WIN_TEXT)
                    print(player.movements_list)
                    return True
        self.players_temp.clear()
        added_player_pos.clear()
        return False
    

    def _update_ui(self):
        """
        Updates graphs according to the character in the maze_with_players
        """
        self.display.fill(WHITE)

        maze = self.maze_with_players[:]
        screen_x, screen_y = 0, 0
        screen_position = (screen_x, screen_y)
        for char in maze:
            if char == PLAYER:
                pygame.draw.rect(self.display, RED, ((screen_position),BLOCK_SIZE))
                screen_x += BLOCK_SIZE[0]

            elif char == OPEN:
                pygame.draw.rect(self.display, WHITE, ((screen_position),BLOCK_SIZE))
                screen_x += BLOCK_SIZE[0]

            elif char == START or char == END:
                pygame.draw.rect(self.display, YELLOW, ((screen_position),BLOCK_SIZE))
                screen_x += BLOCK_SIZE[0]

            elif char in BAD_POSITION:
                pygame.draw.rect(self.display, GREEN, ((screen_position),BLOCK_SIZE))
                screen_x += BLOCK_SIZE[0]
            
            elif char == WALL:
                pygame.draw.rect(self.display, BLACK, ((screen_position),BLOCK_SIZE))
                screen_x += BLOCK_SIZE[0]

            else:
                screen_x = 0
                screen_y += BLOCK_SIZE[1]

            screen_position = (screen_x, screen_y)
        
        pygame.display.flip()


class Player(MazeChallenge):
    def __init__(self, player_position=None, movements_list=[], square=None):
        # init player state
        self.player_position = player_position
        self.movements_list = movements_list
        self.square = square
        self.remove_player = False
    
    def get_player_info(self):
        # get player's info to clone
        return self.player_position, self.movements_list[:], self.square
    

if __name__ == "__main__":
    game = MazeChallenge(w=87*BLOCK_SIZE[0], h=67*BLOCK_SIZE[1])
    game_over = False
    # game loop
    while True:
        game.play_maze()
        for player in game.players:
            game.play_step(player)
        game_over = game.check() #limpar os remove_player e duplicados
        game.update_maze_with_players() #Atualizar a maze com jogadores
        game._update_ui()
        
        if game_over:
            break
        print('Iteraction:', game.frame_iteration, 'Players:', len(game.players))

    pygame.quit()