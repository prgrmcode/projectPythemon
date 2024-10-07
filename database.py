import sqlite3

conn = sqlite3.connect("player_pokemon.db")
cursor = conn.cursor()

# Create a table to store player Pokémon
cursor.execute('''
    CREATE TABLE IF NOT EXISTS player_pokemon (
        id INTEGER PRIMARY KEY,
        name TEXT,
        level INTEGER,
        hp INTEGER,
        attack INTEGER,
        defense INTEGER,
        sprite_path TEXT
    )
''')

conn.commit()
