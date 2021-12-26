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
This file contains standalone functions that don't fit anywhere else
"""

import pygame
from settings import WHITE, BLACK, BLUE, FONT, TILE_SIZE, CHUNK_SIZE, RED, GREEN

def print_text(text, x, y, display, allignment=0, size=32, color=BLACK): # pragma: no cover
    """
    Draws text onto the screen
    allignments: 0=left, 1=center, 2=right
    Args:
        text
        x
        y
        display: surface to draw on
        allignment: 0=left, 1=center, 2=right (default=0)
        size: font size
        color: text color
    """
    font = pygame.font.SysFont(FONT, size)
    surf = font.render(text, False, color)
    if allignment == 1:
        x = x - surf.get_width() / 2
    elif allignment == 2:
        x = x - surf.get_width()
    display.blit(surf, (x, y))

def move(entity, world, entity_collisions=False, falling=False):
    """
    Moves an entity while checking for collisions.

    Args:
        entity: Object with a pygame rect, collisions and dx/dy attributes
        world: World object
        entity_collisions: Should collisions be checked with entities
    """

    collisions = {
            "right": False,
            "left": False,
            "up": False,
            "down": False,
            }
    # move horizontally and check for collisions
    entity.rect.x += entity.dx
    for tile in world.tiles:
        if entity.rect.colliderect(tile):
            if not tile in world.slabs:
                if entity.dx > 0:
                    entity.rect.right = tile.left
                    collisions["right"] = True
                if entity.dx < 0:
                    entity.rect.left = tile.right
                    collisions["left"] = True
    if entity_collisions:
        for w_entity in world.entities:
            if not w_entity.rect == entity.rect:
                if w_entity.rect.colliderect(entity.rect):
                    #entity.rect.x -= entity.dx
                    if entity.rect.centerx < w_entity.rect.centerx:
                        entity.dx -= 2
                        w_entity.dx += 2
                    else:
                        entity.dx += 2
                        w_entity.dx -= 2
    # move vertically and check for collisions
    entity.rect.y += entity.dy
    for tile in world.tiles:
        if entity.rect.colliderect(tile):
            if entity.dy > 0:
                if falling and tile in world.slabs:
                    pass
                else:
                    entity.rect.bottom = tile.top
                    collisions["down"] = True
            if entity.dy < 0:
                if not tile in world.slabs:
                    entity.rect.top = tile.bottom
                    collisions["up"] = True

    entity.collisions = collisions

def chunk_debug(pos, display, world): # pragma: no cover
    """
    Shows chunk borders, biomes and other debug information
    """
    mousex = pos[0]
    mousey = pos[1]
    for chunk in world.game_map.keys():
        chunkx, chunky = chunk.split(";")
        chunkx = int(chunkx) * TILE_SIZE * CHUNK_SIZE
        chunky = int(chunky) * TILE_SIZE * CHUNK_SIZE
        chunkrect = pygame.Rect(chunkx, chunky, 8*TILE_SIZE, 8*TILE_SIZE)
        if chunkrect.collidepoint(mousex, mousey):
            chunkrect.x -= world.scrollx
            chunkrect.y -= world.scrolly
            if world.game_map[chunk][1] == 1:
                biome = "Forest"
            elif world.game_map[chunk][1] == 2:
                biome = "Tundra"
            elif world.game_map[chunk][1] == 3:
                biome = "Underworld"
            else:
                biome = world.game_map[chunk][1]
            chunkname = chunk.replace(";", ", ")
            color = BLACK
            if world.current_biome == 3:
                color = WHITE
            print_text("biome: {}".format(biome), chunkrect.x, chunkrect.y, display, 0, 16, color)
            print_text("chunk: {}".format(chunkname), chunkrect.x, chunkrect.y + 16, display, 0, 16, color)
            for tile in world.game_map[chunk][0]:
                drawrect = pygame.Rect(tile[0][0]*TILE_SIZE-world.scrollx,
                                       tile[0][1]*TILE_SIZE-world.scrolly, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(display, BLUE, drawrect, 1)
        else:
            chunkrect.x -= world.scrollx
            chunkrect.y -= world.scrolly
            pygame.draw.rect(display, RED, chunkrect, 1)

def draw_health_bar(health_x, health_y, display, health, max_health): # pragma: no cover
    """
    Draws a health bar showing health in green and lost health in red
    Args:
        health_x: x coord of the *center* of the health bar
        health_y: y coord of the health bar
        display: surf to draw the health bar
        health
        max_health
    """
    health_x -= max_health // 2
    if health < max_health:
        for x in range(health):
            pygame.draw.line(display, GREEN, (health_x + x, health_y),
                             (health_x + x, health_y+2), 1)
        health_x += health
        for x in range(max_health - health):
            pygame.draw.line(display, RED, (health_x + x, health_y), (health_x + x, health_y+2), 1)
