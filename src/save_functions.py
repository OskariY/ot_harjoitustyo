import pickle
import random

def write_game_data(name, game_data):
    """
    Helper function that writes data to a save file
    """
    with open("saves/{}".format(name), "wb") as f:
        pickle.dump(game_data, f)

def load_game(name):
    """
    Helper function that loads data from a save file
    """
    with open("saves/{}".format(name), "rb") as f:
        game_data = pickle.load(f)
    return game_data

def save_game(name, world, inventory, player):
    """
    Saves games files like the game_map, player position, scroll, inventory and mob positions
    """
    game_data = {
        "game_map": world.game_map,
        "spawn_x": world.spawn_x,
        "spawn_y": world.spawn_y,
        "player_x": player.rect.x,
        "player_y": player.rect.y,
        "scrollx": world.scrollx,
        "scrolly": world.scrolly,
        "mob_coords": [],
        "worm_coords": [],
        "inventory": inventory.inventory,

        # world generation parameters
        "seed": world.seed
    }
    for mob in world.mobs:
        game_data["mob_coords"].append([mob.rect.x, mob.rect.y, mob.mobtype])
    for worm in world.worms:
        game_data["worm_coords"].append([worm.head_rect.x, worm.head_rect.y])

    write_game_data(name, game_data)

def create_world(name):
    """
    Creates a new world save
    """
    game_data = {
        "game_map": {},
        "spawn_x": 0,
        "spawn_y": -100,
        "player_x": 200,
        "player_y": -100,
        "scrollx": 0,
        "scrolly": 0,
        "mob_coords": [],
        "worm_coords": [],
        "drops": [],
        "inventory": [],

        # world generation parameters
        "seed": random.randint(-9999999,9999999),
    }
    write_game_data(name, game_data)

