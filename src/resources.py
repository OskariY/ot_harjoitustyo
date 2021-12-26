#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Northlands is a 2D survival game inspired by games like Minecraft, Terriaria and Valheim
# Copyright (C) 2021 Oskari Ylönen [oskari@ylonen.org]
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of  MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
"""
This file loads all the required images and sounds to memory as well as containing
the ITEMS index dictionary and "recepies" for crafing
"""

import random
import os
import pygame
from settings import GREEN, WHITE, DISPLAY_WIDTH, DISPLAY_HEIGHT, TILE_SIZE, MUSIC

# directories
MUSIC_DIR = "resources/music/"
IMAGES_DIR = "resources/images/"

# music and sounds
pygame.mixer.init()

# songs
sound_names = os.listdir(f"{MUSIC_DIR}")
songs = []
random.shuffle(sound_names)
for song in sound_names:
    if song.endswith(".mp3"):
        if songs == [] and MUSIC:
            pygame.mixer.music.load(f"{MUSIC_DIR}{song}")
            pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
            pygame.mixer.music.play()
        songs.append(f"{MUSIC_DIR}{song}")

# sound effects
jump_sound = pygame.mixer.Sound(f"{MUSIC_DIR}jump.wav")
throw_sound = pygame.mixer.Sound(f"{MUSIC_DIR}throw.wav")
hurt_sound = pygame.mixer.Sound(f"{MUSIC_DIR}hurt.wav")
break_sound = pygame.mixer.Sound(f"{MUSIC_DIR}break.wav")
death_sound = pygame.mixer.Sound(f"{MUSIC_DIR}death.wav")
build_sound = pygame.mixer.Sound(f"{MUSIC_DIR}build.wav")

# lighting
evening = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), flags=pygame.SRCALPHA)
evening.fill((50, 50, 10))
morning = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), flags=pygame.SRCALPHA)
morning.fill((5, 30, 30))
night = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), flags=pygame.SRCALPHA)
night.fill((60, 60, 20))
darkness = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), flags=pygame.SRCALPHA)
darkness.fill((50, 50, 50))
dark = False
glowradius = 128
glow = pygame.Surface((glowradius*2, glowradius*2), flags=pygame.SRCALPHA)
glowcolor = pygame.Surface((glowradius*2, glowradius*2), flags=pygame.SRCALPHA)
glowcolor.set_colorkey((0, 0, 0))
for i in range(glowradius // 8):
    pygame.draw.circle(glowcolor, ((2+i)*4, (2+i)*4, (1+i)*4), (glowradius, glowradius), glowradius-i*8)
glow.blit(glowcolor, (0, 0), special_flags=pygame.BLEND_RGB_ADD)


# player images
player_standing = pygame.image.load(f"{IMAGES_DIR}/player/standing.png").convert()
player_standing.set_colorkey(GREEN)
player_hand_straight = pygame.image.load(f"{IMAGES_DIR}/player/straight_hand.png").convert()
player_hand_straight.set_colorkey(GREEN)
player_hand = pygame.image.load(f"{IMAGES_DIR}/player/hand.png").convert()
player_hand.set_colorkey(GREEN)
player_walking = []
for image_name in os.listdir(f"{IMAGES_DIR}/player/"):
    if image_name.startswith("walking"):
        img = pygame.image.load(f"{IMAGES_DIR}/player/{image_name}").convert()
        img.set_colorkey(GREEN)
        player_walking.append(img)

# tile images
grasstile = pygame.image.load(f"{IMAGES_DIR}tiles/grass.png").convert()
snowy_grass = pygame.image.load(f"{IMAGES_DIR}tiles/snowy_grass.png").convert()
rocktile = pygame.image.load(f"{IMAGES_DIR}tiles/rock.png").convert()
stonetile = pygame.image.load(f"{IMAGES_DIR}tiles/stone.png").convert()
dirttile = pygame.image.load(f"{IMAGES_DIR}tiles/dirt.png").convert()
planktile = pygame.image.load(f"{IMAGES_DIR}tiles/plank.png").convert()
coaltile = pygame.image.load(f"{IMAGES_DIR}tiles/coaltile.png").convert()
plank_wall = pygame.image.load(f"{IMAGES_DIR}tiles/plank_wall.png").convert()
plant_image = pygame.image.load(f"{IMAGES_DIR}tiles/plant.png").convert()
plant_image.set_colorkey((255, 255, 255))

# tools
hammer_image = pygame.image.load(f"{IMAGES_DIR}hammer.png").convert()
hammer_image.set_colorkey(WHITE)
pick_image = pygame.image.load(f"{IMAGES_DIR}pickaxe.png").convert()
pick_image.set_colorkey(WHITE)
shovel_image = pygame.image.load(f"{IMAGES_DIR}spade.png").convert()
shovel_image.set_colorkey(WHITE)
axe_image = pygame.image.load(f"{IMAGES_DIR}axe.png").convert()
axe_image.set_colorkey(WHITE)
hoe_image = pygame.image.load(f"{IMAGES_DIR}hoe.png").convert()
hoe_image.set_colorkey(WHITE)


# others
bow_image = pygame.image.load(f"{IMAGES_DIR}bow.png")
bow_image.set_colorkey(GREEN)
select_arrow = pygame.image.load(f"{IMAGES_DIR}select_arrow.png")
select_arrow.set_colorkey(WHITE)
sapling_image = pygame.image.load(f"{IMAGES_DIR}sapling.png").convert()
sapling_image.set_colorkey(WHITE)
slab_image = pygame.image.load(f"{IMAGES_DIR}slab.png").convert()
slab_image.set_colorkey(WHITE)
coal_item = pygame.image.load(f"{IMAGES_DIR}coal.png").convert()
coal_item.set_colorkey(WHITE)
arrow_image = pygame.image.load(f"{IMAGES_DIR}arrow.png").convert()
arrow_image.set_colorkey(GREEN)
arrow_tip_image = pygame.image.load(f"{IMAGES_DIR}arrow_tip.png").convert()
arrow_tip_image.set_colorkey(GREEN)
string_image = pygame.image.load(f"{IMAGES_DIR}string.png").convert()
string_image.set_colorkey(GREEN)
stick_image = pygame.image.load(f"{IMAGES_DIR}stick.png").convert()
stick_image.set_colorkey(GREEN)
torch_image = pygame.image.load(f"{IMAGES_DIR}torch.png").convert()
torch_image.set_colorkey(WHITE)
tonttulakki = pygame.image.load(f"{IMAGES_DIR}tonttulakki.png").convert()
tonttulakki.set_colorkey(GREEN)
meat_image = pygame.image.load(f"{IMAGES_DIR}meat.png").convert()
meat_image.set_colorkey(GREEN)
worm_head = pygame.image.load(f"{IMAGES_DIR}worm/head.png").convert()
worm_head.set_colorkey(WHITE)
worm_body = pygame.image.load(f"{IMAGES_DIR}worm/body.png").convert()
worm_body.set_colorkey(WHITE)
worm_tail = pygame.image.load(f"{IMAGES_DIR}worm/tail.png").convert()
worm_tail.set_colorkey(WHITE)
background_image = pygame.transform.scale(pygame.image.load(f"{IMAGES_DIR}background.png").convert(), (DISPLAY_WIDTH, DISPLAY_HEIGHT))
night_background_image = pygame.transform.scale(pygame.image.load(f"{IMAGES_DIR}background_night.png").convert(), (DISPLAY_WIDTH, DISPLAY_HEIGHT))

polarbear_images = []
for i in range(0, 12):
    polarbear_image = pygame.transform.scale(
            pygame.image.load("{}polarbear/{}.png".format(IMAGES_DIR, i)), (2*TILE_SIZE, 2*TILE_SIZE)
            )
    polarbear_images.append(polarbear_image)

zombie_walking = []
for i in range(1, 4):
    image = pygame.image.load("{}zombie/zombie_walking{}.png".format(IMAGES_DIR, str(i))).convert()
    image.set_colorkey(GREEN)
    zombie_walking.append(image)

skeleton_walking = []
for i in range(1, 4):
    image = pygame.image.load("{}skeleton/walking{}.png".format(IMAGES_DIR, str(i))).convert()
    image.set_colorkey(GREEN)
    skeleton_walking.append(image)

crow_images = []
for i in range(1, 4):
    crow = pygame.transform.scale(pygame.image.load("{}crow/{}.png".format(IMAGES_DIR, i)), (16, 16))
    crow_images.append(crow)

tree_images = []
for i in range(1,5):
    tree_image = pygame.image.load("{}trees/tree{}.png".format(IMAGES_DIR, i)).convert()
    tree_image.set_colorkey((255, 255, 255))
    tree_images.append(tree_image)

explosion_images = []
for i in range(0, 9):

    explosion_image = pygame.image.load("{}explosion/{}.png".format(IMAGES_DIR, i)).convert()
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
    "hammer": {
        "image": hammer_image,
        "stack": 1,
        "food": False,
        "build": False,
        "tool":  True,
        },
    "bow": {
        "image": bow_image,
        "stack": 1,
        "food": False,
        "build": False,
        "tool":  True,
        },
    "arrow": {
        "image": arrow_image,
        "stack": 999,
        "food": False,
        "build": False,
        "tool": False,
        },
    "arrow tip": {
        "image": arrow_tip_image,
        "stack": 999,
        "food": False,
        "build": False,
        "tool": False,
        },
    "stick": {
        "image": stick_image,
        "stack": 999,
        "food": False,
        "build": False,
        "tool": False,
        },
    "string": {
        "image": string_image,
        "stack": 999,
        "food": False,
        "build": False,
        "tool": False,
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
    "sapling": {
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
    "plank wall": {
        "amount": 1,
        "requirements": [
            ("plank", 2),
            ]
    },
    "slab": {
        "amount": 1,
        "requirements": [
            ("plank", 2),
            ]
    },
    "pickaxe": {
        "amount": 1,
        "requirements": [
            ("plank", 3),
            ("rock", 3),
            ]
    },
    "shovel": {
        "amount": 1,
        "requirements": [
            ("plank", 3),
            ("rock", 3),
            ]
    },
    "axe": {
        "amount": 1,
        "requirements": [
            ("plank", 3),
            ("rock", 3),
            ]
    },
    "torch": {
        "amount": 1,
        "requirements": [
            ("stick", 1),
            ("coal", 1),
            ]
    },
    "stick": {
        "amount": 10,
        "requirements": [
            ("plank", 1),
            ]
    },
    "arrow tip": {
        "amount": 10,
        "requirements": [
            ("rock", 1),
            ]
    },
    "arrow": {
        "amount": 10,
        "requirements": [
            ("arrow tip", 10),
            ("stick", 10),
            ]
    },
    "string": {
        "amount": 1,
        "requirements": [
            ("plant", 2),
            ]
    },
    "bow": {
        "amount": 1,
        "requirements": [
            ("stick", 10),
            ("string", 3),
            ]
    },
}
