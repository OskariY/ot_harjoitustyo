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

    def test_remove_item_normal(self):
        # add axe to inventory and equip it
        self.inventory.add_to_inventory("dirt", 100)
        self.inventory.equip_item(0)

        # remove axe
        self.inventory.remove_item("dirt", 1)

        self.assertEqual(self.inventory.inventory[0][2], 99)

    def test_remove_item_more_than_exists(self):
        self.inventory.add_to_inventory("dirt", 10)
        self.inventory.remove_item("dirt", 11)

        self.assertEqual(self.inventory.inventory[0][1], "")
        self.assertEqual(self.inventory.inventory[0][2], 0)

    def test_remove_item_equipped_removed(self):
        self.inventory.add_to_inventory("dirt", 10)
        self.inventory.equip_item(0)
        self.inventory.remove_item("dirt", 11)

        self.assertEqual(self.inventory.equipped, "")

    def test_in_inventory_true(self):
        self.inventory.add_to_inventory("dirt", 10)
        output = self.inventory.in_inventory("dirt")

        self.assertEqual(output, True)

    def test_in_inventory_false(self):
        output = self.inventory.in_inventory("dirt")

        self.assertEqual(output, False)

    def test_drag_item_to_empty(self):
        self.inventory.add_to_inventory("dirt", 1)
        self.inventory.inv_select1 = 0
        self.inventory.inv_select2 = 1

        self.inventory.inventory_drag()

        self.assertEqual(self.inventory.inventory[0][1], "")
        self.assertEqual(self.inventory.inventory[1][1], "dirt")

    def test_drag_item_to_item(self):
        self.inventory.add_to_inventory("dirt", 100)
        self.inventory.add_to_inventory("stone", 100)
        self.inventory.inv_select1 = 0
        self.inventory.inv_select2 = 1
        self.inventory.inventory_drag()

        print(self.inventory.inventory)
        self.assertEqual(self.inventory.inventory[0][1], "stone")
        self.assertEqual(self.inventory.inventory[1][1], "dirt")

    def test_drag_combine_stacks(self):
        # create two stacks of dirt
        self.inventory.add_to_inventory("dirt", 1500)
        # remove some of it so both stacks are 75
        self.inventory.inventory[0][2] = 75
        self.inventory.inventory[1][2] = 75

        self.inventory.inv_select1 = 0
        self.inventory.inv_select2 = 1
        self.inventory.inventory_drag()

        print(self.inventory.inventory)
        self.assertEqual(self.inventory.inventory[1][2], 150)

    def test_drag_combine_stacks_over_limit(self):
        # create two stacks of dirt
        self.inventory.add_to_inventory("dirt", 1500)
        # remove some of it
        self.inventory.inventory[0][2] = 750
        self.inventory.inventory[1][2] = 750

        self.inventory.inv_select1 = 0
        self.inventory.inv_select2 = 1
        self.inventory.inventory_drag()

        print(self.inventory.inventory)
        self.assertEqual(self.inventory.inventory[0][2], 501)
        self.assertEqual(self.inventory.inventory[1][2], 999)
