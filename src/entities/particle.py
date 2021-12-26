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

import random
import pygame

class Particle():
    """
    Particle object for visual effects. The size of the particle is randomized upon creation.
    The particle size is then decreased with each update, and the object is removed once the
    particle gets small enough.
    """
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.dx = random.randint(0, 10) / 10 - 1
        self.dy = random.randint(0, 10) / 10 - 1
        # both timer and radius for the particle
        self.timer = random.randint(1, 7)

    def update(self, display, particles, scrollx, scrolly):
        """
        Updates and draws the particle object
        """
        self.x += self.dx
        self.y += self.dy
        self.y += 2
        self.timer -= 0.2
        pygame.draw.circle(display, self.color, (int(self.x - scrollx), int(self.y - scrolly)), int(self.timer))
        if self.timer <= 0:
            particles.remove(self)

