import datetime
import sys
import time

import pygame
import random

from database import cursor, conn
from get_pokemon import get_pokemon_data
import pygame_graphics
from utils import custom_print as print  # Import and alias the custom print function


# Fonts
font = pygame.font.Font(None, 36)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


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


class GameState:

    def __init__(self):
        print("GameState initialized")
        self.active_pokemon_index = None
        self.player_name = "Ash"
        pokemon_name, pokemon_hp, pokemon_attack, pokemon_sprite, pokemon_level, pokemon_defense, pokemon_base_experience, pokemon_sprite_path = get_pokemon_data(
            25)
        self.player_pokemon = Pokemon(pokemon_name, max_hp=pokemon_hp, attack_power=pokemon_attack,
                                      sprite=pokemon_sprite, level=pokemon_level, defense=pokemon_defense,
                                      base_experience=pokemon_base_experience, sprite_path=pokemon_sprite_path)
        self.player_pokemon_list = []  # List to store player's captured Pokémon
        self.wild_pokemon = None  # Wild Pokemon that appears in battles
        self.add_player_pokemon(self.player_pokemon)

    def capture_pokemon(self, pokemon):
        self.player_pokemon_list.append(pokemon)
        self.add_player_pokemon(pokemon)

    def add_player_pokemon(self, pokemon):
        sql_insert = '''
            INSERT INTO player_pokemon (name, level, hp, attack, defense, sprite_path)
            VALUES (?, ?, ?, ?, ?, ?)
        '''

        values = (pokemon.name, pokemon.level, pokemon.hp, pokemon.attack_power, pokemon.defence, pokemon.sprite_path)

        print("SQL Statement:", sql_insert)
        print("Values:", values)

        cursor.execute(sql_insert, values)
        conn.commit()

    def get_player_pokemon(self):
        cursor.execute('SELECT * FROM player_pokemon')
        player_pokemon_data = cursor.fetchall()

        player_pokemon_list = self.player_pokemon_list
        for data in player_pokemon_data:
            name = data['name']
            max_hp = data['max_hp']
            attack_power = data['attack_power']
            sprite = data['sprite']  # Replace this with the actual column name for the sprite path
            player_pokemon = Pokemon(name=name, max_hp=max_hp, attack_power=attack_power, sprite=sprite)
            player_pokemon_list.append(player_pokemon)

        return player_pokemon_list

        # return cursor.fetchall()

    def switch_pokemon(self, new_pokemon_index):
        self.active_pokemon_index = new_pokemon_index

    def choose_switch_pokemon(self, player_pokemon_list):
        switch_index = None
        font = pygame.font.Font(None, 36)
        clock = pygame.time.Clock()

        print("I am in choose_switch_pokemon")

        while switch_index is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            pygame.display.get_surface().fill((0, 0, 0))
            text = font.render("Select a Pokémon to switch to:", True, (255, 255, 255))
            pygame.display.get_surface().blit(text, (50, 50))

            # Display list of Pokémon for switching
            button_y = 100
            for index, pokemon in enumerate(player_pokemon_list):
                button_text = font.render(pokemon.name, True, (255, 255, 255))
                button_rect = button_text.get_rect(topleft=(50, button_y))
                if button_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(pygame.display.get_surface(), (100, 100, 100), button_rect)
                    if pygame.mouse.get_pressed()[0]:
                        switch_index = index
                pygame.display.get_surface().blit(button_text, (button_rect.x + 10, button_rect.y))
                button_y += 40

            pygame.display.flip()
            clock.tick(60)

        return switch_index

    def start_battle(self, wild_pokemon, pygame_surface):
        self.wild_pokemon = wild_pokemon
        print("I am in start_battle line 112 game_logic2")
        # Call the function to start the animations
        pygame_graphics.animate_pokemon_battle(
            pygame_graphics.is_daytime, game_state.player_pokemon, game_state.wild_pokemon, pygame_surface)

    def get_random_wild_pokemon(self):
        # Get Pokémon data
        name, hp, attack, sprite, level, defense, base_experience, sprite_path = get_pokemon_data()

        # Create a wild Pokémon object
        wild_pokemon = Pokemon(name, max_hp=hp, attack_power=attack, sprite=sprite, level=level, defense=defense,
                               base_experience=base_experience, sprite_path=sprite_path)
        return wild_pokemon


class Pokemon:
    def __init__(self, name, max_hp, attack_power, sprite, level, defense, base_experience, sprite_path):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack_power = attack_power
        self.sprite = sprite
        self.level = level
        self.defence = defense
        self.base_experience = base_experience
        self.sprite_path = sprite_path

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def is_alive(self):
        return self.hp > 0

    def attack(self, target_pokemon):
        target_pokemon.take_damage(self.attack_power)


def display_text(screen, messages, color=load_color()):
    y_position = 20
    for message in messages:
        text_surface = font.render(message, True, color)
        screen.blit(text_surface, (20, y_position))
        y_position += 30  # Increase the y-position for the next message
        pygame.display.flip()
        # time.sleep(1)  # Add a delay before displaying the next message


# Implementing the battle system:
def start_battle(player_pokemon, wild_pokemon, screen):
    print("I am in start battle function, game_logic2")
    battle_messages = []  # Store battle messages
    color = load_color()
    # Initialize Pygame
    pygame.init()

    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # pygame.display.set_caption("Pokemon Battle")
    print("wildpokemon sprite: ", wild_pokemon.sprite)
    print("wildpokemon name: ", wild_pokemon.name)
    wild_pokemon_sprite = wild_pokemon.sprite

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if color == (0, 0, 0):
            bg = WHITE
        elif color == (255, 255, 255):
            bg = BLACK
        screen.fill(bg)
        # Implement battle mechanics, player choices, animations, sprites etc
        # font = pygame.font.Font(None, 36)

        battle_messages.append(f"A wild {wild_pokemon.name} appeared!")
        display_text(screen, battle_messages)

        # # Display the player Pokemon sprite
        # player_pokemon_rect = player_pokemon.sprite.get_rect(
        #     center=(WIDTH // 2 - 100, HEIGHT // 2))  # Adjust the x-coordinate
        # screen.blit(player_pokemon.sprite, player_pokemon_rect)

        # # Display the wild Pokemon sprite
        # wild_pokemon_rect = wild_pokemon_sprite.get_rect(
        #     center=(WIDTH // 2 + 100, HEIGHT // 2))  # Adjust the x-coordinate
        # screen.blit(wild_pokemon_sprite, wild_pokemon_rect)

        # Display the wild Pokemon sprite with animation
        animation_frames = 30  # Number of frames for the animation
        for frame in range(animation_frames + 1):
            # Calculate the current scale of the sprite
            scale_factor = frame / animation_frames
            current_sprite = pygame.transform.scale(
                wild_pokemon.sprite,
                (int(wild_pokemon.sprite.get_width() * scale_factor),
                 int(wild_pokemon.sprite.get_height() * scale_factor))
            )
            current_rect = current_sprite.get_rect(
                center=(WIDTH // 2 + 100, HEIGHT // 2))  # Adjust the x-coordinate
            screen.blit(current_sprite, current_rect)
            pygame.display.update()
            pygame.time.delay(50)  # Delay between frames

        time.sleep(1)  # Add a delay before displaying the next message
        pygame.display.flip()  # Update the display

        while player_pokemon.hp > 0 and wild_pokemon.hp > 0:
            battle_messages.append(f"Your {player_pokemon.name} HP: {player_pokemon.hp}")
            battle_messages.append(f"{wild_pokemon.name} HP: {wild_pokemon.hp}")

            display_text(screen, battle_messages)
            print("I am in while after your pikachu, hp: on line 114... ")

            battle_messages.append("What will you do? (Fight(f)/Capture(c)/Flee(e)): ")
            print(
                "line 125:I am in while after battle messages.append What will you do? (Fight(f)/Capture(c)/Flee(f)):... ")
            display_text(screen, battle_messages)
            battle_messages.clear()  # Clear the list after displaying
            pygame.display.flip()  # Update the display

            action = None
            while not action:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_f:
                            action = "fight"
                        elif event.key == pygame.K_c:
                            action = "capture"
                        elif event.key == pygame.K_e:
                            action = "flee"


            # Get player's choice: Fight, Capture, Flee
            # action = input("What will you do? (Fight/Capture/Flee): ").lower()
            screen.fill(bg)
            pygame.display.flip()  # Update the display
            if action:
                battle_messages.append(f"You chose: {action.capitalize()}")
                display_text(screen, battle_messages)
                time.sleep(1)  # Display the choice for a moment
                screen.fill(bg)
                pygame.display.flip()  # Update the display

            if action == "fight":
                # # before starting the battle, trigger switch option for player.
                # switch_index = game_state.choose_switch_pokemon(game_state.player_pokemon_list)
                # if switch_index is not None:
                #     new_pokemon = player_pokemon_list[switch_index]
                #     print(f"You switched to {new_pokemon.name}.")
                #     player_pokemon = new_pokemon
                # # game_state.switch_pokemon(switch_index)

                game_state.start_battle(wild_pokemon, screen)

                wild_pokemon.hp -= player_pokemon.attack_power
                player_pokemon.hp -= wild_pokemon.attack_power
                battle_messages.append("You attacked the wild Pokemon!")

                # # Display the player's Pokémon sprite on the left
                # player_pokemon_sprite = player_pokemon.sprite
                # player_pokemon_rect = player_pokemon_sprite.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                # screen.blit(player_pokemon_sprite, player_pokemon_rect)
                #
                # # Display the wild Pokémon sprite on the right
                # wild_pokemon_sprite = wild_pokemon.sprite
                # wild_pokemon_rect = wild_pokemon_sprite.get_rect(center=(WIDTH * 3 // 4, HEIGHT // 2))
                # screen.blit(wild_pokemon_sprite, wild_pokemon_rect)

                # Display battle messages on the screen
                font = pygame.font.Font(None, 30)
                player_hp_text = font.render(f"Your {player_pokemon.name} HP: {player_pokemon.hp}", True, (0, 0, 0))
                wild_pokemon_hp_text = font.render(f"{wild_pokemon.name} HP: {wild_pokemon.hp}", True, (0, 0, 0))
                screen.blit(player_hp_text, (20, 20))
                screen.blit(wild_pokemon_hp_text, (20, 50))

            elif action == "capture":
                battle_messages = []  # Store battle messages
                capture_chance = 0.5
                if random.random() < capture_chance:
                    # pygame_graphics.animate_pokemon_capturing(screen, wild_pokemon, pygame_graphics.is_daytime)
                    pygame_graphics.animate_pokeball_closing(screen, wild_pokemon)
                    # Wait for a short period
                    battle_messages.append(f"You captured {wild_pokemon.name}!")
                    display_text(screen, battle_messages)
                    game_state.capture_pokemon(wild_pokemon)  # capture and add pokemon to the players pokemons list
                    print("232 game_logic: ", battle_messages)
                    pygame.time.wait(1000)
                    break
                else:
                    battle_messages.append(f"{wild_pokemon.name} escaped the capture!")
                display_text(screen, battle_messages)
                time.sleep(3)  # Add a delay before displaying the next message

            elif action == "flee":
                battle_messages = []  # Store battle messages
                battle_messages.append("You ran away from the battle")
                display_text(screen, battle_messages)
                time.sleep(3)  # Add a delay before displaying the next message
                break
            else:
                battle_messages.append("Invalid choice. Choose Fight, Capture, or Flee.")
                display_text(screen, battle_messages)
                time.sleep(3)  # Add a delay before displaying the next message

            display_text(screen, battle_messages)
            time.sleep(1)  # Add a delay before displaying the next message

            pygame.display.flip()
            clock.tick(60)

        # Check for battle end conditions
        if player_pokemon.hp <= 0:
            battle_messages.append(f"Your {player_pokemon.name} fainted.")
            display_text(screen, battle_messages)
            print(f"Your {player_pokemon.name} fainted. in game_logic2, line 354")
            # Player's Pokémon is knocked out, trigger switch option
            switch_index = game_state.choose_switch_pokemon(game_state.player_pokemon_list)
            if switch_index is not None:
                new_pokemon = game_state.player_pokemon_list[switch_index]
                print(f"You switched to {new_pokemon.name}.")
                player_pokemon = new_pokemon
            else:
                display_text(screen, battle_messages)
                pygame.display.flip()
                clock.tick(60)

            # game_state.switch_pokemon(switch_index)
            # break
        elif wild_pokemon.hp <= 0:
            pygame_graphics.animate_pokemon_capturing(screen, wild_pokemon, pygame_graphics.is_daytime)
            battle_messages.append(f"You defeated the wild {wild_pokemon.name}!"),
            display_text(screen, battle_messages)
            pygame.display.flip()
            clock.tick(60)

            break
        display_text(screen, battle_messages)
        pygame.display.flip()
        clock.tick(60)
        break  # Exit the battle loop after the battle ends


# Initialize game state
game_state = GameState()
