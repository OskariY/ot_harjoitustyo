import unittest
import pygame
from functions import move

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

