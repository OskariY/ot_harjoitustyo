import pygame
from settings import DISPLAY_WIDTH, DISPLAY_HEIGHT, TILE_SIZE
from resources import ITEMS
from functions import move

class DroppedItem():
    """
    Object for drops that can be picked up by the player
    """

    def __init__(self, x, y, dx, dy, item, amount=1):
        self.image = ITEMS[item]["image"]
        size = TILE_SIZE - 4

        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.item = item
        self.dx = dx
        self.dy = dy
        self.gravity = 0.4
        self.amount = amount
        self.collisions = {}

    def update(self, world):
        """
        Updates the drop position based on its gravity and dx/dy values if it's
        not outside the screen
        """
        # only update movement if drop is in the screen
        # prevents them from falling off the map
        if self.rect.x - world.scrollx > 0 \
                and self.rect.x - world.scrollx < DISPLAY_WIDTH \
                and self.rect.y - world.scrolly > 0 \
                and self.rect.y - world.scrolly < DISPLAY_HEIGHT:
            move(self, world)
            self.dy += self.gravity
            if self.collisions["down"]:
                self.dy = 0
                self.dx = 0

            if self.collisions["left"] or self.collisions["right"]:
                self.dx = 0

    def draw(self, display, scrollx, scrolly): # pragma: no cover
        """
        Draws the drop
        """
        display.blit(self.image, (self.rect.x - scrollx, self.rect.y - scrolly))
