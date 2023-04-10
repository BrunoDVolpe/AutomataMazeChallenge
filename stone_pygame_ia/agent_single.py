import torch
import random
import numpy as np
from collections import deque
from game_single import MazeChallengeAI, Point
from stone_pygame_ia_support import *
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1024
LR = 0.001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        #self.model = Linear_QNet(# de models, aqui supostamente pode mudar, # de saídas/ ações)
        #self.model = Linear_QNet(14, 256, 4)
        self.model = Linear_QNet(12, 1024, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)


    def get_state(self, game):
        position = game.player_position
        actual_maze = game.get_maze()
        maze = game.change_maze(actual_maze)
        nxt_maze = game.change_maze(maze)

        point_l = Point(position.x - 1, position.y)
        point_r = Point(position.x + 1, position.y)
        point_u = Point(position.x, position.y - 1)
        point_d = Point(position.x, position.y + 1)
        
        square_l = maze[position_to_index(point_l, maze_columns(maze))]
        square_r = maze[position_to_index(point_r, maze_columns(maze))]
        square_u = maze[position_to_index(point_u, maze_columns(maze))]
        square_d = maze[position_to_index(point_d, maze_columns(maze))]

        state = [
            # Danger up
            game.is_collision(square_u),

            # Danger left
            game.is_collision(square_l),

            # Danger down
            game.is_collision(square_d),

            # Danger right
            game.is_collision(square_r),
            
            # If up, more than 1 way?
            game.more_than_1_way(point_u, nxt_maze),

            # If left, more than 1 way?
            game.more_than_1_way(point_l, nxt_maze),

            # If down, more than 1 way?
            game.more_than_1_way(point_d, nxt_maze),

            # If right, more than 1 way?
            game.more_than_1_way(point_r, nxt_maze),

            # Wall up
            square_u == WALL,

            # Wall left
            square_l == WALL,

            # Wall down
            square_d == WALL,

            # Wall right
            square_r == WALL,

            # Está na última coluna
            #position.x < (maze_columns(maze) - 1),

            #Está na última linha
            #position.y < (maze_rows(maze) - 1),
            ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 3)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = MazeChallengeAI()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()