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

import math
import pygame
from numpy import random
from resources import polarbear_images, zombie_walking, skeleton_walking
from entities.drop import DroppedItem
from entities.particle import Particle
from entities.arrow import Arrow
from settings import TILE_SIZE, DISPLAY_WIDTH, DISPLAY_HEIGHT, GREEN, RED
from functions import move, draw_health_bar

class WalkingMob():
    """
    Class for a mob that tries to walk towards the player and cause damage
    the mobtype parameter allows for adding other mobs with the same "AI",
    but different textures.
    """
    def __init__(self, x, y, mobtype="bear"):
        self.images = polarbear_images
        self.animation_repeat = 10
        if mobtype == "skeleton":
            self.images = skeleton_walking
            self.anim_repeat = 15
            self.arrow_counter = 0
        if mobtype == "zombie":
            self.images = zombie_walking
            self.anim_repeat = 15
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.mobtype = mobtype # makes retextured mobs with same logic possible
        self.invert = 0 # which way the mob is facing

        self.image_index = 0
        self.animation_counter = 0

        self.aggroed = False
        self.speed = 1
        self.max_speed = 3
        self.dx = 0
        self.dy = 0
        self.jumppower = 7
        self.jumps = 1
        self.gravity = 0.4
        self.max_gravity = 8

        self.max_health = 50
        self.health = self.max_health

        self.collisions = {
            "right": False,
            "left": False,
            "up": False,
            "down": False,
            }

    def update(self, player, world):
        """
        Updates the WalkingMob object, handling things like movement, health and aggression
        to the player
        """
        if abs(self.rect.x - player.rect.x) > 700 or abs(self.rect.y < player.rect.y) > 700:
            world.mobs.remove(self)
            world.entities.remove(self)

        if self.health <= 0:
            # blood particles
            for i in range(40):
                world.particles.append(Particle(self.rect.centerx, self.rect.centery, RED))
            # drops
            drops = []
            if self.mobtype == "zombie":
                drop_rng = random.randint(1, 6)
                if drop_rng in [1, 2]:
                    drops.append(("meat", random.randint(1, 3)))
                elif drop_rng == 3:
                    drops.append(("arrow", random.randint(1, 3)))
                elif drop_rng == 4:
                    drops.append(("stick", random.randint(1, 3)))
                elif drop_rng == 5:
                    drops.append(("string", random.randint(1, 3)))
                elif drop_rng == 6:
                    drops.append(("rock", random.randint(1, 3)))
            elif self.mobtype == "skeleton":
                drop_rng = random.randint(1, 3)
                if drop_rng == 1:
                    drops.append(("arrow", random.randint(1, 10)))
                elif drop_rng == 2:
                    drops.append(("stick", random.randint(1, 3)))
                elif drop_rng == 3:
                    drops.append(("string", random.randint(1, 3)))
            else:
                drops.append(("meat", random.randint(1, 3)))
            for drop in drops:
                world.drops.append(DroppedItem(self.rect.x, self.rect.y,
                                   self.dx//2, self.dy//2, drop[0], drop[1]))

            world.mobs.remove(self)
            world.entities.remove(self)

        if self.mobtype == "skeleton":
            # shooting arrows
            if self.arrow_counter <= 0:
                if abs(self.rect.x - player.rect.x) < 10 * TILE_SIZE:
                    self.shoot(world, player.rect.x, player.rect.y)
                    self.arrow_counter = 150
            else:
                self.arrow_counter -= 1


        # animation
        self.animation_counter += 1
        if self.animation_counter == self.animation_repeat:
            self.animation_counter = 0
            self.image_index += 1
            if self.image_index > len(self.images) - 1:
                self.image_index = 0
            self.image = self.images[self.image_index]

        # aggro to player
        if self.rect.right > world.scrollx or self.rect.left < DISPLAY_WIDTH + world.scrollx:
            self.aggroed = True
        self.move(player, world)

    def shoot(self, world, x, y): # pragma: no cover
        """
        Shoot an arrow towards (x, y)
        """
        distance_x = x - self.rect.x
        distance_y = y - self.rect.y - abs(distance_x)//3

        angle = math.atan2(distance_y, distance_x)
        speed_x = 5 * math.cos(angle)
        speed_y = 5 * math.sin(angle)
        arrow = Arrow(self.rect.centerx, self.rect.centery, speed_x, speed_y, True)
        world.arrows.append(arrow)

    def move(self, player, world):
        """
        Moves towards the x coordinate of the player and jumps when encountering obsticles.
        """
        # movement
        if self.mobtype == "skeleton":
            target_offset = TILE_SIZE * 5
        else:
            target_offset = TILE_SIZE
        if self.rect.centerx < player.rect.centerx - target_offset:
            if self.dx < self.speed:
                self.dx += 0.5
        elif self.rect.centerx > player.rect.centerx + target_offset:
            if self.dx > -self.speed:
                self.dx -= 0.5
        # hard speed gap
        if self.dx > self.max_speed:
            self.dx = self.max_speed
        if self.dx < -self.max_speed:
            self.dx = -self.max_speed

        # soft speed gap
        if self.dx > self.speed:
            self.dx -= 0.1
        if self.dx < -self.speed:
            self.dx += 0.1

        # set invert
        if self.rect.x < player.rect.x:
            if self.mobtype == "bear":
                self.invert = 1
            else:
                self.invert = 0
        else:
            if self.mobtype == "bear":
                self.invert = 0
            else:
                self.invert = 1

        move(self, world, True)

        if self.collisions["left"] or self.collisions["right"]:
            if self.jumps:
                self.dy = -self.jumppower
                self.jumps = 0

        if self.collisions["down"]: # gravity
            self.dy = 0
            self.jumps = 1
        else:
            if (self.rect.y-world.scrolly) < DISPLAY_HEIGHT:
                if self.dy < self.max_gravity:
                    self.dy += self.gravity

    def draw(self, display, world): # pragma: no cover
        """
        Draws the mob and a health bar if it has taken damage
        """
        drawx = self.rect.x-world.scrollx
        drawy = self.rect.y-world.scrolly

        # flip the image if needed and make it transparent
        image = pygame.transform.flip(self.image, self.invert, 0)
        image.set_colorkey(GREEN)
        display.blit(image, (drawx, drawy))

        draw_health_bar(self.rect.centerx-world.scrollx, self.rect.y-TILE_SIZE-world.scrolly,
                        display, self.health, self.max_health)
