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
BLACK = (0, 0, 0)

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
INITIAL_NEXT_PIPE_X = 600

game_state = "PLAYING"

running = True

score = 0

def display_message(message):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, BLACK)
    window.blit(text, (WINDOW_WIDTH//2 - text.get_width()//2, WINDOW_HEIGHT//2 - text.get_height()//2))

class Bird:
    def __init__(self):
        self.x = 50
        self.y = WINDOW_HEIGHT // 2
        self.velocity = 0
        self.hit_ground = False

    def draw(self):
        pygame.draw.rect(window, RED, (BIRD_X_DRAW, self.y, BIRD_SIZE, BIRD_SIZE))

    def flap(self):
        self.velocity = JUMP_VELOCITY

    def update(self):
        self.x += BIRD_X_SPEED

        self.velocity = max(TERMINAL_VELOCITY, self.velocity - GRAVITY)
        self.y += -self.velocity

        if self.y + BIRD_SIZE > WINDOW_HEIGHT:
            self.y = WINDOW_HEIGHT - BIRD_SIZE  # Prevent sinking into the ground
            self.hit_ground = True

        

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
        self.next_pipe_x = INITIAL_NEXT_PIPE_X

    def update(self):
        if bird.x + WINDOW_WIDTH > self.next_pipe_x:
            print("a")
            self.pipe_pairs.append(PipePair(self.next_pipe_x))
            self.next_pipe_x += PIPE_X_GAP

        self.pipe_pairs = [p for p in self.pipe_pairs if p.x > bird.x - PIPE_WIDTH]

    def draw(self):
        for pipe_pair in self.pipe_pairs:
            pipe_pair.draw()

    def check_collision(self, bird):
        bird_rect = pygame.Rect(BIRD_X_DRAW, bird.y, BIRD_SIZE, BIRD_SIZE)
        for pipe in self.pipe_pairs:
            upper_pipe_rect = pygame.Rect(pipe.x - bird.x, 0, PIPE_WIDTH, pipe.gap_start)
            lower_pipe_rect = pygame.Rect(pipe.x - bird.x, pipe.gap_start + PIPE_Y_GAP, PIPE_WIDTH, WINDOW_HEIGHT)

            if bird_rect.colliderect(upper_pipe_rect) or bird_rect.colliderect(lower_pipe_rect):
                return True  
        return False 

bird = Bird()
pipe_service = PipeService()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if game_state == "PLAYING":
                bird.flap()
            elif game_state == "GAME_OVER":
                bird = Bird()
                pipe_service = PipeService()
                game_state = "PLAYING"

    

    if game_state == "PLAYING":
        window.fill(WHITE)
        pipe_service.update()
        bird.update()
        pipe_service.draw()
        bird.draw()
        if pipe_service.check_collision(bird) or bird.hit_ground:
            game_state = "GAME_OVER"
    elif game_state == "GAME_OVER":
        display_message("Press space bar to start again")

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()


