import pygame
from resources import ITEMS, CRAFTING_REQUIREMENTS, select_arrow
from settings import CENTER, TILE_SIZE, GRAY, WHITE, BLACK, BROWN, RED
from functions import print_text

class Inventory():
    """
    Handles the inventory, hotbar, crafting and all actions related to them
    """
    def __init__(self):
        self.surface = pygame.Surface((300, 32*6+2))
        self.invx = CENTER[0] - self.surface.get_width() // 2
        self.invy = CENTER[1] - self.surface.get_height() // 2
        self.inv_select1 = -1
        self.inv_select2 = -1
        self.equipped = ""
        self.index_equipped = 0

        self.inventory = [] # format: [ [rect, item, amount, equipped] ]
        x = 2
        y = 2
        for i in range(30):
            self.inventory.append([pygame.Rect(x, y, 30, 30), "", 0, False])
            x += 32
            if x > 150:
                x = 2
                y += 32

        # hotbar
        self.hotbar_surf = pygame.Surface((32*5+4, 34))
        self.hotbar_x = CENTER[0] - self.hotbar_surf.get_width() // 2

        # crafting related vars
        self.crafting_window = pygame.Rect(32*5+12, 30, 120, 64)
        self.crafting_button = pygame.Rect(258, 170, 30, 15)
        self.crafting_selection_width = self.crafting_window.width // 2
        self.crafting_selection_height = self.crafting_window.height // 3
        self.crafting_item_selected = None
        self.crafting_item_rect = None
        self.crafting_back_button = pygame.Rect(self.crafting_window.x,
                                                self.crafting_window.bottom + 2,
                                                TILE_SIZE, TILE_SIZE)
        self.crafting_next_button = pygame.Rect(self.crafting_window.right - TILE_SIZE,
                                                self.crafting_window.bottom + 2,
                                                TILE_SIZE, TILE_SIZE)
        self.crafting_index_1 = 0
        self.crafting_index_2 = 6
        self.left_arrow = select_arrow
        self.right_arrow = pygame.transform.flip(select_arrow, 1, 0)
        self.right_arrow.set_colorkey(WHITE)

        self.crafting_selection_rects = []
        x = 32*5+12
        y = 30
        for i in range(6):
            self.crafting_selection_rects.append(pygame.Rect(x, y, self.crafting_selection_width,
                                                             self.crafting_selection_height))
            y += self.crafting_selection_height
            if i == 2:
                y = 30
                x = 32*5+12 + self.crafting_selection_width

    def draw(self, inv_open, display, mousepos): # pragma: no cover
        """
        Draws the inventory/crafting interface if it's open, otherwise just draws the hotbar
        """
        if inv_open:
            self.surface.fill(GRAY)
            x = 2
            y = 2
            # draw inventory grid
            for i in range(30):
                # draw hotbar with a different color
                if i < 5:
                    pygame.draw.rect(self.surface, BLACK, self.inventory[i][0], 1)
                # draw other inventory slots
                else:
                    pygame.draw.rect(self.surface, WHITE, self.inventory[i][0], 1)
                # if the slot contains an item, draw it along with text
                if self.inventory[i][1]:
                    self.surface.blit(pygame.transform.scale(ITEMS[self.inventory[i][1]]["image"], (TILE_SIZE, TILE_SIZE)), (x + 2, y + 2))
                    print_text(str(self.inventory[i][2]), x + 29, y, self.surface, 2, 8)
                    print_text(str(self.inventory[i][1][:8]), x + 16, y + 19, self.surface, 1, 8)

                x += 32
                if x > 150:
                    x = 2
                    y += 32
            # crafting
            print_text("Crafting", 230, 8, self.surface, 1, 16, BLACK)
            pygame.draw.rect(self.surface, BROWN, self.crafting_window)
            x = 2
            y = 2
            self.visible_crafting_items = list(CRAFTING_REQUIREMENTS.keys())[self.crafting_index_1:self.crafting_index_2]
            for itemname in self.visible_crafting_items:
                self.surface.blit(ITEMS[itemname]["image"],
                                  (self.crafting_window.x + x, self.crafting_window.y + y))
                print_text(itemname, self.crafting_window.x + x + 18, self.crafting_window.y + y,
                           self.surface, 0, 8, WHITE)
                y += self.crafting_window.height // 3
                if y >= 3*18:
                    y = 2
                    x += self.crafting_window.width // 2

            if self.crafting_item_selected is not None:
                pygame.draw.rect(self.surface, WHITE, self.crafting_item_rect, 1)
                if self.crafting_item_selected < len(self.visible_crafting_items):
                    x = self.crafting_window.x
                    y = self.crafting_window.bottom + 32
                    print_text("Requirements", x+self.crafting_window.width//2, y - 18,
                               self.surface, 1, 16, BLACK)
                    # check requirements for crafting
                    for requirement in CRAFTING_REQUIREMENTS[self.visible_crafting_items[self.crafting_item_selected]]:
                        self.surface.blit(ITEMS[requirement[0]]["image"], (x, y))
                        textcolor = RED
                        # text is black if you have the item, red if you don't
                        if self.in_inventory(requirement[0], requirement[1]):
                            textcolor = BLACK
                        print_text("{} x {}".format(requirement[1], requirement[0]),
                                   x+18, y+2, self.surface, 0, 8, textcolor)
                        y += 18

            pygame.draw.rect(self.surface, BLACK, self.crafting_button, 1)
            print_text("Craft", 258+15, 172, self.surface, 1, 8, BLACK)
            self.surface.blit(self.left_arrow, (self.crafting_back_button.x,
                                                self.crafting_back_button.y))
            self.surface.blit(self.right_arrow, (self.crafting_next_button.x,
                                                 self.crafting_next_button.y))



            # draw the inventory surface to the display
            display.blit(self.surface, (self.invx, self.invy))
            # draw dragging items in inventory
            if self.inv_select1 != -1 and self.inventory[self.inv_select1][1] != "":
                display.blit(ITEMS[self.inventory[self.inv_select1][1]]["image"], mousepos)
        # draw hotbar if inventory isn't open
        else:
            self.hotbar_surf.fill(GRAY)
            x = 2
            y = 2
            for i in range(5):
                if self.inventory[i][3]:
                    pygame.draw.rect(self.hotbar_surf, BLACK, pygame.Rect(x, y, 30, 30), 1)
                else:
                    pygame.draw.rect(self.hotbar_surf, WHITE, pygame.Rect(x, y, 30, 30), 1)
                if self.inventory[i][1]:
                    self.hotbar_surf.blit(ITEMS[self.inventory[i][1]]["image"], (x + 8, y + 8))
                    print_text(str(self.inventory[i][2]), x + 29, y, self.hotbar_surf, 2, 8, WHITE)

                x += 32

            display.blit(self.hotbar_surf, (self.hotbar_x, 0))


    def add_to_inventory(self, item, amount):
        """
        Adds item to inventory
        Args:
            item, amount
        """
        item_in_inventory = False
        # see if item is in inventory
        for squere in self.inventory:
            # if the slot contains item and has less items than the max stack
            if squere[1] == item and squere[2] < ITEMS[item]["stack"]:

                if squere[2] + amount > ITEMS[item]["stack"]:
                    minus = ITEMS[item]["stack"] - squere[2]
                    squere[2] = ITEMS[item]["stack"]
                    self.add_to_inventory(item, amount - minus)
                else:
                    squere[2] += amount

                item_in_inventory = True
                break
        if not item_in_inventory:
            for squere in self.inventory:
                if squere[1] == "" or squere[1] is None:
                    squere[1] = item
                    if amount > ITEMS[item]["stack"]:
                        squere[2] = ITEMS[item]["stack"]
                        self.add_to_inventory(item, amount - ITEMS[item]["stack"])
                    else:
                        squere[2] = amount
                    break

    def remove_item(self, item, amount):
        """
        Removes item from inventory
        Args:
            item, amount
        """
        for squere in self.inventory:
            if squere[1] == item:
                if squere[2] < amount:
                    if self.equipped == squere[1]:
                        self.equipped = ""
                    squere[1] = ""
                    squere[2] = 0
                    squere[3] = False
                    self.remove_item(item, amount - squere[2])
                else:
                    squere[2] -= amount
                    if squere[2] <= 0:
                        if self.equipped == squere[1]:
                            self.equipped = ""
                        squere[1] = ""
                        squere[2] = 0
                        squere[3] = False

                break

    def inventory_drag(self):
        """
        Drags items around the inventory
        """
        if self.inv_select1 != -1 and self.inv_select2 != -1 and self.inv_select1 != self.inv_select2:
            # if destination item is same as beginning item
            if self.inventory[self.inv_select1][1] == self.inventory[self.inv_select2][1]:
                # if destination + beginning is more than the stack limit
                if self.inventory[self.inv_select2][2] + self.inventory[self.inv_select1][2] > ITEMS[self.inventory[self.inv_select2][1]]["stack"]:
                    minus = ITEMS[self.inventory[self.inv_select2][1]]["stack"] - self.inventory[self.inv_select2][2]
                    self.inventory[self.inv_select2][2] = ITEMS[self.inventory[self.inv_select2][1]]["stack"]
                    self.inventory[self.inv_select1][2] -= minus

                # stack
                else:
                    self.inventory[self.inv_select2][2] += self.inventory[self.inv_select1][2]
                    self.inventory[self.inv_select1][1] = ""
                    self.inventory[self.inv_select1][2] = 0
            else:
                temp1 = self.inventory[self.inv_select2][1]
                temp2 = self.inventory[self.inv_select2][2]
                self.inventory[self.inv_select2][1] = self.inventory[self.inv_select1][1]
                self.inventory[self.inv_select2][2] = self.inventory[self.inv_select1][2]
                self.inventory[self.inv_select1][1] = temp1
                self.inventory[self.inv_select1][2] = temp2
            self.inv_select1 = -1
            self.inv_select2 = -1

    def in_inventory(self, item, amount=1):
        """
        Checks if an item is in the inventory
        Args:
            item, amount
        Returns:
            boolean
        """
        for squere in self.inventory:
            if squere[1] == item and squere[2] >= amount:
                return True
        return False

    def equip_item(self, index):
        """
        Takes inventory index (0-29) as argument and equips it and unequips all other ITEMS
        """
        for i, item in enumerate(self.inventory):
            if i == index:
                item[3] = True
                self.equipped = self.inventory[index][1]
                self.index_equipped = i
            else:
                item[3] = False
