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
from functions import print_text
from settings import BLACK, WHITE, GRAY
from resources import ITEMS

class Console:
    """Ingame console object for logging and cheat commands"""

    def __init__(self, x, y, width, height, font):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.surf = pygame.Surface((width, height))

        self.font = font

        self.show = False # is console visible
        self.focused = False

        self.history = [] # list of strings

        self.offset = 0

        self.help_text = [
                "help - print text",
                "give [item] [amount] - give an item",
                "tp [x] [y] - teleport to coordinates",
                "seed [seed] - set seed to [seed]",
                "tod [tod] - set time of day",
                ]

        self.cmdbuffer = ""

    def command(self, inventory, world, player):
        text = self.cmdbuffer.split(" ")
        cmd = text[0]
        args = text[1:]

        if cmd == "help":
            for line in self.help_text:
                self.log(line)
        elif cmd == "give":
            if len(args) == 2:
                if args[0] not in ITEMS.keys():
                    self.log(f"Error: item '{args[0]}' not found")
                elif not args[1].isnumeric():
                    self.log(f"Error: amount must be a number")
                else:
                    inventory.add_to_inventory(args[0], int(args[1]))
            else:
                self.log("Error: give takes two arguments, item and amount")
        elif cmd == "tp":
            if len(args) == 2:
                if not args[1].strip("-").isdigit():
                    self.log(f"Error: coordinate must be a number")
                elif not args[1].strip("-").isdigit():
                    self.log(f"Error: coordinate must be a number")
                else:
                    player.rect.x = int(args[0])
                    player.rect.y = int(args[1])
            else:
                self.log("Error: tp takes two arguments, x and y")
        elif cmd == "seed":
            if len(args) == 1:
                if not args[0].isnumeric():
                    self.log(f"Error: seed must be a number")
                else:
                    world.seed = int(args[0])
            else:
                self.log("Error: seed takes one argument")
        elif cmd == "tod":
            if len(args) == 1:
                if not args[0].isnumeric():
                    self.log(f"Error: tod must be a number")
                else:
                    world.tod = int(args[0])
            else:
                self.log("Error: tod takes one argument")
                self.log("day: 0-40000, evening: 40000-50000, night: 50000-90000, morning: 90000-100000")
        else:
            self.log("Unknown command. Type 'help' to see all commands.")

        self.log(" ")
        self.cmdbuffer = ""

    def update(self):
        mouse = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse) and self.show:
            self.focused = True
        else:
            self.focused = False

    def draw(self, display):
        if self.show:
            self.surf.fill(GRAY)

            if self.focused:
                pygame.draw.rect(self.surf, WHITE, self.surf.get_rect(), 1)

            text_x = 1
            bottom_edge = self.height - self.font * 2 + self.offset
            text_y = bottom_edge
            print_text(">" + self.cmdbuffer, text_x, text_y, self.surf, 0, self.font, WHITE)
            text_y -= self.font
            for line in self.history:
                if text_y > self.y-self.font and text_y <= bottom_edge:
                    print_text(line, text_x, text_y, self.surf, 0, self.font, WHITE)
                    text_y -= self.font

            display.blit(self.surf, (self.x, self.y))

    def log(self, text):
        self.history.insert(0, text)
        self.history = self.history[:300]
