import unittest
import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))

from functions import move
from world import World
from console import Console
class TestMove(unittest.TestCase):
    class TestObject():
        def __init__(self):
            self.rect = pygame.Rect(16, 16, 16, 16)
            self.dx = 0
            self.dy = 0
            self.collisions = {}

    def setUp(self):
        self.obj = self.TestObject()
        self.world = World(Console(0, 0, 10, 10, 10))
        # usually created in the world generation process
        self.world.tiles = []
        self.world.slabs = []
        x = -64
        for i in range(10):
            self.world.tiles.append(pygame.Rect(x, 16, 16, 16))
            x += 16

    def test_move_no_dspeed_no_collisions(self):
        # set the test rect slightly above the tiles
        self.obj.rect.bottom = 14
        old_rect = self.obj.rect
        move(self.obj, self.world)
        new_rect = self.obj.rect
        # rect doesn't move
        self.assertEqual(new_rect, old_rect)
        # no collisions are detected
        self.assertEqual(self.obj.collisions, {
            "right": False,
            "left": False,
            "up": False,
            "down": False,
            })

    def test_move_y_collisions(self):
        self.obj.dy = 3

        self.obj.rect.bottom = 14
        move(self.obj, self.world)
        # rect bottom should be stopped at 16 instead of going up to 17
        self.assertEqual(self.obj.rect.bottom, 16)
        # "down" should be True
        self.assertEqual(self.obj.collisions, {
            "right": False,
            "left": False,
            "up": False,
            "down": True,
            })

    def test_move_x_collisions(self):
        self.obj.dx = 5

        self.obj.rect.y = 16
        self.obj.rect.right = -65
        move(self.obj, self.world)
        self.assertEqual(self.obj.rect.right, -64)
        self.assertEqual(self.obj.collisions, {
            "right": True,
            "left": False,
            "up": False,
            "down": False,
            })

