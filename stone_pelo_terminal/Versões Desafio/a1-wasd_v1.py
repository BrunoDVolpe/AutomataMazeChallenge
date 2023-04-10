from a1_support1 import *

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
    n_maze = change_maze(maze)
    A_in_maze = position_to_index(position,maze_columns(n_maze))
    menor = int(A_in_maze) - 86 * 2
    maior = int(A_in_maze) + 86 * 2 - 1
    if menor < 0:
        menor = 0
    if maior > 5588:
        maior = 5588
    #print(n_maze[menor:int(A_in_maze)]+'*'+n_maze[int(A_in_maze + 1):maior])
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
        if move(maze,position,c)[1] not in WALL:
            moves.append(c)
    return moves

def interact():
    position=START_POSITION
    print("")
    maze=load_maze(FILE)
    plays=[START_POSITION]
    b=1
    while True:
        print("")
        print_maze(maze,position)
        print("")
        print_hint(maze, position)
        print("")
        command=str(input("Command: ")).strip() #avoid white spaces
        if command == '':
            continue

        elif command in DIRECTIONS: #Testing if the comand is a direction
            maze = change_maze(maze)
            position,square = move(maze,position,command)

            if square == "1" or square == None or square == '\n':
                print("You can't go in that direction.")

            elif square not in GOOD_POSITION+BAD_POSITION:
                plays.append(position)
                b += 1

            if square in GOOD_POSITION:
                print(WIN_TEXT)
                print("")
                x=input("Press Enter to exit...")
                break

            if square in BAD_POSITION:
                print(LOSE_TEXT)
                print("")
                x=input("Press Enter to exit...")
                break

        elif command == "q": #Exiting the program
            exit_game=str(input("Are you sure you want to quit? [y] or n: "))
            """
            while exit_game not in 'y' or 'n':
                exit_game=input("Are you sure you want to quit? [y] or n: ")

                if exit_game in 'YyNn': #Possibility of capital or not
                    break #break the condition of invalid answer

                else:
                    print("Invalid answer")
            if exit_game in ("Yy"): #confirm the break in case of 'y'comand
                break
                """
            if exit_game not in ("nN"): #confirm the break in case of 'y'comand
                print("")
                break

        elif command == "?":
            print(HELP_TEXT)

        elif command == "p":
            print("Possible positions:",', '.join(get_legal_directions(maze,position)))

        if command == "r":
            interact()

        if command not in DIRECTIONS+"p?bqr":
            print("Invalid command:",command)


    return None


def change_maze(maze):
    # Regra do movimento
    # '0' cells turn '1' if they have a number of adjacent '1' cells greater than 1 and less than 5. Otherwise,
    #  they remain '0'.

    # '1' cells remain '1' if they have a number of '1' adjacent cells greater than 3 and less than 6. Otherwise,
    #  they become '0'.

    # Set height and weight
    height = maze_rows(maze) #65
    width = maze_columns(maze) #85

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


if __name__ == '__main__':
    interact()
