import pygame
from resources import arrow_image, hurt_sound
from settings import TILE_SIZE

class Arrow():
    """
    Arrow object
    """
    def __init__(self, x, y, dx, dy, enemy=False):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.rect.centerx = x
        self.rect.centery = y
        self.dx = dx
        self.dy = dy
        if self.dx < 0:
            self.original_image = pygame.transform.flip(arrow_image, 1, 0)
            self.left = True
        else:
            self.original_image = arrow_image
            self.left = False
        self.image = self.original_image

        self.gravity = 0.1
        self.grounded = False
        self.despawn_count = 0
        # damages player or mobs
        self.enemy = enemy
        self.damage = 5

    def update(self, world, player):
        remove = False
        if self.grounded == False:
            self.rect.x += self.dx
            self.rect.y += self.dy
            self.dy += self.gravity

            for tile in world.tiles:
                if tile.collidepoint(self.rect.center):
                    self.grounded = True

            if self.enemy:
                if self.rect.colliderect(player.rect):
                    player.health -= self.damage
                    hurt_sound.play()
                    remove = True
            else:
                for mob in world.mobs:
                    if self.rect.colliderect(mob.rect):
                        mob.health -= self.damage
                        hurt_sound.play()
                        remove = True

            # rotating arrow
            if self.left:
                if self.dx > self.dy:
                    self.image = pygame.transform.rotate(self.original_image, -45)
                elif -self.dx < self.dy * 2:
                    self.image = pygame.transform.rotate(self.original_image, 45)
                else:
                    self.image = self.original_image

            else:
                if -self.dx > self.dy:
                    self.image = pygame.transform.rotate(self.original_image, 45)
                elif self.dx < self.dy * 2:
                    self.image = pygame.transform.rotate(self.original_image, -45)
                else:
                    self.image = self.original_image
        else:
            self.despawn_count += 1
            if self.despawn_count >= 50:
                remove = True
        if remove and self in world.arrows:
            world.arrows.remove(self)

    def draw(self, display, world):
        display.blit(self.image, (self.rect.x-world.scrollx, self.rect.y-world.scrolly))

