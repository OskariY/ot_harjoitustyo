import random
import pygame
from resources import polarbear_images
from entities.drop import DroppedItem
from entities.particle import Particle
from settings import TILE_SIZE, DISPLAY_WIDTH, DISPLAY_HEIGHT, GREEN, RED
from functions import move

class WalkingMob():
    def __init__(self, x, y, mobtype="bear"):
        self.images = polarbear_images
        self.animation_repeat = 10
        if mobtype == "skeleton":
            self.images = skeleton_images
            self.anim_repeat = 20
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
        if abs(self.rect.x - player.rect.x) > 700 or abs(self.rect.y < player.rect.y) > 700:
            world.mobs.remove(self)

        if self.health <= 0:
            # blood particles
            for i in range(40):
                world.particles.append(Particle(self.rect.centerx, self.rect.centery, RED))
            world.drops.append(DroppedItem(self.rect.x, self.rect.y,
                                           self.dx, self.dy, "meat", random.randint(1, 5)))

            world.mobs.remove(self)
            world.entities.remove(self)
        else:
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

            # movement
            if self.aggroed:
                if self.rect.centerx < player.rect.centerx - TILE_SIZE:
                    if self.dx < self.speed:
                        self.dx += 0.5
                    self.inverse = 1
                elif self.rect.centerx > player.rect.centerx + TILE_SIZE:
                    if self.dx > -self.speed:
                        self.dx -= 0.5
                    self.inverse = 0
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
        drawx = self.rect.x-world.scrollx
        drawy = self.rect.y-world.scrolly

        # flip the image if needed and make it transparent
        image = pygame.transform.flip(self.image, self.inverse, 0)
        image.set_colorkey(GREEN)
        display.blit(image, (drawx, drawy))

        # draw health
        if self.health != self.max_health:
            healthx = self.rect.centerx - self.max_health // 2 - world.scrollx
            healthy = self.rect.y - TILE_SIZE - world.scrolly
            for x in range(self.health):
                pygame.draw.line(display, GREEN, (healthx + x, healthy),
                                 (healthx + x, healthy+2), 1)
            healthx += self.health
            for x in range(self.max_health - self.health):
                pygame.draw.line(display, RED, (healthx + x, healthy),
                                 (healthx + x, healthy+2), 1)


