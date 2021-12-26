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
Contains constants used by the game like colors and display variables
"""

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
