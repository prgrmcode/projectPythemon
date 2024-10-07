import random
import requests
from pygame_graphics import pokemon_sprites, pokemon_sprites_files
from utils import custom_print as print  # Import and alias the custom print function



def get_pokemon_data(id_pokemon=None):
    # Fetch data from PokeAPI for a random Pokémon
    if id_pokemon == None:
        random_pokemon_id = random.randint(1, 151)  # Only gen. 1 pokemons
    else:
        random_pokemon_id = id_pokemon
    api_url = f"https://pokeapi.co/api/v2/pokemon/{random_pokemon_id}/"
    response = requests.get(api_url)
    pokemon_data = response.json()
    stats_json = pokemon_data['stats']

    # Extract Pokémon name
    wild_pokemon_name = pokemon_data["name"].capitalize()

    base_experience = pokemon_data["base_experience"]

    # Load the corresponding sprite image
    sprite = pokemon_sprites[random_pokemon_id]
    sprite_path = pokemon_sprites_files[random_pokemon_id]
    print("sprite_path in get_pokemon func: ", sprite_path)
    print("wildpokemon id: ", random_pokemon_id)
    print("line23, getpokemondata in get_pokemon.py")


    # Get hp and attack stats from the stats list
    hp = 100
    attack = 15
    defence = 15

    # ref.:https://notebook.community/Sebbenbear/notebooks/PokeAPI:
    for stat in stats_json:
        stat_name = stat['stat']['name'].title()
        base_stat = stat['base_stat']
        if stat_name == 'Hp':
            hp = base_stat
        elif stat_name == 'Attack':
            attack = base_stat
            print("attacking stat:", attack)
        elif stat_name == 'Defense':
            defence = base_stat


    # get attack from stats:
    rand_num = random.randint(3, 6)
    # attack = attack // rand_num
    print("attack attack = attack // rand_num:", attack)

    level = random.randint(1, 15)
    hp = hp + level * 5

    return wild_pokemon_name, hp, attack, sprite, level, defence, base_experience, sprite_path
