import pygame
from settings import *

# directories
music_dir = "src/music/"
images_dir = "src/images/"

# music and sounds
pygame.mixer.init()
pygame.mixer.music.set_volume(0.5)


pygame.mixer.music.load(f"{music_dir}oyho.ogg")
jump_sound = pygame.mixer.Sound(f"{music_dir}jump.wav")
throw_sound = pygame.mixer.Sound(f"{music_dir}throw.wav")
hurt_sound = pygame.mixer.Sound(f"{music_dir}hurt.wav")
break_sound = pygame.mixer.Sound(f"{music_dir}break.wav")
death_sound = pygame.mixer.Sound(f"{music_dir}death.wav")
build_sound = pygame.mixer.Sound(f"{music_dir}build.wav")

# player images
player_image1 = pygame.image.load(f"{images_dir}player1.png").convert()
player_image2 = pygame.image.load(f"{images_dir}player2.png").convert()
player_image1.set_colorkey(GREEN)
player_image2.set_colorkey(GREEN)
player_images = [player_image1, player_image2]

# tile images
grasstile = pygame.image.load(f"{images_dir}tiles/grass.png").convert()
snowy_grass = pygame.image.load(f"{images_dir}tiles/snowy_grass.png").convert()
rocktile = pygame.image.load(f"{images_dir}tiles/rock.png").convert()
stonetile = pygame.image.load(f"{images_dir}tiles/stone.png").convert()
dirttile = pygame.image.load(f"{images_dir}tiles/dirt.png").convert()
planktile = pygame.image.load(f"{images_dir}tiles/plank.png").convert()
coaltile = pygame.image.load(f"{images_dir}tiles/coaltile.png").convert()
plank_wall = pygame.image.load(f"{images_dir}tiles/plank_wall.png").convert()
plant_image = pygame.image.load(f"{images_dir}tiles/plant.png").convert()
plant_image.set_colorkey((255, 255, 255))

# tools
hammer_image = pygame.image.load(f"{images_dir}hammer.png").convert()
hammer_image.set_colorkey(WHITE)
pick_image = pygame.image.load(f"{images_dir}pickaxe.png").convert()
pick_image.set_colorkey(WHITE)
shovel_image = pygame.image.load(f"{images_dir}spade.png").convert()
shovel_image.set_colorkey(WHITE)
axe_image = pygame.image.load(f"{images_dir}axe.png").convert()
axe_image.set_colorkey(WHITE)
hoe_image = pygame.image.load(f"{images_dir}hoe.png").convert()
hoe_image.set_colorkey(WHITE)


# others
select_arrow = pygame.image.load(f"{images_dir}select_arrow.png")
select_arrow.set_colorkey(WHITE)
sapling_image = pygame.image.load(f"{images_dir}sapling.png").convert()
sapling_image.set_colorkey(WHITE)
slab_image = pygame.image.load(f"{images_dir}slab.png").convert()
slab_image.set_colorkey(WHITE)
coal_item = pygame.image.load(f"{images_dir}coal.png").convert()
coal_item.set_colorkey(WHITE)
arrow_image = pygame.image.load(f"{images_dir}arrow.png").convert()
arrow_image.set_colorkey(WHITE)
torch_image = pygame.image.load(f"{images_dir}torch.png").convert()
torch_image.set_colorkey(WHITE)
meat_image = pygame.image.load(f"{images_dir}meat.png").convert()
meat_image.set_colorkey(GREEN)
worm_head = pygame.image.load(f"{images_dir}worm/head.png").convert()
worm_head.set_colorkey(WHITE)
worm_body = pygame.image.load(f"{images_dir}worm/body.png").convert()
worm_body.set_colorkey(WHITE)
worm_tail = pygame.image.load(f"{images_dir}worm/tail.png").convert()
worm_tail.set_colorkey(WHITE)
background_image = pygame.transform.scale(pygame.image.load(f"{images_dir}background.png").convert(), (DISPLAY_WIDTH, DISPLAY_HEIGHT))
night_background_image = pygame.transform.scale(pygame.image.load(f"{images_dir}background_night.png").convert(), (DISPLAY_WIDTH, DISPLAY_HEIGHT))

polarbear_images = []
for i in range(0, 12):
    polarbear_image = pygame.transform.scale(pygame.image.load("{}polarbear/{}.png".format(images_dir, i)), (32, 32))
    polarbear_images.append(polarbear_image)

skeleton_images = []
for i in range(1, 3):
    image = pygame.image.load("{}skeleton/skeleton{}.png".format(images_dir, str(i)))
    image.set_colorkey(GREEN)
    skeleton_images.append(image)

crow_images = []
for i in range(1, 4):
    crow = pygame.transform.scale(pygame.image.load("{}crow/{}.png".format(images_dir, i)), (16, 16))
    crow_images.append(crow)

tree_images = []
for i in range(1,5):
    tree_image = pygame.image.load("{}trees/tree{}.png".format(images_dir, i)).convert()
    tree_image.set_colorkey((255, 255, 255))
    tree_images.append(tree_image)

explosion_images = []
for i in range(0, 9):

    explosion_image = pygame.image.load("{}explosion/{}.png".format(images_dir, i)).convert()
    explosion_image.set_colorkey((229, 229, 229))
    explosion_images.append(explosion_image)





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
