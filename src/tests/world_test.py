import unittest
import pygame

from world import World
from inventory import Inventory
from entities.player import Player
from settings import TILE_SIZE

class TestWorld(unittest.TestCase):
    def setUp(self):
        self.world = World()
        self.inventory = Inventory()
        self.inventory.add_to_inventory("dirt", 100)

    def test_get_next_tiles_false(self):
        self.world.buildables = []
        self.assertEqual(self.world.get_next_tiles((0, 0)), False)

    def test_get_next_tiles_true(self):
        self.world.buildables = []
        self.world.buildables.append(pygame.Rect(0, 0, 16, 16))
        self.assertEqual(self.world.get_next_tiles((0, 0)), True)

    def test_remove_tile_distance_too_long(self):
        player = Player(0, 0)
        pos = (TILE_SIZE*6, 0)
        chunk = [[[[TILE_SIZE * 6, 0], "dirt"]], 1]
        self.world.game_map["0;0"] = chunk
        self.world.remove_tile(pos, player)
        self.assertEqual(self.world.game_map["0;0"], chunk)
    
    def test_remove_tile_distance_works(self):
        player = Player(4 * TILE_SIZE, 0)
        pos = (1, 1)
        chunk = [[[[0, 0], "dirt"]], 1]
        self.world.game_map["0;0"] = chunk
        self.world.remove_tile(pos, player, True, False)
        self.assertEqual(self.world.game_map["0;0"], [[], 1])       

    def test_get_chunk_none(self):
        pos = (0, 0)
        self.assertEqual(self.world.get_chunk(pos), None)

    def test_get_chunk_works(self):
        pos = (0, 0)
        chunk = [[[[TILE_SIZE * 6, 0], "dirt"]], 1]
        self.world.game_map["0;0"] = chunk
        self.assertEqual(self.world.get_chunk(pos), "0;0")

    def test_tile_exists_none(self):
        chunk = [[], 1]
        self.world.game_map["0;0"] = chunk
        self.assertEqual(self.world.tile_exists("0;0", 0, 0), None)

    def test_tile_exists_works(self):
        chunk = [[[[0, 0], "dirt"]], 1]
        self.world.game_map["0;0"] = chunk
        self.assertEqual(type(self.world.tile_exists("0;0", 0, 0)), list)

#    def test_place_tile_works_notile(self):
#        chunk = [[[[TILE_SIZE, 0], "dirt"]], 1]
#        self.world.game_map["0;0"] = chunk
#        pos = (5, 5)
#        player = Player(TILE_SIZE * 2, 0)
#        self.world.place_tile(pos, "dirt", self.inventory, player, True)
#        self.assertEqual(self.world.game_map["0;0"], chunk) 

    def test_get_tile_works(self):
        chunk = [[[[0, 0], "dirt"]], 1]
        self.world.game_map["0;0"] = chunk
        self.assertEqual(self.world.get_tile((0, 0)), [[0, 0], "dirt"])

    def test_get_tile_none(self):
        chunk = [[[[TILE_SIZE*2, 0], "dirt"]], 1]
        self.world.game_map["0;0"] = chunk
        self.assertEqual(self.world.get_tile((0, 0)), None)
    
    def test_get_biome(self):
        chunk = [[[[TILE_SIZE*2, 0], "dirt"]], 1]
        self.world.game_map["0;0"] = chunk
        self.assertEqual(self.world.get_biome((0, 0)), 1)
