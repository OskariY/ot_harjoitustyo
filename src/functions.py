import noise
import random
import pygame
from settings import BLACK, BLUE, BROWN, GRAY, BROWN, GRASSGREEN, FONT, TILE_SIZE, CHUNK_SIZE
from resources import ITEMS, break_sound, build_sound

def print_text(text, x, y, display, allignment=0, size=32, color=BLACK):
    """
    Prints text onto the screen
    allignments: 0=left, 1=center, 2=right
    Args:
        text, x, y, display, allignment=0, size=32, color=BLACK
    """
    font = pygame.font.SysFont(FONT, size)
    surf = font.render(text, False, color)
    if allignment == 1:
        x = x - surf.get_width() / 2
    elif allignment == 2:
        x = x - surf.get_width()
    display.blit(surf, (x, y))

def move(rect, dx, dy, world):
    """Moves a pygame rectangle

    Args:
        rect, tiles, dx, dy, slabs=[], entities=[]
    Returns:
        rect, collisions

    """

    collisions = {
            "right": False,
            "left": False,
            "up": False,
            "down": False,
            }
    # move horizontally and check for collisions
    rect.x += dx
    for tile in world.tiles:
        if rect.colliderect(tile):
            if not tile in world.slabs:
                if dx > 0:
                    rect.right = tile.left
                    collisions["right"] = True
                if dx < 0:
                    rect.left = tile.right
                    collisions["left"] = True
    for entity in world.entities:
        if rect.colliderect(entity):
            if dx > 0:
                rect.x -= dx
            if dx < 0:
                rect.y += dx
    # move vertically and check for collisions
    rect.y += dy
    for tile in world.tiles:
        if rect.colliderect(tile):
            if dy > 0:
                rect.bottom = tile.top
                collisions["down"] = True
            if dy < 0:
                if not tile in world.slabs:
                    rect.top = tile.bottom
                    collisions["up"] = True

    return rect, collisions

