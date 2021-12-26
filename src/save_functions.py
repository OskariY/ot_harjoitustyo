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
This file contains all the functions related to saving and loading the game
"""

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
        "tod": world.tod,

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
        "tod": 0,

        # world generation parameters
        "seed": random.randint(-9999999,9999999),
    }
    write_game_data(name, game_data)

