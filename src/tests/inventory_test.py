import unittest
import pygame

from inventory import Inventory

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inventory = Inventory()

    # test adding item to empty inventory
    def test_add_to_inventory_empty(self):
        self.inventory.add_to_inventory("axe", 1)
        # check that axe is in inventory
        self.assertEqual(self.inventory.inventory [0][1], "axe")
   
    # test adding items over the stack limit
    # the items should be divided into multiple slots as needed
    def test_add_to_inventory_over_stack(self):
        self.inventory.add_to_inventory("axe", 2)
        # check that axe is in inventory
        self.assertEqual(self.inventory.inventory[0][1], "axe")
        self.assertEqual(self.inventory.inventory[1][1], "axe")
   
    def test_remove_inventory_item(self):
        # add axe to inventory and equip it
        self.inventory.add_to_inventory("axe", 1)
        self.inventory.equip_item(0)
        
        # remove axe
        self.inventory.remove_item("axe", 1)

        self.assertEqual(self.inventory.inventory[0][1], "")
