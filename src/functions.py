import noise
import random
import pygame
from settings import *

# modifiers for how fast the algorythm goes through the noise pattern
noise_speed = 0.05
cave_noise_speed = 0.07
cave_noise_multiplier = 30

def generate_chunk(x,y,seed):
    """
    generate_chunk generates a list of tiles with their coordinates and types

    Args:
        x: x chunk coord
        y: y chunk coord
        seed: offset to the noise x coord

    Returns:
        [[[tilex, tiley], tiletype], [[tilex, tiley], tiletype]]

    """

    # variation in noise multiplayer to create variating
    # height differences in the game world
    noise_multiplier = (noise.pnoise1((x + seed) * 0.01, repeat=99999999) + 1) * 20
    heat_map = int(round(noise.pnoise1((x + seed) * 0.01, repeat=99999999) * noise_multiplier))
    # setting biome based on heat map
    # 1: Forest, 2: Tundra, 3: Underground
    if heat_map < 0:
        biome = 2
    else:
        biome = 1

    chunk_data = [[], biome]
    for x_pos in range(CHUNK_SIZE):
        for y_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0

            plant_map = noise.pnoise1((target_x + seed) * 0.4, repeat=99999999, persistence=2) * noise_multiplier
            caveheight = int(round(noise.pnoise2((target_x + seed) * cave_noise_speed, (target_y) * cave_noise_speed, repeatx=99999999, repeaty=99999999) * cave_noise_multiplier))
            height = int(round(noise.pnoise1((target_x + seed) * noise_speed, repeat=99999999) * noise_multiplier))

            # cave generation
            if target_y > 29 - height:
                chunk_data[1] = 3
                if caveheight < 3:
                    tile_type = "stone"
                    if caveheight < -15:
                        tile_type = "coal block"

            # dirt
            if target_y > 8 - height and target_y < 30 - height:
                tile_type = "dirt"
            # grass
            elif target_y == 8 - height:
                if biome == 1:
                    tile_type = "grass"
                elif biome == 2:
                    tile_type = "snowy grass"

            elif target_y == 7 - height:
                # plants

                    if plant_map < 0:
                        if biome == 1:
                            tile_type = "plant"
                    # trees
                    if plant_map > 0:
                        if biome == 1:
                            if plant_map < 3:
                                tile_type = "tree1"
                            elif plant_map < 6:
                                tile_type = "tree2"
                            elif plant_map < 10:
                                tile_type = "tree3"
                        elif biome == 2:
                            if 5 < plant_map < 10:
                                tile_type = "tree4"
                    # flags
                    if plant_map == 10:
                        tile_type = "flag"
            if tile_type != 0:
                chunk_data[0].append([[target_x,target_y],tile_type])
    return chunk_data


def move(rect, dx, dy, tiles, slabs=[], entities=[]):
    """Moves a pygame rectangle

    Args:
        rect, tiles, dx, dy, slabs=[], entities=[]
    Returns:
        rect, collisions

    """

    collisions = {
            "right": False,
            "left": False,
            "up": False,
            "down": False,
            }
    rect.x += dx
    for tile in tiles:
        if rect.colliderect(tile):
            if not tile in slabs:
                if dx > 0:
                    rect.right = tile.left
                    collisions["right"] = True
                if dx < 0:
                    rect.left = tile.right
                    collisions["left"] = True
    for entity in entities:
        if rect.colliderect(entity):
            if dx > 0:
                rect.x -= dx
            if dx < 0:
                rect.y += dx

    rect.y += dy
    for tile in tiles:
        if rect.colliderect(tile):
            if dy > 0:
                rect.bottom = tile.top
                collisions["down"] = True
            if dy < 0:
                if not tile in slabs:
                    rect.top = tile.bottom
                    collisions["up"] = True

    return rect, collisions
