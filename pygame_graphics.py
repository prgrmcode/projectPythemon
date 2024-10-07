import pygame
import os
import datetime
import re
from load_color import load_color
from utils import custom_print as print  # Import and alias the custom print function


# Initialize the game
pygame.init()

# Initialize Pygame font for displaying text
pygame.font.init()
font = pygame.font.SysFont(None, 36)

# Define text colors
WHITE = (255, 255, 255)

# Set up the display
WIDTH, HEIGHT = 800, 600
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pythemon RPG")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load the icon image
icon_image = pygame.image.load("asset/pokemon2.png")  # Replace "icon.png" with the path to your icon image
# Set the icon
pygame.display.set_icon(icon_image)
print("I am in pygame graphics, after icon image loading line 2")

# Determine whether it's daytime or nighttime
current_time = datetime.datetime.now().time()
is_daytime = current_time >= datetime.time(6, 0) and current_time <= datetime.time(19, 11)

# Load background image based on the time of day
if is_daytime:
    background_image = pygame.image.load("asset/background1.jpg").convert()
else:
    background_image = pygame.image.load("asset/background2.jpg").convert()


def initialize():
    global screen
    screen = pygame.display.get_surface()


# Define Pokémon sprite paths
pokemon_sprites_dir = "sprites-master/sprites/pokemon/other/dream-world"
pokemon_sprites_files = os.listdir(pokemon_sprites_dir)
# Sort the sprite filenames numerically
sorted_sprite_filenames = sorted(pokemon_sprites_files, key=lambda x: int(re.search(r'\d+', x).group()))
# print("sorted_sprite_filenames: ", sorted_sprite_filenames)

# Load Pokémon sprites
pokemon_sprites = []
for sprite_file in sorted_sprite_filenames:
    sprite_path = os.path.join(pokemon_sprites_dir, sprite_file)
    sprite = pygame.image.load(sprite_path).convert_alpha()
    pokemon_sprites.append(sprite)


def animate_pokemon_battle(daytime, player_pokemon, wild_pokemon, pygame_surface):
    # Set up the Pygame display
    initialize()
    animation_frames = 30  # Number of frames for the animation
    for frame in range(animation_frames + 1):
        # Calculate the current scale of the player and wild Pokemon sprites
        scale_factor = frame / animation_frames
        # scale_factor = 3


        current_player_sprite = pygame.transform.scale(
            player_pokemon.sprite,
            (int(player_pokemon.sprite.get_width() * scale_factor),
             int(player_pokemon.sprite.get_height() * scale_factor))
        )
        current_player_rect = current_player_sprite.get_rect(
            center=(WIDTH // 2 - 150, HEIGHT // 2))  # Adjust the x-coordinate

        current_wild_sprite = pygame.transform.scale(
            wild_pokemon.sprite,
            (int(wild_pokemon.sprite.get_width() * scale_factor),
             int(wild_pokemon.sprite.get_height() * scale_factor))
        )
        current_wild_rect = current_wild_sprite.get_rect(
            center=(WIDTH // 2 + 150, HEIGHT // 2))  # Adjust the x-coordinate

        # Calculate new positions for scaled and positioned sprites
        player_pokemon_x = 150
        player_pokemon_y = pygame_surface.get_height() - current_player_sprite.get_height() - 30
        wild_pokemon_x = pygame_surface.get_width() - current_wild_sprite.get_width() - 150
        wild_pokemon_y = pygame_surface.get_height() - current_wild_sprite.get_height() - 30

        # Display the background text
        if daytime:
            background_color = (255, 255, 255)
            text_color = (0, 0, 0)
        else:
            background_color = (0, 0, 0)
            text_color = (255, 255, 255)

        # Clear the surface
        pygame_surface.fill(background_color)  # Fill with black background color

        # Display the player Pokemon sprite
        pygame_surface.blit(current_player_sprite, current_player_rect)
        # Display the player's Pokémon sprite
        # pygame_surface.blit(current_player_sprite, (player_pokemon_x, player_pokemon_y))

        # Display the wild Pokemon sprite
        pygame_surface.blit(current_wild_sprite, current_wild_rect)


        # Update the display
        pygame.display.update()

        # Wait for a short period to simulate animation
        # pygame.time.wait(1000)

        # Clear the surface
        # pygame_surface.fill(background_color)

        # Update the display
        pygame.display.update()
        pygame.time.delay(50)  # Delay between frames


# this function was inspired by ref.: https://www.geeksforgeeks.org/pygame-character-animation/
def animate_pokemon_capturing(pygame_surface, wild_pokemon, daytime):
    # Set up the Pygame display
    initialize()

    # Display the background text
    if daytime:
        background_color = (255, 255, 255)
        text_color = (0, 0, 0)
    else:
        background_color = (0, 0, 0)
        text_color = (255, 255, 255)

    pygame_surface.fill(background_color)
    font = pygame.font.Font(None, 36)
    text = font.render(f"Capturing {wild_pokemon.name}...", True, text_color)
    text_rect = text.get_rect(center=(pygame_surface.get_width() // 2, pygame_surface.get_height() // 2))
    pygame_surface.blit(text, text_rect)

    # Update the display
    pygame.display.update()

    # Simulate capturing animation
    pygame.time.wait(1000)

    # Display the captured Pokéball
    pokeball_sprite = pygame.image.load("asset/pokeball.png").convert_alpha()
    pokeball_scale_factor = 0.5  # Adjust this value as needed
    pokeball_sprite = pygame.transform.scale(pokeball_sprite, (int(pokeball_sprite.get_width() * pokeball_scale_factor),
                                                               int(pokeball_sprite.get_height() * pokeball_scale_factor)))

    pokeball_x = pygame_surface.get_width() // 2 - pokeball_sprite.get_width() // 2
    pokeball_y = pygame_surface.get_height() // 2 - pokeball_sprite.get_height() // 2

    pygame_surface.fill(background_color)
    pygame_surface.blit(pokeball_sprite, (pokeball_x, pokeball_y))
    pygame.time.delay(50)  # Delay between frames

    # Update the display
    pygame.display.update()

    # Wait for a short period to display the Pokéball
    pygame.time.wait(1000)

    # Clear the surface
    pygame_surface.fill(background_color)

    # Update the display
    pygame.display.update()
    # Wait for a short period
    pygame.time.wait(1000)

def animate_pokeball_closing(screen, wild_pokemon, is_daytime=is_daytime):
    pokeball_image = pygame.image.load("asset/pokeball.png").convert_alpha()
    pokeball_rect = pokeball_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    if not is_daytime:
        screen.fill((0, 0, 0))  # Fill with black background color
        text_color = (255, 255, 255)
    else:
        screen.fill((255, 255, 255))  # Fill with white background color
        text_color = (0, 0, 0)

    # for angle in range(0, 360, 10):
    #     rotated_pokeball = pygame.transform.rotate(pokeball_image, angle)
    #     screen.blit(rotated_pokeball, pokeball_rect)
    #     pygame.display.flip()
    #     pygame.time.delay(30)

    # ref.:https://blender.stackexchange.com/questions/205629/find-opposite-angle-range-in-radians
    for angle in range(0, 360, 10):
        if not is_daytime:
            screen.fill((0, 0, 0))  # Fill with black background color
        else:
            screen.fill((255, 255, 255))  # Fill with white background color

        rotated_pokeball = pygame.transform.rotate(pokeball_image, angle)
        screen.blit(rotated_pokeball, pokeball_rect)
        pygame.display.flip()
        pygame.time.delay(30)

    # Display the message "You captured the Pokémon!"
    text = font.render(f"You captured {wild_pokemon.name}!", True, text_color)
    # screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(1000)


# Background image loading function
def load_background_image():
    # Determine whether it's daytime or nighttime
    current_time = datetime.datetime.now().time()
    is_daytime = current_time >= datetime.time(6, 0) and current_time <= datetime.time(19, 11)

    # Load background image based on the time of day
    if is_daytime:
        background_image = pygame.image.load("asset/background1.jpg").convert()
    else:
        background_image = pygame.image.load("asset/background2.jpg").convert()
    # Resize the background image to match the screen dimensions
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    return background_image


# Initialize the pygame_surface variable
pygame_surface = None

# Initialize Pygame font for displaying text
pygame.font.init()
font = pygame.font.SysFont(None, 36)


def update_graphics(screen, player_pokemon, wild_pokemon):
    pygame.font.init()  # Initialize the font module
    font = pygame.font.Font(None, 36)

    # Clear the surface
    screen.fill((0, 0, 0))  # Fill with black background color

    # Draw background from the image
    background_image = load_background_image()
    screen.blit(background_image, (0, 0))
    print("line251, I am in update_graphics func in pygame_graphics.py")

    # Draw player's Pokémon sprite
    player_pokemon_x = 100
    player_pokemon_y = 300
    screen.blit(player_pokemon.sprite, (player_pokemon_x, player_pokemon_y))

    # Draw wild Pokémon sprite
    wild_pokemon_x = 500
    wild_pokemon_y = 300
    screen.blit(wild_pokemon.sprite, (wild_pokemon_x, wild_pokemon_y))

    # # Display information text
    # text = f"Player: {player_pokemon.name} | Wild: {wild_pokemon.name}"
    # text_render = font.render(text, True, WHITE)
    # screen.blit(text_render, (10, 10))
    #
    # # Display battle messages
    # y_offset = 60
    # for message in messages:
    #     message_render = font.render(message, True, WHITE)
    #     screen.blit(message_render, (10, y_offset))
    #     y_offset += 30

    # Update the display
    pygame.display.update()  # Use pygame.display.update() instead of pygame.display.flip()


# Create a Pygame widget container
def create_pygame_widget():
    pygame_surface = pygame.Surface((800, 600))
    return pygame_surface

# # main game loop
# running = True
# clock = pygame.time.Clock()
#
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#     # Draw background from the image
#     screen.blit(background_image, (0, 0))
#     print("I am in running in pygame_graphics.py after 'screen.blit(background_image, (0, 0))' ")
#
#     # Draw Pokemon sprites
#     # sprite_x = 100
#     # sprite_y = 300
#     # for pokemon_sprite in pokemon_sprites:
#     #     screen.blit(pokemon_sprite, (sprite_x, sprite_y))
#     #     sprite_x += 100
#
#     pygame.display.flip()
#     clock.tick(60)
#
# # Clean up
# pygame.quit()
