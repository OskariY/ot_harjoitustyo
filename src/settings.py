CHUNK_SIZE = 8
TILE_SIZE = 16

DISPLAY_WIDTH = 400
DISPLAY_HEIGHT = 300
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900
CENTER = [W // 2, H // 2]

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

MOB_SPAWNS = False

# items and tiles
ITEMS = {
    "": {
        "stack": 0,
        "food": False,
        "build": False,
        "tool":  True,
        },
    "pickaxe": {
        "image": pick_image,
        "stack": 1,
        "food": False,
        "build": False,
        "tool":  True,
        },
    "axe": {
        "image": axe_image,
        "stack": 1,
        "food": False,
        "build": False,
        "tool":  True,
        },
    "hoe": {
        "image": hoe_image,
        "stack": 1,
        "food": False,
        "build": False,
        "tool":  True,
        },
    "shovel": {
        "image": shovel_image,
        "stack": 1,
        "food": False,
        "build": False,
        "tool":  True,
        },
    "palosammutin": {
        "image": arrow_image,
        "stack": 999,
        "food": False,
        "build": False,
        "tool": False,
        },
    "hammer": {
        "image": hammer_image,
        "stack": 1,
        "food": False,
        "build": False,
        "tool":  True,
        },
    "meat": {
        "image": meat_image,
        "stack": 999,
        "food": True,
        "heal": 10,
        "build": False,
        "tool": False,
        },
    "dirt": {
        "image": dirttile,
        "stack": 999,
        "food": False,
        "build": True,
        "furniture": False,
        "tool": False,
        },
    "slab": {
        "image": slab_image,
        "stack": 999,
        "food": False,
        "build": True,
        "furniture": True,
        "tool": False,
        },
    "coal block": {
        "image": coaltile,
        "stack": 999,
        "food": False,
        "build": True,
        "furniture": False,
        "tool": False,
        },
    "grass": {
        "image": grasstile,
        "stack": 999,
        "food": False,
        "build": True,
        "furniture": False,
        "tool": False,
        },
    "plant": {
        "image": plant_image,
        "stack": 999,
        "food": False,
        "build": True,
        "tool": False,
        "furniture": False,
        },
    "oak sapling": {
        "image": sapling_image,
        "stack": 999,
        "food": False,
        "build": True,
        "tool": False,
        "furniture": False,
        },
    "snowy grass": {
        "image": snowy_grass,
        "stack": 999,
        "food": False,
        "build": True,
        "tool": False,
        "furniture": False,
        },
    "stone": {
        "image": stonetile,
        "stack": 999,
        "food": False,
        "build": True,
        "furniture": False,
        "tool": False,
        },
    "rock": {
        "image": rocktile,
        "stack": 999,
        "food": False,
        "build": True,
        "furniture": False,
        "tool": False,
        },
    "plank": {
        "image": planktile,
        "stack": 999,
        "food": False,
        "build": True,
        "furniture": False,
        "tool": False,
        },
    "torch": {
        "image": torch_image,
        "stack": 999,
        "food": False,
        "build": True,
        "tool": False,
        "furniture": True,
        },
    "coal": {
        "image": coal_item,
        "stack": 999,
        "food": False,
        "build": False,
        "tool": False,
        },
    "plank wall": {
        "image": plank_wall,
        "stack": 999,
        "food": False,
        "build": True,
        "tool": False,
        "furniture": True,
        },
    "tree1": {
        "image": tree_images[0],
        "stack": 999,
        "food": False,
        "build": False,
        "tool": False,
        "furniture": False,
        },
    "tree2": {
        "image": tree_images[1],
        "stack": 999,
        "food": False,
        "build": False,
        "tool": False,
        "furniture": False,
        },
    "tree3": {
        "image": tree_images[2],
        "stack": 999,
        "food": False,
        "build": False,
        "tool": False,
        "furniture": False,
        },
    "tree4": {
        "image": tree_images[3],
        "stack": 999,
        "food": False,
        "build": False,
        "tool": False,
        "furniture": False,
        },
    "flag": {
        "image": flag_image,
        "stack": 999,
        "food": False,
        "build": False,
        "tool": False,
        "furniture": False,
        },
}

CRAFTING_REQUIREMENTS = {
    "plank wall": [
        ["plank", 2],
    ],
    "pickaxe": [
        ["plank", 3],
        ["rock", 3]
    ],
    "axe": [
        ["plank", 3],
        ["rock", 3]
    ],
    "shovel": [
        ["plank", 3],
        ["rock", 3]
    ],
    "torch": [
        ["plank", 1],
        ["coal", 1]
    ],
    "slab": [
        ["plank", 3],
    ],
    "hoe": [
        ["plank", 3],
        ["stone", 3],
    ],
}
