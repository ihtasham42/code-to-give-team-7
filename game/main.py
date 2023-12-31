import pygame
import sys
import random
import sounddevice as sd
import numpy as np
import time

pygame.init()

# Loading audio files
beep_sound = pygame.mixer.Sound('beep.mp3') # played  when the bird is too high/low relative the the pipe entry
clear_sound = pygame.mixer.Sound('clear.mp3') # played when the bird clears the pipes
fail_sound = pygame.mixer.Sound('fail.mp3') # played when bird collides with pipe or hits the ground

flap_sound = pygame.mixer.Sound("game/sfx/flap.mp3")


score = 0

big_font = pygame.font.Font(None, 72)

# Constants
CHUNK_SIZE = 1024  # Number of frames per buffer
RATE = 44100  # Sample rate (samples per second)
THRESHOLD = 0.1  # Adjust this threshold value as needed

# Initialize a list to store loudness values for plotting
loudness_values = []

# Set the input device index (change this to the appropriate index)
input_device_index = 1  # Change this to the desired input device index

# Variable to store the time of the last detected spike
last_spike_time = time.time()

WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 800
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("My Game")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

BIRD_SIZE = 50
BIRD_X_DRAW = 50
BIRD_X_SPEED = 2
GRAVITY = 0.1
TERMINAL_VELOCITY = -2
JUMP_VELOCITY = 5

X_VELOCITY = 5

PIPE_X_GAP = 600
PIPE_Y_GAP = 300
PIPE_WIDTH = 150
PIPE_GAP_MARGIN = 150
INITIAL_NEXT_PIPE_X = 600

bird_image = pygame.image.load('game/img/bird.png')
bird_image = pygame.transform.scale(bird_image, (BIRD_SIZE * 1.2, BIRD_SIZE))

background_image = pygame.image.load('game/img/background.png')  # Add your path here
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
background_x = 0  # initial position
SCROLL_SPEED = 5  # adjust the speed as needed

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
        window.blit(bird_image, (BIRD_X_DRAW, self.y))

    def flap(self):
        self.velocity = JUMP_VELOCITY
        flap_sound.play()

    def update(self):
        self.x += BIRD_X_SPEED

        self.velocity = max(TERMINAL_VELOCITY, self.velocity - GRAVITY)
        self.y += -self.velocity

        if self.y + BIRD_SIZE > WINDOW_HEIGHT:
            self.y = WINDOW_HEIGHT - BIRD_SIZE  # Prevent sinking into the ground
            self.hit_ground = True

        closest_pipe_pair = None

        for pipe_pair in pipe_service.pipe_pairs:
            if pipe_pair.x > bird.x:
                if not closest_pipe_pair or pipe_pair.x - bird.x < closest_pipe_pair.x - bird.x:
                    closest_pipe_pair = pipe_pair

        if closest_pipe_pair:
            global distance_to_gap
            distance_to_gap = abs(closest_pipe_pair.gap_start + PIPE_Y_GAP // 2 - bird.y)

        print(distance_to_gap)
        

class PipePair:
    def __init__(self, x):
        self.x = x
        self.gap_start = random.randrange(PIPE_GAP_MARGIN, WINDOW_HEIGHT - PIPE_GAP_MARGIN - PIPE_Y_GAP )
        self.passed = False

    def draw(self):
        pygame.draw.rect(window, RED, (self.x - bird.x, 0, PIPE_WIDTH, self.gap_start))
        pygame.draw.rect(window, RED, (self.x - bird.x, self.gap_start + PIPE_Y_GAP, PIPE_WIDTH, WINDOW_HEIGHT))

def draw_status():
    global score

    score_text = big_font.render(str(score), True, (0, 0, 0)) 

    window.blit(score_text, (20, 20)) 

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

    def check_score(self, bird):
        for pipe in self.pipe_pairs:
            if pipe.x < bird.x and not pipe.passed:
                pipe.passed = True
                clear_sound.play()
                global score
                score += 1

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
distance_to_gap = 0

# Function to callback for capturing audio data
def callback(indata, frames, callback_time, status):
    print('hello world')
    global last_spike_time
    # Calculate loudness as root mean square (RMS) of the audio signal
    loudness = np.sqrt(np.mean(indata**2))
    # print(f"Loudness: {loudness:.2f} dB")
    # Check if loudness exceeds the threshold
    if loudness > THRESHOLD:
        current_time = time.time()
        if current_time - last_spike_time >= 1:  # Check if at least 1 second has passed since the last spike
            print("True")  # Print True when loudness spikes
            bird.flap()
            last_spike_time = current_time
    # Store loudness values for plotting
    loudness_values.append(loudness)

with sd.InputStream(device=input_device_index, channels=1, samplerate=RATE, callback=callback, blocksize=CHUNK_SIZE):
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                
                if game_state == "PLAYING":
                    bird.flap()
                elif game_state == "GAME_OVER":
                    score = 0
                    bird = Bird()
                    pipe_service = PipeService()
                    game_state = "PLAYING"

<<<<<<< HEAD
        

        if game_state == "PLAYING":
            window.fill(WHITE)
            
            
            
            pipe_service.update()
            bird.update()
            pipe_service.draw()
            pipe_service.check_score(bird) 
            bird.draw()

            # Placeholder values of y1 and y2 - will need to be updated with current values of y1 and y2 (refer to excalidraw)
            y1 = 400
            y2 = 200
            # Placeholder values of x_bird and y_bird - will need to be updated with the current x and y position of the bird
            x_bird = 300 
            y_bird = 300 

            # if birds current y position is postion then no alert will be played
            if y2 <= y_bird <= y1:
                beep_volume = 0.0
            
            elif y_bird > y1:
                # beep gets louder and more frequent the higher the bird goes above y1, beep_volume between 0 and 1 
                beep_volume = (y_bird - y1) / (WINDOW_HEIGHT - y1)

            elif y_bird < y2:
                # beep gets louder the lower the bird goes below y2
                beep_volume = (y2 - y_bird) / y2


            if x_bird > INITIAL_NEXT_PIPE_X and x_bird < INITIAL_NEXT_PIPE_X + PIPE_WIDTH and y2 <= y_bird <= y1:
                # if the bird clears the pipe, then a 'success' sound will be played
                clear_sound.play() 
=======
    if game_state == "PLAYING":
        background_x -= SCROLL_SPEED
        if background_x <= -WINDOW_WIDTH:
            background_x = 0

        # Draw the background
        window.blit(background_image, (background_x, 0))
        window.blit(background_image, (background_x + WINDOW_WIDTH, 0))

        pipe_service.update()
        bird.update()
        pipe_service.draw()
        pipe_service.check_score(bird) 
        bird.draw()

        # Placeholder values of x_bird and y_bird - will need to be updated with the current x and y position of the bird
        x_bird = bird.x
        y_bird = bird.y

        yToGap = abs(distance_to_gap)
        # if birds current y position is postion then no alert will be played


        if yToGap < PIPE_Y_GAP // 2: # if bird within the gap of pipe
            beep_volume = 0.0
        
        
        elif yToGap > PIPE_Y_GAP // 2:
            # beep gets louder the higher the bird goes above y1, beep_volume between 0 and 1 
            distance_to_gap_edge = yToGap - PIPE_Y_GAP // 2
            beep_volume = min(1.0, distance_to_gap_edge / (PIPE_Y_GAP // 2))

            # Set volume
            beep_sound.set_volume(beep_volume)
            beep_sound.play()


       
>>>>>>> 11009f5f19e24400748789176202299d42458f36


            if pipe_service.check_collision(bird) or bird.hit_ground:
                game_state = "GAME_OVER"
                fail_sound.play() # fail sound will be played, so user is aware they need to restart
        elif game_state == "GAME_OVER":
            display_message(f"You scored {score}. Press space bar to start again!")

<<<<<<< HEAD
        # Set volume
        beep_sound.set_volume(beep_volume)
        beep_sound.play()
=======
>>>>>>> 11009f5f19e24400748789176202299d42458f36

        draw_status()

        pygame.display.flip()

        pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
