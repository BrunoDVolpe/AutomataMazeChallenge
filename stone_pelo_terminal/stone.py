from stone_support import *
import sys, csv, random, datetime
import traceback

# Global Constants
#sys.setrecursionlimit(10**6) #if more recursion necessary.

# Desireable plays. It was used to test the final answer.
"""
JOGADAS_DESEJADAS = ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D',
                      'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'A', 'S', 'W', 'W', 'D', 'S', 'D', 'S', 'D',
                      'S', 'D', 'S', 'S', 'S', 'D', 'S', 'D', 'D', 'S', 'S', 'S', 'D', 'D', 'S', 'A', 'D', 
                      'D', 'D', 'S', 'W', 'W', 'D', 'S', 'W', 'S', 'W', 'D', 'D', 'S', 'D', 'S', 'D', 'W', 
                      'W', 'S', 'S', 'A', 'S', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'S', 'S', 'D', 
                      'D', 'D', 'S', 'S', 'S', 'W', 'D', 'S', 'S', 'A', 'A', 'A', 'S', 'D', 'S', 'D', 'S', 
                      'S', 'D', 'A', 'S', 'A', 'S', 'D', 'A', 'A', 'D', 'S', 'D', 'A', 'D', 'W', 'D', 'A', 
                      'D', 'S', 'S', 'D', 'S', 'S', 'A', 'D', 'D', 'S', 'D', 'S', 'D', 'D', 'D', 'D', 'D', 
                      'W', 'S', 'S', 'D', 'S', 'W', 'W', 'W', 'D', 'S', 'S', 'S', 'D', 'W', 'W', 'S', 'D', 
                      'S', 'D', 'S', 'S', 'S', 'W', 'D', 'S', 'D', 'D', 'D', 'D', 'D', 'D', 'A', 'D', 'D', 
                      'W', 'D', 'D', 'D', 'D', 'A', 'D', 'D', 'D', 'D', 'W', 'S', 'A', 'W', 'W', 'W', 'S', 
                      'S', 'A', 'D', 'S', 'A', 'D', 'W', 'S', 'D', 'D', 'D', 'A', 'D', 'S', 'S', 'S', 'D', 
                      'A', 'D', 'S', 'S', 'S', 'S', 'S', 'A', 'S', 'S', 'W', 'D', 'D', 'S', 'D', 'W', 'D', 
                      'W', 'S', 'D', 'W', 'S', 'S', 'S', 'D', 'W', 'D', 'S', 'S', 'W', 'D', 'W', 'S', 'D', 
                      'A', 'S', 'D', 'A', 'W', 'A', 'D', 'S', 'S', 'S', 'S', 'S', 'S', 'D', 'A', 'S', 'D', 
                      'W', 'D', 'W', 'S', 'S', 'A', 'A', 'A', 'D', 'S', 'S', 'S', 'S', 'W', 'S', 'D', 'D']
JOGADAS_INICIAIS = [x.lower() for x in JOGADAS_DESEJADAS]
"""
JOGADAS_INICIAIS = []

def get_position_in_direction(position,direction):

    """
    Takes a row, column pair representing a position, and a direction character (one of w, a, s, d), and returns the position of the adjacent square
in the given direction. It does not matter whether or not the direction is legal.

    get_position_in_direction((tuple,tuple),str) -> (tuple,tuple)
    """

    delta = DIRECTION_DELTAS[direction]
    newposition = (position[0]+delta[0],position[1]+delta[1])

    return newposition


def print_maze(maze,position):

    """
    takes a maze string and the position of the player, and prints the
    maze with the player shown as an 'A'.
    """

    A_in_maze = position_to_index(position,maze_columns(maze))
    maze=maze[:int(A_in_maze)]+PLAYER+maze[int(A_in_maze)+1:]

    return print(maze)


def print_hint(maze, position):
    """
    takes a maze string and the position of the player, and prints 1 line before and 1 line after the player position
    """
    width = maze_columns(maze)
    n_maze = change_maze(maze)

    A_in_maze = position_to_index(position,maze_columns(n_maze))
    menor = int(A_in_maze) - width * 2 - 1
    maior = int(A_in_maze) + width * 2
    if menor < 0:
        menor = 0
    if maior > 5588:
        maior = 5588
    return print(n_maze[menor:int(A_in_maze)]+'*'+n_maze[int(A_in_maze + 1):maior])


def move(maze,position,direction):
    """
    takes a maze string, a position of a square and a direction and
    returns a pair of the form (position, square) where position is
    the position after the move and square is the resulting square
    after the move. When the move is invalid, the new position returned
    is the same as the old position.
    """

    T1=maze_columns(maze)
    T2=get_position_in_direction(position,direction)
    T3=position_to_index(T2,T1)

    square=maze[T3]
    
    if square == WALL:
        return position,square
    else:
        return get_position_in_direction(position,direction),square


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


def save_steps_win(plays):
    with open('win_steps.txt', 'w') as file:
        for move in plays:
             file.write(f"{move} ")


def save_steps(plays):
    with open('steps_memory.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(plays)


def load_memory(file):
    memory = []
    try:
        with open(file, 'r') as f:
            for row in f:
                row = row[:-1].lower() #avoids \n
                memory.append(row.split(','))
    except FileNotFoundError:
        sys.exit('Memory file not found.')

    return memory


def auto_play(maze, position):
    #return random.choice(DIRECTIONS)
    if get_legal_directions(change_maze(maze),position):
        return get_legal_directions(change_maze(maze),position)[random.randint(0, len(get_legal_directions(change_maze(maze),position))) - 1]
    return DIRECTIONS[random.randint(0,3)]


def interact():
    position=START_POSITION
    #print("")
    #print(datetime.datetime.now())
    maze=load_maze(INITIAL_MAZE)
    steps_memory = load_memory(MEMORY)
    plays=[]
    b=1
    jogadas_iniciais = JOGADAS_INICIAIS
    while True:
        print("")
        print_maze(maze,position) #fazer na forma correta
        #print_maze(change_maze(maze),position) #printar a maze 'seguinte' para facilitar
        print("")
        #print_hint(maze, position) #printar uma dica de como ficará o próximo movimento
        #print("")
        #command=str(input("Command: ")).strip() #avoid white spaces
        #command = auto_play(maze, position)

        #"""
        if jogadas_iniciais:
            jogada = jogadas_iniciais[0]
            jogadas_iniciais = jogadas_iniciais[1:]
            command = jogada
        else:
            #command = auto_play(maze, position)
            command=str(input("Command: ")).strip() #avoid white spaces
        #"""
        
        # Se já existir a jogada, pula ela.
        # E se só tiver essa opção? Acho que corrigi.
        if plays + list(command) in steps_memory and len(get_legal_directions(change_maze(maze),position)) > 1:
            print("Já existe!")
            print(plays + list(command))
            print('Compr legal directions:', len(get_legal_directions(change_maze(maze),position)))
            continue
        #if command == '':
        #    continue

        # Se tiver posições recomendadas e o comando não for uma delas, tenta outra posição
        #elif get_legal_directions(change_maze(maze),position) and command not in get_legal_directions(change_maze(maze),position):
        #    print('posições recomendadas e comando diferente dela')
        #    print('Lista:', get_legal_directions(change_maze(maze),position))
        #    print('Comando:', command)
        #    continue

        elif command in DIRECTIONS: #Testing if the comand is a direction
            maze_bk = maze
            position_bk = position
            maze = change_maze(maze)
            position,square = move(maze,position,command)

            if square == WALL:
                print("You can't go in that direction.")
                maze = maze_bk
                position = position_bk

            elif square not in GOOD_POSITION+BAD_POSITION:
                plays.append(command.upper())
                b += 1

            if square in GOOD_POSITION:
                plays.append(command.upper())
                print(WIN_TEXT)
                print("")
                #print(f"Moves: {b}")
                #print(plays)
                save_steps_win(plays)
                x=input("Press Enter to exit...")
                break

            if square in BAD_POSITION:
                plays.append(command.upper())
                #print(LOSE_TEXT)
                #print("")
                #print(f"Moves: {b}")
                #print(plays)
                save_steps(plays)
                x=input("Press Enter to restart or 'q' followed by Enter to quit... ")
                if x == 'q': break
                interact() #recomeçar

        elif command == "q": #Exiting the program
            exit_game=str(input("Are you sure you want to quit? [n] to cancel: "))
            if exit_game not in ("nN"): #confirm the break in case of 'y'comand
                print("")
                break
                #return
                #sys.exit()

        elif command == "?":
            print(HELP_TEXT)

        elif command == "p":
            print("Possible positions:",', '.join(get_legal_directions(change_maze(maze),position)))

        elif command == "r":
            interact()

        if command not in str(DIRECTIONS) + "p?qr":
            print("Invalid command:",command)
    
    
    return None


if __name__ == '__main__':
    interact()
    exit()
