import unittest
import pygame

from world import World
from inventory import Inventory
from entities.player import Player
from settings import TILE_SIZE
from console import Console

class TestWorld(unittest.TestCase):
    def setUp(self):
        self.world = World(Console(10, 10, 10, 10, 10))
        self.inventory = Inventory()
        self.inventory.add_to_inventory("dirt", 100)
        self.inventory.equip_item(0)

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

    def test_remove_tile_drops_work(self):
        player = Player(4 * TILE_SIZE, 0)
        pos = (1, 1)
        chunk = [[[[0, 0], "dirt"]], 1]
        self.world.tiles = []
        self.world.tiles.append(pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE))

        self.world.game_map["0;0"] = chunk
        self.world.remove_tile(pos, player, False, False)
        # tile is removed
        self.assertEqual(self.world.game_map["0;0"], [[], 1])
        # drop is added
        self.assertEqual(len(self.world.drops), 1)

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

    def test_place_tile_distance_okay(self):
        # checks that the tile is placed
        chunk = [[[[TILE_SIZE, 0], "dirt"]], 1]
        target_chunk = [[[[TILE_SIZE, 0], 'dirt'], [[0, 0], 'dirt']], 1]

        self.world.game_map["0;0"] = chunk
        pos = (5, 5)
        player = Player(TILE_SIZE * 2, 0)
        self.world.place_tile(pos, "dirt", self.inventory, player, True)

        self.assertEqual(self.world.game_map["0;0"], target_chunk)

    def test_place_tile_distance_too_long(self):
        # checks that the tile isn't placed
        chunk = [[[[TILE_SIZE, 0], "dirt"]], 1]
        target_chunk = [[[[TILE_SIZE, 0], "dirt"]], 1]
        self.world.game_map["0;0"] = chunk
        pos = (5, 5)
        player = Player(TILE_SIZE * 5, 0)
        self.world.place_tile(pos, "dirt", self.inventory, player, True)

        self.assertEqual(self.world.game_map["0;0"], target_chunk)

    def test_place_tile_plant_replaced(self):
        # checks that the plant is replaced with dirt
        chunk = [[[[0, 0], "plant"]], 1]
        target_chunk = [[[[0, 0], 'dirt']], 1]

        self.world.game_map["0;0"] = chunk
        self.world.tiles = []
        pos = (5, 5)
        player = Player(TILE_SIZE * 2, 0)
        self.world.place_tile(pos, "dirt", self.inventory, player, True)

        self.assertEqual(self.world.game_map["0;0"], target_chunk)

    def test_place_tile_tile_already_exists(self):
        # checks that the tile isn't placed
        chunk = [[[[0, 0], "dirt"]], 1]
        target_chunk = [[[[0, 0], "dirt"]], 1]
        self.world.game_map["0;0"] = chunk
        pos = (5, 5)
        player = Player(TILE_SIZE * 3, 0)
        self.world.place_tile(pos, "dirt", self.inventory, player, True)

        self.assertEqual(self.world.game_map["0;0"], target_chunk)

    def test_place_tile_furniture(self):
        # checks that torch is placed on top of plank wall
        chunk = [[[[0, 0], "plank wall"]], 1]
        target_chunk = [[[[0, 0], "plank wall"], [[0, 0], "torch"]], 1]
        self.world.game_map["0;0"] = chunk
        pos = (5, 5)
        player = Player(TILE_SIZE * 3, 0)
        self.inventory.add_to_inventory("torch", 1)
        self.inventory.equip_item(1)
        self.world.place_tile(pos, "torch", self.inventory, player, True)

        self.assertEqual(self.world.game_map["0;0"], target_chunk)

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

    def test_world_generation_correct_format(self):
        chunk = self.world.generate_chunk(0, 0)
        # the chunk should be a list that contains an other list of any existing tiles and
        # the biome which is stored as an integer
        self.assertEqual(type(chunk), list)
        self.assertEqual(type(chunk[0]), list)
        self.assertEqual(type(chunk[1]), int)
