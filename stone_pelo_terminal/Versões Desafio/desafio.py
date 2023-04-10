import sys

#Globals
"""
U - movement up
D - movement down
R - movement to the right
L - movement to the left
"""
DIRECTIONS = 'UDRL'
HEIGHT = int() # to be defined in main
WIDTH = int() # to be defined in main

def main():
    file = 'input_.txt'
    maze = load_maze(file)
    if not maze:
        sys.exit("Are you sure you have the correct maze.txt file?")
    height = len(maze) #65
    global HEIGHT
    HEIGHT = height
    width = len(maze[0]) - 1 #85
    global WIDTH
    WIDTH = width

    while True:
        print_maze(maze, height)
        spacing()
        command = input().upper()
        if command not in 'UDRL' and command != 'RESTART' and command != 'EXIT':
            if command == '?':
                print('U - movement up',
                    'D - movement down',
                    'R - movement to the right',
                    'L - movement to the left',
                    'RESTART - restart the game',
                    '? - see options',
                    'EXIT - exit the game',
                    sep='\n')
                input('Press anything to continue...')
            else:
                print("Invalid command. Type '?' for info.")
                input('Press anything to continue...')
            spacing()
        elif command == '':
            print("Invalid command. Type '?' for info.")
            input('Press anything to continue...')
            spacing()
        else:
            if command == 'EXIT':
                break
            elif command == 'RESTART':
                input('The game is restarted. Press anything to reload...')
                maze = load_maze(file)
            elif command in 'UDRL':
                maze = change_maze(maze, height, width)
    """
    # original maze print
    print_maze(maze, height)

    # spacing
    spacing(width)

    # new maze print
    maze = change_maze(maze, height, width)
    print_maze(maze, height)
    """

# Laod maze into memory
def load_maze(file):
    # Lista de strings - matrix has 65 rows and 85 columns
    maze = []
    try:
        with open(file, 'r') as f:
            for row in f:
                maze.append(row)
        return maze
    except FileNotFoundError:
        print(f"File '{file}' not found.")


# Change maze according to the rules
def change_maze(maze, height, width):
    # Regra do movimento
    # '0' cells turn '1' if they have a number of adjacent '1' cells greater than 1 and less than 5. Otherwise,
    #  they remain '0'.

    # '1' cells remain '1' if they have a number of '1' adjacent cells greater than 3 and less than 6. Otherwise,
    #  they become '0'.

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
    return maze_cp


#spacing
def spacing():
    print(WIDTH * '-')


# Print maze
def print_maze(maze, height):
    for i in range(height):
        print(maze[i], end='')


if __name__ == "__main__":
    main()