import os
import unittest

from world import World
from inventory import Inventory
from entities.player import Player
from entities.walkingmob import WalkingMob
from entities.flyingmob import FlyingMob
from entities.caveworm import Worm
from save_functions import *
from console import Console

class TestSaveFunctions(unittest.TestCase):
    def setUp(self):
        self.world = World(Console(10, 10, 10, 10, 10))
        self.inventory = Inventory()
        self.player = Player(0, 0)

    def test_create_world(self):
        create_world("unittest_test")
        target = {
            "game_map": {},
            "spawn_x": 0,
            "spawn_y": -100,
            "player_x": 200,
            "player_y": -100,
            "scrollx": 0,
            "scrolly": 0,
            "mob_coords": [],
            "worm_coords": [],
            "drops": [],
            "inventory": [],
            "tod": 0,

            # world generation parameters
            "seed": random.randint(-9999999,9999999),
        }

        game_data = load_game("unittest_test")

        self.assertEqual(type(game_data), dict)
        for key, value in game_data.items():
            if key == "seed":
                self.assertEqual(type(value), int)
            else:
                self.assertEqual(value, target[key])

    def test_save_game(self):
        self.world.mobs.append(WalkingMob(0, 0))
        self.world.mobs.append(WalkingMob(0, 0, "zombie"))
        self.world.mobs.append(FlyingMob(0, 0))
        self.world.worms.append(Worm(0, 0))
        save_game("unittest_test", self.world, self.inventory, self.player)
        target = {
            "game_map": self.world.game_map,
            "spawn_x": self.world.spawn_x,
            "spawn_y": self.world.spawn_y,
            "player_x": self.player.rect.x,
            "player_y": self.player.rect.y,
            "scrollx": self.world.scrollx,
            "scrolly": self.world.scrolly,
            "mob_coords": [],
            "worm_coords": [],
            "inventory": self.inventory.inventory,
            "tod": self.world.tod,

            # world generation parameters
            "seed": self.world.seed
        }
        for mob in self.world.mobs:
            target["mob_coords"].append([mob.rect.x, mob.rect.y, mob.mobtype])
        for worm in self.world.worms:
            target["worm_coords"].append([worm.head_rect.x, worm.head_rect.y])

        game_data = load_game("unittest_test")

        self.assertEqual(game_data, target)

    def tearDown(self):
        os.remove("saves/unittest_test")
