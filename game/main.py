import pygame
import sys
import random

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 800
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("My Game")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

BIRD_SIZE = 50
BIRD_X_DRAW = 50
BIRD_X_SPEED = 3
GRAVITY = 0.1
TERMINAL_VELOCITY = -2
JUMP_VELOCITY = 5

X_VELOCITY = 5

PIPE_X_GAP = 600
PIPE_Y_GAP = 300
PIPE_WIDTH = 150
PIPE_GAP_MARGIN = 150

running = True

score = 0

class Bird:
    def __init__(self):
        self.x = 50
        self.y = WINDOW_HEIGHT // 2
        self.velocity = 0

    def draw(self):
        pygame.draw.rect(window, RED, (BIRD_X_DRAW, self.y, BIRD_SIZE, BIRD_SIZE))

    def flap(self):
        self.velocity = JUMP_VELOCITY

    def update(self):
        self.x += BIRD_X_SPEED

        self.velocity = max(TERMINAL_VELOCITY, self.velocity - GRAVITY)
        self.y += -self.velocity

class PipePair:
    def __init__(self, x):
        self.x = x
        self.gap_start = random.randrange(PIPE_GAP_MARGIN, WINDOW_HEIGHT - PIPE_GAP_MARGIN - PIPE_Y_GAP )

    def draw(self):
        pygame.draw.rect(window, GREEN, (self.x - bird.x, 0, PIPE_WIDTH, self.gap_start))
        pygame.draw.rect(window, GREEN, (self.x - bird.x, self.gap_start + PIPE_Y_GAP, PIPE_WIDTH, WINDOW_HEIGHT))

class PipeService:
    def __init__(self):
        self.pipe_pairs = []
        self.next_pipe_x = 600

    def update(self):
        if bird.x + WINDOW_WIDTH > self.next_pipe_x:
            print("a")
            self.pipe_pairs.append(PipePair(self.next_pipe_x))
            self.next_pipe_x += PIPE_X_GAP

        self.pipe_pairs = [p for p in self.pipe_pairs if p.x > bird.x - PIPE_WIDTH]

    def draw(self):
        for pipe_pair in self.pipe_pairs:
            pipe_pair.draw()

bird = Bird()
pipe_service = PipeService()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird.flap()

    window.fill(WHITE)

    pipe_service.update()
    bird.update()
    pipe_service.draw()
    bird.draw()

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()


