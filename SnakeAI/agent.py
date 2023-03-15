import torch
import random
import numpy as np
from collections import deque
from snake import Snake, Food, GameAI
import consts as consts
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0 # number of games
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) 
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)


    def get_state(self, game):
        head = game.snake.positions[0]
        point_left = (head[0] - consts.BLOCK_SIZE, head[1])
        point_right = (head[0] + consts.BLOCK_SIZE, head[1])
        point_up = (head[0], head[1] - consts.BLOCK_SIZE)
        point_ddown = (head[0], head[1] + consts.BLOCK_SIZE)

        dir_left = game.snake.direction == "left"
        dir_right = game.snake.direction == "right"
        dir_up = game.snake.direction == "up"
        dir_down = game.snake.direction == "down"

        state = [
            # Danger straight
            (dir_right and game.check_collision(point_right)) or
            (dir_left and game.check_collision(point_left)) or
            (dir_up and game.check_collision(point_up)) or
            (dir_down and game.check_collision(point_ddown)),

            # Danger right
            (dir_up and game.check_collision(point_right)) or
            (dir_down and game.check_collision(point_left)) or
            (dir_left and game.check_collision(point_up)) or
            (dir_right and game.check_collision(point_ddown)),

            # Danger left
            (dir_down and game.check_collision(point_right)) or
            (dir_up and game.check_collision(point_left)) or
            (dir_right and game.check_collision(point_up)) or
            (dir_left and game.check_collision(point_ddown)),

            # Move direction
            dir_left,
            dir_right,
            dir_up,
            dir_down,

            # Food location
            game.food.pos[0] < head[0],  # food left
            game.food.pos[0] > head[0],  # food right
            game.food.pos[1] < head[1],  # food up
            game.food.pos[1] > head[1]  # food down
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
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
    game = GameAI()
    while True:
        state_old = agent.get_state(game)

        final_move = agent.get_action(state_old)

        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
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


        
if __name__ == "__main__":
    train()