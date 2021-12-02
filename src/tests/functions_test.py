import unittest
import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))

from functions import move
from world import World

class TestMove(unittest.TestCase):
    def setUp(self):
        self.rect = pygame.Rect(16, 16, 16, 16)
        self.world = World()
        self.world.tiles = [] # usually created in the world generation process
        self.world.slabs = []
        x = -64
        for i in range(10):
            self.world.tiles.append(pygame.Rect(x, 16, 16, 16))
            x += 16

    def test_move_no_dspeed_no_collisions(self):
        dx = 0
        dy = 0
        # set the test rect slightly above the tiles
        self.rect.bottom = 14
        new_rect, collisions = move(self.rect, dx, dy, self.world)
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
        new_rect, collisions = move(self.rect, dx, dy, self.world)
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
        new_rect, collisions = move(self.rect, dx, dy, self.world)
        self.assertEqual(new_rect, self.rect)
        self.assertEqual(collisions, {
            "right": True,
            "left": False,
            "up": False,
            "down": False,
            })

