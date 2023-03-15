import pygame
import random
import sys
import numpy as np
import consts as consts


class Food:
    def __init__(self):
        self.x = random.randint(
            0, (consts.SCREEN_WIDTH - consts.BLOCK_SIZE) / consts.BLOCK_SIZE) * consts.BLOCK_SIZE
        self.y = random.randint(
            0, (consts.SCREEN_HEIGHT - consts.BLOCK_SIZE) / consts.BLOCK_SIZE) * consts.BLOCK_SIZE
        self.pos = (self.x, self.y)

    def draw(self, screen):
        food = pygame.Rect(self.pos, (consts.BLOCK_SIZE, consts.BLOCK_SIZE))
        pygame.draw.rect(screen, (255, 0, 0), food)

        pygame.display.flip()


class Snake:
    ''' Constructor
        length: length of snake
        positions: list of tuples containing x and y coordinates of snake
        direction: direction of snake
    '''

    def __init__(self):
        self.length = 1
        self.positions = [((consts.SCREEN_WIDTH / 2), (consts.SCREEN_HEIGHT / 2))]
        self.direction = random.choice(["up", "down", "left", "right"])

    def draw(self, screen):
        for position in self.positions:
            snake_body = pygame.Rect(position, (consts.BLOCK_SIZE, consts.BLOCK_SIZE))
            pygame.draw.rect(screen, (0, 0, 255), snake_body)

        pygame.display.flip()

    def move(self, action):
        clock_wise = ["up", "right", "down", "left"]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]
        else:
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]

        self.direction = new_dir

        # update positions of snake keeping the head in the same direction
        cur_x, cur_y = self.positions[0]
        if self.direction == "up":
            new = (cur_x, cur_y - consts.BLOCK_SIZE)
        elif self.direction == "down":
            new = (cur_x, cur_y + consts.BLOCK_SIZE)
        elif self.direction == "left":
            new = (cur_x - consts.BLOCK_SIZE, cur_y)
        elif self.direction == "right":
            new = (cur_x + consts.BLOCK_SIZE, cur_y)

        self.positions.insert(0, new)

        if len(self.positions) > self.length:
            self.positions.pop()


class GameAI:
    def __init__(self, width=consts.SCREEN_WIDTH, height=consts.SCREEN_HEIGHT):
        self.width = width
        self.height = height
        self.game_done = False

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.reset()

    def draw_grid(self):
        self.screen.fill((0, 0, 0))

    def check_collision(self, pt=None):
        if pt is None:
            pt = self.snake.positions[0]

        reset = False
        if pt[0] > consts.SCREEN_WIDTH or pt[0] < 0:
            return True
        if pt[1] > consts.SCREEN_HEIGHT or pt[1] < 0:
            return True
        if pt in self.snake.positions[1:]:
            return True
        
        if self.snake.positions[0] == self.food.pos:
            self.snake.length += 1
            self.score += 1
            self.reward = 10
            self.food = Food()

        return False
            

    def reset(self):
        self.snake = Snake()
        self.food = Food()
        self.frame_iterations = 0
        self.score = 0

    def play_step(self, action):
        self.frame_iterations += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self.snake.move(action)
        self.reward = 0
        self.game_done = False

        if self.check_collision() or self.frame_iterations > 100 * len(self.snake.positions):
            self.game_done = True
            self.reward = -10
            return self.reward, self.game_done, self.score

        self.draw_grid()
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        self.clock.tick(consts.TICK_RATE)

        return self.reward, self.game_done, self.score
