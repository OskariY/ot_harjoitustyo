import pygame
from resources import ITEMS
from settings import CENTER, TILE_SIZE, GRAY, WHITE, WHITE, BLACK
from functions import print_text

class Inventory():
    def __init__(self):
        self.surface = pygame.Surface((300, 32*6+2))
        self.invx = CENTER[0] - self.surface.get_width() // 2
        self.invy = CENTER[1] - self.surface.get_height() // 2
        self.inv_select1 = None
        self.inv_select2 = None
        self.equipped = ""

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



    def draw(self, inv_open, display, mousepos):
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
            # draw the inventory surface to the display
            display.blit(self.surface, (self.invx, self.invy))
            # draw dragging items in inventory
            if self.inv_select1 != '' and self.inv_select1 != None and self.inventory[self.inv_select1][1] != None:
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
                if squere[1] == "" or squere[1] == None:
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
                    squere[1] = ""
                    squere[2] = 0
                    squere[3] = False
                    self.remove_item(item, amount - squere[2])
                else:
                    squere[2] -= amount
                    if squere[2] <= 0:
                        squere[1] = ""
                        squere[2] = 0
                        squere[3] = False
                        if self.equipped == squere[1]:
                            self.equipped = ""

                break

    def inventory_drag(self):
        """
        Drags items around the inventory
        """
        
        if self.inv_select1 != None and self.inv_select2 != None and self.inv_select1 != self.inv_select2:
            # if destination is empty, move item
            if self.inventory[self.inv_select2][1] == None:
                self.inventory[self.inv_select2][1] = self.inventory[self.inv_select1][1]
                self.inventory[self.inv_select2][2] = self.inventory[self.inv_select1][2]
                self.inventory[self.inv_select1][1] = None
                self.inventory[self.inv_select1][2] = 0
            else:
                # if destination item is same as beginning item
                if self.inventory[self.inv_select1][1] == self.inventory[self.inv_select2][1]:
                    # if destination + beginning is more than the stack limit
                    if self.inventory[self.inv_select2][2] + self.inventory[self.inv_select1][2] > ITEMS[self.inventory[self.inv_select2][1]]["stack"]:
                        minus = ITEMS[self.inventory[self.inv_select2][1]]["stack"] - self.inventory[self.self.inv_select2][2]
                        self.inventory[self.inv_select2][2] = ITEMS[self.inventory[self.inv_select2][1]]["stack"]
                        self.inventory[self.inv_select1][2] -= minus

                    # stack
                    else:
                        self.inventory[self.inv_select2][2] += self.inventory[self.inv_select1][2]
                        self.inventory[self.inv_select1][1] = None
                        self.inventory[self.inv_select1][2] = 0
                else:
                    temp1 = self.inventory[self.inv_select2][1]
                    temp2 = self.inventory[self.inv_select2][2]
                    self.inventory[self.inv_select2][1] = self.inventory[self.inv_select1][1]
                    self.inventory[self.inv_select2][2] = self.inventory[self.inv_select1][2]
                    self.inventory[self.inv_select1][1] = temp1
                    self.inventory[self.inv_select1][2] = temp2

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
            else:
                item[3] = False
