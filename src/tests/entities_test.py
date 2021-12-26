import unittest
import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))

from world import World
from console import Console
from entities.player import Player
from entities.walkingmob import WalkingMob
from entities.flyingmob import FlyingMob
from entities.caveworm import Worm
class TestWalkingMob(unittest.TestCase):
    def setUp(self):
        self.world = World(Console(0, 0, 10, 10, 10))
        # usually created in the world generation process
        self.world.tiles = []
        self.world.slabs = []
        self.player = Player(0, 0)
        x = -64
        for i in range(10):
            self.world.tiles.append(pygame.Rect(x, 64, 16, 16))
            x += 16

    def test_move(self):
        mob = WalkingMob(100, 0)
        startx = mob.rect.x
        mob.move(self.player, self.world)

        self.assertTrue(mob.rect.x < startx)

    def test_skeleton_shoot(self):
        mob = WalkingMob(100, 0, "skeleton")
        mob.update(self.player, self.world)

        self.assertTrue(len(self.world.arrows) > 0)

    def test_death(self):
        mob = WalkingMob(100, 0)
        self.world.mobs.append(mob)
        self.world.entities.append(mob)
        mob.update(self.player, self.world)
        mob.health = 0
        mob.update(self.player, self.world)

        self.assertTrue(len(self.world.mobs) == 0)
        self.assertTrue(len(self.world.entities) == 0)
        self.assertTrue(len(self.world.drops) > 0)

    def test_despawn(self):
        mob = WalkingMob(10000, 0)
        self.world.mobs.append(mob)
        self.world.entities.append(mob)
        mob.update(self.player, self.world)

        self.assertTrue(len(self.world.mobs) == 0)
        self.assertTrue(len(self.world.entities) == 0)

class TestFlyingMob(unittest.TestCase):
    def setUp(self):
        self.world = World(Console(0, 0, 10, 10, 10))
        # usually created in the world generation process
        self.world.tiles = []
        self.world.slabs = []
        self.player = Player(0, 0)
        x = -64
        for i in range(10):
            self.world.tiles.append(pygame.Rect(x, 64, 16, 16))
            x += 16

    def test_move(self):
        mob = FlyingMob(100, 0)
        startx = mob.rect.x
        mob.move(self.player, self.world)

        self.assertTrue(mob.rect.x < startx)

    def test_death(self):
        mob = FlyingMob(100, 0)
        self.world.mobs.append(mob)
        self.world.entities.append(mob)
        mob.update(self.player, self.world)
        mob.health = 0
        mob.update(self.player, self.world)

        self.assertTrue(len(self.world.mobs) == 0)
        self.assertTrue(len(self.world.entities) == 0)
        self.assertTrue(len(self.world.drops) > 0)

    def test_despawn(self):
        mob = WalkingMob(10000, 0)
        self.world.mobs.append(mob)
        self.world.entities.append(mob)
        mob.update(self.player, self.world)

        self.assertTrue(len(self.world.mobs) == 0)
        self.assertTrue(len(self.world.entities) == 0)

class TestWorm(unittest.TestCase):
    def setUp(self):
        self.world = World(Console(0, 0, 10, 10, 10))
        # usually created in the world generation process
        self.world.tiles = []
        self.world.slabs = []
        self.player = Player(0, 1000)
        x = -64
        for i in range(10):
            self.world.tiles.append(pygame.Rect(x, 64, 16, 16))
            x += 16

    def test_move(self):
        mob = Worm(100, 1000)
        startx = mob.head_rect.x
        mob.move(self.player.rect.x, self.player.rect.y)

        self.assertTrue(mob.head_rect.x < startx)

    def test_death(self):
        mob = Worm(100, 1000)
        self.world.worms.append(mob)
        mob.update(self.player, self.world)
        mob.health = 0
        mob.update(self.player, self.world)

        self.assertTrue(len(self.world.worms) == 0)
        self.assertTrue(len(self.world.drops) > 0)

    def test_despawn(self):
        mob = Worm(10000, 1000)
        self.world.worms.append(mob)
        mob.update(self.player, self.world)

        self.assertTrue(len(self.world.worms) == 0)
        self.assertTrue(len(self.world.entities) == 0)
