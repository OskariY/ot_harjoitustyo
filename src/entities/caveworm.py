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
# this program.  If not, see <http://www.gnu.org/licenses/>

import math
import noise
import random
import pygame
from settings import TILE_SIZE, RED
from entities.particle import Particle
from entities.drop import DroppedItem
from resources import worm_head, worm_body, worm_tail
from functions import draw_health_bar

class Worm():
    """
    Caveworm object
    the worm is made up of three types of rects: the head, body (list of rects) and the tail
    """
    def __init__(self, x, y):
        # differences between drawn images and rects
        # this is necesseary to remove gaps between the different worm parts
        # that would otherwise form
        self.margin = 4
        # head
        self.head_rect = pygame.Rect(x, y, TILE_SIZE - self.margin, TILE_SIZE - self.margin)
        self.head_image = worm_head
        self.head_angle = math.radians(-90)

        # body
        self.body_rects = []
        self.body_images = []
        self.body_angles = []
        for i in range(7):
            y += TILE_SIZE
            self.body_images.append(worm_body)
            self.body_rects.append(pygame.Rect(x, y, TILE_SIZE - self.margin,
                                   TILE_SIZE - self.margin))
            self.body_angles.append(math.radians(-90))

        # tail
        self.tail_rect = pygame.Rect(x, y+TILE_SIZE, TILE_SIZE - self.margin,
                                     TILE_SIZE - self.margin)
        self.tail_image = worm_tail
        self.tail_angle = math.radians(-90)

        self.speed = 2
        self.body_speed = self.speed + 1
        self.aggroed = False
        self.target = None
        self.direction = "right"
        self.max_health = 100
        self.health = self.max_health

    def move(self, target_x, target_y):
        """
        Move the head towards the target and the other parts towards the part preceding them
        """
        # head movement
        distance_x = target_x - self.head_rect.x
        distance_y = target_y - self.head_rect.y
        self.head_angle = math.atan2(distance_y, distance_x)
        speed_x = self.speed * math.cos(self.head_angle)
        speed_y = self.speed * math.sin(self.head_angle)
        self.head_rect.x += round(speed_x)
        self.head_rect.y += round(speed_y)
        if speed_x > 0:
            self.direction = "right"
        else:
            self.direction = "left"

        # body movement
        for i, body in enumerate(self.body_rects):
            if i == 0:
                distance_x = self.head_rect.x - body.x
                distance_y = self.head_rect.y - body.y
            else:
                distance_x = self.body_rects[i-1].x - body.x
                distance_y =self.body_rects[i-1].y - body.y
            self.body_angles[i] = math.atan2(distance_y, distance_x)
            speed_x = self.body_speed * math.cos(self.body_angles[i])
            speed_y = self.body_speed * math.sin(self.body_angles[i])
            if i == 0:
                if not body.colliderect(self.head_rect):
                    body.x += round(speed_x)
                    body.y += round(speed_y)
            else:
                if not body.colliderect(self.body_rects[i-1]):
                    body.x += round(speed_x)
                    body.y += round(speed_y)

        # tail movement
        distance_x = self.body_rects[-1].x - self.tail_rect.x
        distance_y = self.body_rects[-1].y - self.tail_rect.y
        self.tail_angle = math.atan2(distance_y, distance_x)
        speed_x = self.body_speed * math.cos(self.tail_angle)
        speed_y = self.body_speed * math.sin(self.tail_angle)
        if not self.tail_rect.colliderect(self.body_rects[-1]):
            self.tail_rect.x += round(speed_x)
            self.tail_rect.y += round(speed_y)

    def update(self, player, world):
        """
        Update cave worm object and call the move method
        """
        # despawn if player is too far
        if abs(player.rect.x - self.head_rect.x) > 500 \
                or abs(player.rect.y - self.head_rect.y) > 500:
            world.worms.remove(self)
        # death
        if self.health <= 0:
            world.drops.append(DroppedItem(self.head_rect.centerx, self.head_rect.centery,
                                           0, 0, "meat", random.randint(1, 10)))
            for i in range(100):
                world.particles.append(Particle(self.head_rect.centerx,
                                       self.head_rect.centery, RED))
            world.worms.remove(self)

        # check for collisions with the player
        if self.head_rect.colliderect(player.rect):
            player.health -= 5
            if self.direction == "right":
                player.dx += 10
                player.dy -= 5
            else:
                player.dx -= 10
                player.dy -= 5

        if self.aggroed:
            if world.current_biome != 3:
                self.aggroed = False
                self.target = None

            if self.target is not None:
                self.move(self.target.rect.x, self.target.rect.y)
        else:
            if world.current_biome == 3 and abs(player.rect.x - self.head_rect.x) < 300:
                self.target = player
                self.aggroed = True
            flee_x = self.head_rect.x + (noise.pnoise1(self.head_rect.y * 0.05,
                                                       repeat=99999999) + 1) * 20
            self.move(flee_x, 2000)

    def draw(self, display, scrollx, scrolly): # pragma: no cover
        """
        Draws all the worm parts
        """
        display.blit(pygame.transform.rotate(self.head_image, math.degrees(-self.head_angle) - 90),
                     (self.head_rect.x-scrollx-self.margin//2,
                      self.head_rect.y-scrolly-self.margin//2))
        for i, image in enumerate(self.body_images):
            display.blit(pygame.transform.rotate(image, math.degrees(-self.body_angles[i]) - 90),
                         (self.body_rects[i].x - scrollx-self.margin//2,
                          self.body_rects[i].y - scrolly-self.margin//2))
        display.blit(pygame.transform.rotate(self.tail_image, math.degrees(-self.tail_angle) - 90),
                     (self.tail_rect.x - scrollx-self.margin//2,
                      self.tail_rect.y - scrolly-self.margin//2))
        draw_health_bar(self.head_rect.centerx-scrollx, self.head_rect.y-TILE_SIZE*2-scrolly,
                        display, self.health, self.max_health)
