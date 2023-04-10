# Maze
INITIAL_MAZE = 'initial_maze_hash.txt'

# Previous steps
MEMORY = 'steps_memory_pygame.csv'

# Maze symbol constants
OPEN = '0'
WALL = '#'
START = '3'
END = '4'
PLAYER = 'P'

START_POSITION = (1, 1)
GOOD_POSITION = '4' # fim / prêmio
BAD_POSITION = '1'

DIRECTIONS = ['w', 'a', 's', 'd']

DIRECTION_DELTAS = {
    'w': (-1, 0),
    'd': (0, 1),
    's': (1, 0),
    'a': (0, -1)
}

HELP_TEXT = """? or h - Help.
w - Move North one square.
s - Move South one square.
d - Move East one square.
a - Move West one square.
r - Restart the game.
q - Quit the game.
p - List all legal directions from the current position."""

LOSE_TEXT = "Oh no! You lose :("
WIN_TEXT = "Congratulations - you reached the corner!"

def load_maze(filename):
    """
    Loads a maze from file, ignoring surrounding whitespace.

    load_maze(str) -> str
    """

    with open(filename, 'r') as f:
        return f.read().strip()

def maze_columns(maze):
    """
    Returns the number of columns in the maze.

    maze_columns(str) -> int
    """

    return maze.find('\n')

def maze_rows(maze):
    """
    Returns the number of rows in the maze.

    maze_rows(str) -> int
    """

    return maze.count('\n') + 1

def position_to_index(position, columns):
    """
    Converts a (row, column) position pair into a single index.

    position_to_index((int, int), int) -> int
    """

    row, column = position
    return row * (columns + 1) + column

def index_to_position(index, columns):
    """
    Converts a single index into a (row, column) position pair.

    index_to_position(int, int) -> (int, int)
    """

    row = index // (columns + 1)
    column = index % (columns + 1)

    return row, column