import math
import random
import pygame
from settings import TILE_SIZE, GREEN, RED
from entities.particle import Particle
from entities.drop import DroppedItem
from resources import worm_head, worm_body, worm_tail

class Worm():
    """
    Caveworm object
    the worm is made up of three types of rects: the head, body (list of rects) and the tail
    """
    def __init__(self, x, y):
        # differences between drawn images and rects
        # this is necesseary to remove gaps between the different worm parts
        # that would otherwise form
        self.margin = 4
        # head
        self.head_rect = pygame.Rect(x, y, TILE_SIZE - self.margin, TILE_SIZE - self.margin)
        self.head_image = worm_head
        self.head_angle = math.radians(-90)

        # body
        self.body_rects = []
        self.body_images = []
        self.body_angles = []
        for i in range(7):
            y += TILE_SIZE
            self.body_images.append(worm_body)
            self.body_rects.append(pygame.Rect(x, y, TILE_SIZE - self.margin, TILE_SIZE - self.margin))
            self.body_angles.append(math.radians(-90))

        # tail
        self.tail_rect = pygame.Rect(x, y+TILE_SIZE, TILE_SIZE - self.margin, TILE_SIZE - self.margin)
        self.tail_image = worm_tail
        self.tail_angle = math.radians(-90)

        self.speed = 2
        self.body_speed = self.speed + 1
        self.aggroed = False
        self.target = None
        self.direction = "right"
        self.max_health = 100
        self.health = self.max_health

    def update(self, player, world):
        # despawn if player is too far
        if abs(player.rect.x - self.head_rect.x) > 1000 and abs(player.rect.y - self.head_rect.y) > 1000:
            world.worms.remove(self)
        # death
        if self.health <= 0:
            world.drops.append(DroppedItem(self.head_rect.centerx, self.head_rect.centery,
                                           0, 0, "meat", random.randint(1, 10)))
            for i in range(100):
                world.particles.append(Particle(self.head_rect.centerx, self.head_rect.centery, RED))
            world.worms.remove(self)

        if self.aggroed:
            if self.head_rect.colliderect(player.rect):
                player.health -= 5
                if self.direction == "right":
                    player.dx += 10
                    player.dy -= 5
                else:
                    player.dx -= 10
                    player.dy -= 5

            if self.target != player:
                if not self.target in world.mobs:
                    self.aggroed = False
                    self.target = None

            if self.target != None:
                # head movement
                distance_x = self.target.rect.x - self.head_rect.x
                distance_y = self.target.rect.y - self.head_rect.y
                self.head_angle = math.atan2(distance_y, distance_x)
                speed_x = self.speed * math.cos(self.head_angle)
                speed_y = self.speed * math.sin(self.head_angle)
                self.head_rect.x += round(speed_x)
                self.head_rect.y += round(speed_y)
                if speed_x > 0:
                    self.direction = "right"
                else:
                    self.direction = "left"

                # body movement
                for i, body in enumerate(self.body_rects):
                    if i == 0:
                        distance_x = self.head_rect.x - body.x
                        distance_y = self.head_rect.y - body.y
                    else:
                        distance_x = self.body_rects[i-1].x - body.x
                        distance_y =self.body_rects[i-1].y - body.y
                    self.body_angles[i] = math.atan2(distance_y, distance_x)
                    speed_x = self.body_speed * math.cos(self.body_angles[i])
                    speed_y = self.body_speed * math.sin(self.body_angles[i])
                    if i == 0:
                        if not body.colliderect(self.head_rect):
                            body.x += round(speed_x)
                            body.y += round(speed_y)
                    else:
                        if not body.colliderect(self.body_rects[i-1]):
                            body.x += round(speed_x)
                            body.y += round(speed_y)

                # tail movement
                distance_x = self.body_rects[-1].x - self.tail_rect.x
                distance_y = self.body_rects[-1].y - self.tail_rect.y
                self.tail_angle = math.atan2(distance_y, distance_x)
                speed_x = self.body_speed * math.cos(self.tail_angle)
                speed_y = self.body_speed * math.sin(self.tail_angle)
                if not self.tail_rect.colliderect(self.body_rects[-1]):
                    self.tail_rect.x += round(speed_x)
                    self.tail_rect.y += round(speed_y)
        else:
            if abs(player.rect.x - self.head_rect.x) < 300:
                self.target = player
                self.aggroed = True

    def draw(self, display, scrollx, scrolly): # pragma: no cover
        display.blit(pygame.transform.rotate(self.head_image, math.degrees(-self.head_angle) - 90), (self.head_rect.x-scrollx-self.margin//2, self.head_rect.y-scrolly-self.margin//2))
        for i, image in enumerate(self.body_images):
            display.blit(pygame.transform.rotate(image, math.degrees(-self.body_angles[i]) - 90), (self.body_rects[i].x - scrollx-self.margin//2, self.body_rects[i].y - scrolly-self.margin//2))
        display.blit(pygame.transform.rotate(self.tail_image, math.degrees(-self.tail_angle) - 90), (self.tail_rect.x - scrollx-self.margin//2, self.tail_rect.y - scrolly-self.margin//2))
        if self.health < self.max_health:
            healthx = self.head_rect.centerx - self.max_health // 2 - scrollx
            healthy = self.head_rect.y - TILE_SIZE*2 - scrolly
            for x in range(self.health):
                pygame.draw.line(display, GREEN, (healthx + x, healthy), (healthx + x, healthy+2), 1)
            healthx += self.health
            for x in range(self.max_health - self.health):
                pygame.draw.line(display, RED, (healthx + x, healthy), (healthx + x, healthy+2), 1)


