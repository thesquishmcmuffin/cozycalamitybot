import cv2
import pygame
import pygame.font
from PIL import Image, ImageDraw, ImageFont

# Initialize Pygame
pygame.init()

# Load images
background_image = pygame.image.load('ui/overlay.png')
water_bottle_image = pygame.image.load('ui/hydration_meter.png')

# Set up the display
screen_width, screen_height = background_image.get_size()
screen = pygame.display.set_mode((screen_width, screen_height))

# Function to draw the hydration meter
def draw_hydration_meter(hydration_level):
    # Draw the background image
    screen.blit(background_image, (0, 0))

    # Calculate the position for water bottles
    x_offset = 50
    y_offset = screen_height - water_bottle_image.get_height() - 10

    # Draw water bottles
    for i in range(hydration_level):
        screen.blit(water_bottle_image, (x_offset, y_offset))
        x_offset += water_bottle_image.get_width() + 10

    pygame.display.flip()

'''# Main loop
running = True

hydration_level= 3

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update hydration level based on your Twitch bot logic
    # (e.g., when a hydration redemption occurs, increment hydration_level)
    #draw_hydration_meter(hydration_level)

pygame.quit()'''

