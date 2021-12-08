import json

with open("config.json", "r") as f:
    config = json.load(f)

CHUNK_SIZE = 8
TILE_SIZE = 16

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 360
WINDOW_WIDTH = config["windowed_width"]
WINDOW_HEIGHT = config["windowed_height"]
CENTER = [DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2]
FONT = "Helvetica"

# colours
LIGHTBLUE = (173, 216, 230)
DARKBLUE = (100, 140, 160)
BROWN = (131, 101, 57)
GRASSGREEN = (0, 154, 23)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128,128,128)

MOB_SPAWNS = config["mob_spawns"]
MOB_LIMIT = config["mob_limit"]
MUSIC = config["music"]

FULLSCREEN = config["fullscreen"]

# max fps
FPS = 60
