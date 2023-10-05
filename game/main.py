import pygame
import sys

# Initialize Pygame
pygame.init()

# Define window dimensions and create window
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 800
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("My Game")

# Define colors
WHITE = (255, 255, 255)

# Game loop control variable
running = True

# Game loop
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Game logic (update objects, check collisions, etc.)
    
    # Draw everything
    window.fill(WHITE)
    
    # Update display
    pygame.display.flip()
    
    # Cap the frame rate to 60 frames per second
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()


