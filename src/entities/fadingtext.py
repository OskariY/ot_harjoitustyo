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

from settings import BLACK, WHITE
from functions import print_text

fadey = 0
class FadingText():
    """
    A fading text popup that appears above the player, rises and disappears
    """

    def __init__(self, x, y, text, world, color=BLACK):
        global fadey
        self.x = x
        self.y = y - fadey
        self.size = 16
        self.text = text
        self.color = color
        if world.current_biome == 3 or world.is_night and color == BLACK:
            self.color = WHITE
        fadey += 10

    def update(self, popups):
        global fadey
        self.size -= 0.3
        self.y -= 1
        if self.size < 8:
            popups.remove(self)
            fadey -= 10

    def draw(self, display, scrollx, scrolly):
        print_text(self.text, int(self.x - scrollx), int(round(self.y) - scrolly),
                   display, 1, int(round(self.size)), self.color)
