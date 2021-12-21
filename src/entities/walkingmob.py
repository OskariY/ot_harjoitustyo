import random
import pygame
from resources import polarbear_images, zombie_walking, skeleton_images
from entities.drop import DroppedItem
from entities.particle import Particle
from settings import TILE_SIZE, DISPLAY_WIDTH, DISPLAY_HEIGHT, GREEN, RED
from functions import move, draw_health_bar

class WalkingMob():
    """
    Class for a mob that tries to walk towards the player and cause damage
    the mobtype parameter allows for adding other mobs with the same "AI",
    but different textures.
    """
    def __init__(self, x, y, mobtype="bear"):
        self.images = polarbear_images
        self.animation_repeat = 10
        if mobtype == "skeleton":
            self.images = skeleton_images
            self.anim_repeat = 20
        if mobtype == "zombie":
            self.images = zombie_walking
            self.anim_repeat = 15
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.mobtype = mobtype # makes retextured mobs with same logic possible
        self.inverse = 0 # which way the mob is facing

        self.image_index = 0
        self.animation_counter = 0

        self.aggroed = False
        self.speed = 1
        self.max_speed = 3
        self.dx = 0
        self.dy = 0
        self.jumppower = 7
        self.jumps = 1
        self.gravity = 0.4
        self.max_gravity = 8

        self.max_health = 50
        self.health = self.max_health

        self.collisions = {
            "right": False,
            "left": False,
            "up": False,
            "down": False,
            }

    def update(self, player, world):
        """
        Updates the WalkingMob object, handling things like movement, health and aggression
        to the player
        """
        if abs(self.rect.x - player.rect.x) > 700 or abs(self.rect.y < player.rect.y) > 700:
            world.mobs.remove(self)
            world.entities.remove(self)

        if self.health <= 0:
            # blood particles
            for i in range(40):
                world.particles.append(Particle(self.rect.centerx, self.rect.centery, RED))
            world.drops.append(DroppedItem(self.rect.x, self.rect.y,
                                           self.dx, self.dy, "meat", random.randint(1, 5)))

            world.mobs.remove(self)
            world.entities.remove(self)
        # animation
        self.animation_counter += 1
        if self.animation_counter == self.animation_repeat:
            self.animation_counter = 0
            self.image_index += 1
            if self.image_index > len(self.images) - 1:
                self.image_index = 0
            self.image = self.images[self.image_index]

        # aggro to player
        if self.rect.right > world.scrollx or self.rect.left < DISPLAY_WIDTH + world.scrollx:
            self.aggroed = True
        self._move(player, world)

    def _move(self, player, world):
        # movement
        if self.rect.centerx < player.rect.centerx - TILE_SIZE:
            if self.dx < self.speed:
                self.dx += 0.5
            if self.mobtype == "bear":
                self.inverse = 1
            else:
                self.inverse = 0
        elif self.rect.centerx > player.rect.centerx + TILE_SIZE:
            if self.dx > -self.speed:
                self.dx -= 0.5
            if self.mobtype == "bear":
                self.inverse = 0
            else:
                self.inverse = 1
        # hard speed gap
        if self.dx > self.max_speed:
            self.dx = self.max_speed
        if self.dx < -self.max_speed:
            self.dx = -self.max_speed

        # soft speed gap
        if self.dx > self.speed:
            self.dx -= 0.1
        if self.dx < -self.speed:
            self.dx += 0.1

        move(self, world, True)

        if self.collisions["left"] or self.collisions["right"]:
            if self.jumps:
                self.dy = -self.jumppower
                self.jumps = 0

        if self.collisions["down"]: # gravity
            self.dy = 0
            self.jumps = 1
        else:
            if (self.rect.y-world.scrolly) < DISPLAY_HEIGHT:
                if self.dy < self.max_gravity:
                    self.dy += self.gravity

    def draw(self, display, world): # pragma: no cover
        """
        Draws the mob and a health bar if it has taken damage
        """
        drawx = self.rect.x-world.scrollx
        drawy = self.rect.y-world.scrolly

        # flip the image if needed and make it transparent
        image = pygame.transform.flip(self.image, self.inverse, 0)
        image.set_colorkey(GREEN)
        display.blit(image, (drawx, drawy))

        draw_health_bar(self.rect.centerx-world.scrollx, self.rect.y-TILE_SIZE-world.scrolly,
                        display, self.health, self.max_health)
