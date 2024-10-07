import datetime

import pygame
import random
import sys
import time

import pygame_graphics
from database import conn
from game_logic_last import game_state, start_battle
from utils import custom_print as print  # Import and alias the custom print function


# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Pythemon Battle")

# Load images
background_image = pygame_graphics.load_background_image()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Fonts
font = pygame.font.Font(None, 36)

# Game state
player_pokemon = game_state.player_pokemon
wild_pokemon = game_state.get_random_wild_pokemon()
print("main wild pokemon line 27: ", wild_pokemon)


# Define game phases
PHASE_START = 0
PHASE_BATTLE = 1
PHASE_RESULT = 2

current_phase = PHASE_START

# Main game loop
running = True
clock = pygame.time.Clock()

def load_color():
    # Determine whether it's daytime or nighttime
    current_time = datetime.datetime.now().time()
    is_daytime = current_time >= datetime.time(6, 0) and current_time <= datetime.time(19, 11)

    # Load background image based on the time of day
    if is_daytime:
        color = (0, 0, 0)
    else:
        color = (255, 255, 255)
    return color

def update_screen():
    screen.blit(background_image, (0, 0))
    pygame.display.flip()


def display_text(text, position, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)
    pygame.display.flip()



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    update_screen()

    color = load_color()

    if current_phase == PHASE_START:
        display_text("Press ENTER to start the game!", (200, 300), color)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            current_phase = PHASE_BATTLE
            # battle(player_pokemon, wild_pokemon)
            print("line83, I am in main.py PHASE_BATTLE")
            start_battle(player_pokemon, wild_pokemon, screen)
            current_phase = PHASE_RESULT

    elif current_phase == PHASE_RESULT:
        display_text("Battle ended. Press ESC to quit.", (200, 300), (155, 155, 144))
        # print("main.py")
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
conn.close()
sys.exit()

