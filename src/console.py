import pygame
from functions import print_text
from settings import BLACK, WHITE, GRAY
from resources import ITEMS

class Console:
    """Ingame console class for logging"""

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
                if not args[0].isnumeric():
                    self.log(f"Error: coordinate must be a number")
                elif not args[1].isnumeric():
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
