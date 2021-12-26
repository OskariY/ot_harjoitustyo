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
from resources import arrow_image, hurt_sound
from settings import TILE_SIZE

class Arrow():
    """
    Arrow that can be shot by the player with a bow or by skeletons.
    Causes damages to the player if shot by skeletons or to mobs if shot by the player.
    """
    def __init__(self, x, y, dx, dy, enemy=False):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.rect.centerx = x
        self.rect.centery = y
        self.dx = dx
        self.dy = dy
        if self.dx < 0:
            self.original_image = pygame.transform.flip(arrow_image, 1, 0)
            self.left = True
        else:
            self.original_image = arrow_image
            self.left = False
        self.image = self.original_image

        self.gravity = 0.1
        self.grounded = False
        self.despawn_count = 0
        # damages player or mobs
        self.enemy = enemy
        self.damage = 5

    def update(self, world, player):
        remove = False
        if self.grounded == False:
            self.rect.x += self.dx
            self.rect.y += self.dy
            self.dy += self.gravity

            for tile in world.tiles:
                if tile.collidepoint(self.rect.center):
                    self.grounded = True

            if self.enemy:
                if self.rect.colliderect(player.rect):
                    player.health -= self.damage
                    hurt_sound.play()
                    remove = True
            else:
                for mob in world.mobs:
                    if self.rect.colliderect(mob.rect):
                        mob.health -= self.damage
                        hurt_sound.play()
                        remove = True
                for worm in world.worms:
                    hit = False
                    if self.rect.colliderect(worm.head_rect):
                        hit = True
                    for body in worm.body_rects:
                        if self.rect.colliderect(body):
                            hit = True
                    if hit:
                        worm.health -= self.damage
                        hurt_sound.play()
                        remove = True

            # rotating arrow
            if self.left:
                if self.dx > self.dy:
                    self.image = pygame.transform.rotate(self.original_image, -45)
                elif -self.dx < self.dy * 2:
                    self.image = pygame.transform.rotate(self.original_image, 45)
                else:
                    self.image = self.original_image

            else:
                if -self.dx > self.dy:
                    self.image = pygame.transform.rotate(self.original_image, 45)
                elif self.dx < self.dy * 2:
                    self.image = pygame.transform.rotate(self.original_image, -45)
                else:
                    self.image = self.original_image
        else:
            self.despawn_count += 1
            if self.despawn_count >= 50:
                remove = True
        if remove and self in world.arrows:
            world.arrows.remove(self)

    def draw(self, display, world):
        display.blit(self.image, (self.rect.x-world.scrollx, self.rect.y-world.scrolly))

