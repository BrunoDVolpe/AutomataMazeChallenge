from stone_pygame_ia_support import *
import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.SysFont('arial', 25)

Point = namedtuple('Point', 'x, y')

class MazeChallengeAI:

    def __init__(self, w=870, h=670):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Stone Automata Maze Challenge')
        self.clock = pygame.time.Clock()
        self.reset()


    def reset(self):
        # init game state
        self.pos_x_max, self.pos_y_max = START_POSITION
        self.player_position = Point(self.pos_x_max, self.pos_y_max)
        self.score = 0
        self.movements_list = []
        self.frame_iteration = 0
        self.square = START
        self.maze = load_maze(INITIAL_MAZE)


    def play_step(self, action):
        maze_bk = self.maze
        player_position_bk = self.player_position
        square_bk = self.square
        self.maze = self.change_maze(self.maze)
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # 2. move
        self._move(action) # update the position and square

        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision():
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # Place conditions
        # Verify wall
        if self.square in WALL:
            self.maze = maze_bk
            self.player_position = player_position_bk
            self.square = square_bk
            self.frame_iteration -= 1
            reward = -1

        elif self.square not in GOOD_POSITION + BAD_POSITION:
            self.score += 1
            reward = 0
            self.movements_list.append(self.direction.upper())
            if self.pos_x_max < self.player_position.x or self.pos_y_max < self.player_position.y:
                #Correct max x and y
                if self.pos_x_max < self.player_position.x:
                    self.pos_x_max = self.player_position.x
                    reward += 2
                elif self.pos_y_max < self.player_position.y:
                    self.pos_y_max = self.player_position.y
                    reward += 2
                
                if self.player_position.x > 60 or self.player_position.y > 60:
                    reward += 64
                elif self.player_position.x > 50 or self.player_position.y > 50:
                    reward += 32
                elif self.player_position.x > 40 or self.player_position.y > 40:
                    reward += 16
                elif self.player_position.x > 30 or self.player_position.y > 30:
                    reward += 8
                elif self.player_position.x > 20 or self.player_position.y > 20:
                    reward += 4
                else:
                    reward += 2


            # Penalizar se voltar
            elif player_position_bk.x > self.player_position.x or player_position_bk.y > self.player_position.y:
                reward -= 1


        elif self.square in GOOD_POSITION:
            reward = 100
            self.movements_list.append(self.direction.upper())
            print(WIN_TEXT)
            print(self.movements_list)
            game_over = True
            return reward, game_over, self.score
        
        # 5. update ui
        self._update_ui()
 
        # 6. return game over and score
        return reward, game_over, self.score
        
        
    def is_collision(self, pt=None):
        if pt == None:
            pt = self.square
        if pt in BAD_POSITION:
            return True
        return False


    def _update_ui(self):
        self.display.fill(WHITE)

        player_in_maze = position_to_index(self.player_position, maze_columns(self.maze))
        maze = self.maze[:int(player_in_maze)] + PLAYER + self.maze[int(player_in_maze)+1:]

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

            elif char == BAD_POSITION:
                pygame.draw.rect(self.display, GREEN, ((screen_position),BLOCK_SIZE))
                screen_x += BLOCK_SIZE[0]
            
            elif char == WALL:
                pygame.draw.rect(self.display, BLACK, ((screen_position),BLOCK_SIZE))
                screen_x += BLOCK_SIZE[0]

            else:
                screen_x = 0
                screen_y += BLOCK_SIZE[1]

            screen_position = (screen_x, screen_y)
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()


    def _move(self, action):
        if np.array_equal(action, [1, 0, 0, 0]):
            new_dir = 'w'
        elif np.array_equal(action, [0, 1, 0, 0]):
            new_dir = 's'
        elif np.array_equal(action, [0, 0, 1, 0]):
            new_dir = 'a'
        else: # [0, 0, 0, 1]
            new_dir = 'd'

        legal_directions = self.get_legal_directions(self.maze, self.player_position)
        if len(legal_directions) > 0 and new_dir not in legal_directions:
            new_dir = legal_directions[random.randint(0,200) % len(legal_directions)]

        self.direction = new_dir
        delta = DIRECTION_DELTAS[self.direction]
        self.player_position = Point(self.player_position[0]+delta[0],self.player_position[1]+delta[1])

        pos_square = position_to_index(self.player_position, maze_columns(self.maze))

        self.square = self.maze[pos_square]


    def get_maze(self):
        return self.maze
    
    
    def change_maze(self, maze):
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
    
    # Helping Model
    def more_than_1_way(self, point_position, maze):
        # Points around the given position
        point_l = Point(point_position.x - 1, point_position.y)
        point_r = Point(point_position.x + 1, point_position.y)
        point_u = Point(point_position.x, point_position.y - 1)
        point_d = Point(point_position.x, point_position.y + 1)

        # Squares around the given position in the given maze
        square_l = maze[position_to_index(point_l, maze_columns(maze))]
        square_r = maze[position_to_index(point_r, maze_columns(maze))]
        square_u = maze[position_to_index(point_u, maze_columns(maze))]
        square_d = maze[position_to_index(point_d, maze_columns(maze))]

        squares = [square_l, square_r, square_u, square_d]
        
        count = 0
        for square in squares:
            if square != WALL and square != BAD_POSITION:
                count += 1
        
        if count > 0:
            return True
        return False
    

    def get_legal_directions(self, maze, position):
        """
        takes a maze string and a position, and returns a list of
        legal directions for that square.
        """
        moves=[]
        for c in DIRECTIONS:
            square = self.move(maze,position,c)
            if square not in WALL and square != '1':
                moves.append(c)
        return moves

        
    def move(self, maze, position, direction):
        """
        takes a maze string, a position of a square and a direction and
        returns the resulting square after the move.
        """

        T1 = maze_columns(maze)
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

if __name__ == "__main__":
    game = MazeChallengeAI(w=87*BLOCK_SIZE[0], h=67*BLOCK_SIZE[1])

    # game loop
    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break

    print('Final Score', score)

    pygame.quit()