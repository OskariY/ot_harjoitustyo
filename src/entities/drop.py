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

import pygame
from settings import DISPLAY_WIDTH, DISPLAY_HEIGHT, TILE_SIZE
from resources import ITEMS
from functions import move

class DroppedItem():
    """
    Object for drops that can be picked up by the player
    """

    def __init__(self, x, y, dx, dy, item, amount=1):
        self.image = ITEMS[item]["image"]
        if item in ["arrow", "stick", "arrow tip"]:
            size = TILE_SIZE
        else:
            size = TILE_SIZE - 4

        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = pygame.Rect(x, y, TILE_SIZE - 4, TILE_SIZE - 4)
        self.item = item
        self.dx = dx
        self.dy = dy
        self.gravity = 0.4
        self.amount = amount
        self.collisions = {
            "right": False,
            "left": False,
            "up": False,
            "down": False,
        }

    def update(self, world):
        """
        Updates the drop position based on its gravity and dx/dy values if it's
        not outside the screen
        """
        # only update movement if drop is in the screen
        # prevents them from falling off the map
        if self.rect.x - world.scrollx > 0 \
                and self.rect.x - world.scrollx < DISPLAY_WIDTH \
                and self.rect.y - world.scrolly > 0 \
                and self.rect.y - world.scrolly < DISPLAY_HEIGHT:
            move(self, world)
            if self.collisions["down"]:
                self.dy = 0
                self.dx = 0
            else:
                self.dy += self.gravity

            if self.collisions["left"] or self.collisions["right"]:
                self.dx = 0

    def draw(self, display, scrollx, scrolly): # pragma: no cover
        """
        Draws the drop
        """
        display.blit(self.image, (self.rect.x - scrollx, self.rect.y - scrolly))
