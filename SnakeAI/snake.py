import pygame
import random
import sys

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BLOCK_SIZE = 20
TICK_RATE = 8

class Food:
    def __init__(self):
        self.x = random.randint(0, (SCREEN_WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        self.pos = (self.x, self.y)
        
    def draw(self, screen):
        food = pygame.Rect(self.pos, (BLOCK_SIZE, BLOCK_SIZE))
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
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice(["up", "down", "left", "right"])
                                       
    def draw(self, screen):
        for position in self.positions:
            snake_body = pygame.Rect(position, (BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, (0, 0, 255), snake_body)

        pygame.display.flip()

    def move(self):
        if self.direction == "up":
            self.positions.insert(0, (self.positions[0][0], self.positions[0][1] - BLOCK_SIZE))
        elif self.direction == "down":
            self.positions.insert(0, (self.positions[0][0], self.positions[0][1] + BLOCK_SIZE))
        elif self.direction == "left":
            self.positions.insert(0, (self.positions[0][0] - BLOCK_SIZE, self.positions[0][1]))
        elif self.direction == "right":
            self.positions.insert(0, (self.positions[0][0] + BLOCK_SIZE, self.positions[0][1]))

        if len(self.positions) > self.length:
            self.positions.pop()

class Game:
    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
        self.width = width
        self.height = height
        self.game_state = 1
        self.score = 0

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()

        self.snake = Snake()
        self.food = Food()
        self.food.draw(self.screen)

    def draw_grid(self):
        self.screen.fill((0, 0, 0))

    def check_collision(self):
        if self.snake.positions[0][0] > SCREEN_WIDTH or self.snake.positions[0][0] < 0:
            self.reset()
        if self.snake.positions[0][1] > SCREEN_HEIGHT or self.snake.positions[0][1] < 0:
            self.reset()
        if self.snake.positions[0] in self.snake.positions[1:]:
            self.reset()

        if self.snake.positions[0] == self.food.pos:
            self.snake.length += 1
            self.score += 1
            self.food = Food()

    def reset(self):
        self.game_state = 0

    ''' Main Game Loop'''
    def run(self):
        while self.game_state:
            self.clock.tick(TICK_RATE)
            self.draw_grid()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.direction = "up"
                    if event.key == pygame.K_DOWN:
                        self.snake.direction = "down"
                    if event.key == pygame.K_LEFT:
                        self.snake.direction = "left"
                    if event.key == pygame.K_RIGHT:
                        self.snake.direction = "right"

            self.snake.move()
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
            self.check_collision()

        print("SCORE: ", self.score)
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()