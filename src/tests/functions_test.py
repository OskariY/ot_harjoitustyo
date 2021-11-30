import unittest
import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))

from functions import *

class TestMove(unittest.TestCase):
    def setUp(self):
        self.rect = pygame.Rect(16, 16, 16, 16)
        self.tiles = []
        x = -64
        for i in range(10):
            self.tiles.append(pygame.Rect(x, 16, 16, 16))
            x += 16

    def test_move_no_dspeed_no_collisions(self):
        dx = 0
        dy = 0
        # set the test rect slightly above the tiles
        self.rect.bottom = 14
        new_rect, collisions = move(self.rect, dx, dy, self.tiles)
        # rect doesn't move
        self.assertEqual(new_rect, self.rect)
        # no collisions are detected
        self.assertEqual(collisions, {
            "right": False,
            "left": False,
            "up": False,
            "down": False,
            })

    def test_move_y_collisions(self):
        dx = 0
        dy = 3
        
        self.rect.bottom = 14
        new_rect, collisions = move(self.rect, dx, dy, self.tiles)
        self.assertEqual(new_rect, self.rect)
        self.assertEqual(collisions, {
            "right": False,
            "left": False,
            "up": False,
            "down": True,
            })

    def test_move_x_collisions(self):
        dx = 2
        dy = 0
        
        self.rect.y = 16
        self.rect.right = -65
        new_rect, collisions = move(self.rect, dx, dy, self.tiles)
        self.assertEqual(new_rect, self.rect)
        self.assertEqual(collisions, {
            "right": True,
            "left": False,
            "up": False,
            "down": False,
            })

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inventory = []
        x = 2
        y = 2
        for i in range(30):
            self.inventory.append([pygame.Rect(x, y, 30, 30), "", 0, False])
            x += 32
            if x > 150:
                x = 2
                y += 32
    
    # test adding item to empty inventory
    def test_add_to_inventory_empty(self):
        self.inventory = add_to_inventory(self.inventory, "axe", 1)
        # check that axe is in inventory
        self.assertEqual(self.inventory[0][1], "axe")
   
   # test adding items over the stack limit
   # the items should be divided into multiple slots as needed
    def test_add_to_inventory_over_stack(self):
        self.inventory = add_to_inventory(self.inventory, "axe", 2)
        # check that axe is in inventory
        self.assertEqual(self.inventory[0][1], "axe")
        self.assertEqual(self.inventory[1][1], "axe")
   
    def test_remove_inventory_item(self):
        # add axe to inventory and equip it
        self.inventory = add_to_inventory(self.inventory, "axe", 1)
        self.inventory, equipped = equip_item(self.inventory, "", 0)
        
        # remove axe
        self.inventory, equipped = remove_inventory_item(self.inventory, equipped, equipped, 1)

        self.assertEqual(self.inventory[0][1], "")
