import math
import pygame
from settings import TILE_SIZE, GREEN, RED
from resources import player_images, ITEMS, hurt_sound, death_sound
from entities.fadingtext import FadingText
from functions import move, draw_health_bar

class Player():
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.hitrect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

        self.original_image = player_images[0]
        self.image = self.original_image
        self.collisions = {
            "right": False,
            "left": False,
            "up": False,
            "down": False,
            }
        self.moving_right = False
        self.moving_left = False
        self.dx = 0
        self.dy = 0
        self.jumps = 2
        self.speed = 2
        self.max_speed = 10
        self.gravity = 0.4
        self.max_gravity = 8
        self.jump_power = 7
        self.max_health = 50
        self.health = self.max_health
        self.invert = 0

        self.walkcount = 0
        self.i = 0
        self.sound_cooldown = 0

        # chopping animation variables
        self.chopping_animation = 0
        self.chopping_rotation = 0
        self.chopping_image = None

        self.falling = False

    def chop(self, image):
        self.chopping_animation = 10
        self.chopping_rotation = 10
        self.chopping_image = image

    def hit(self, weapon, world, mousex, mousey):
        """
        Invokes the chopping animation and "hits" towards the direction of the mouse
        by placing an invisible rectangle towards the mouse and checking for collisions
        with mobs
        """
        self.chop(ITEMS[weapon]["image"])
        if abs(self.rect.centerx - mousex - world.scrollx) < 40 \
                and abs(self.rect.centery - mousey - world.scrolly) < 40:
            self.hitrect.centerx = mousex+world.scrollx
            self.hitrect.centery = mousey+world.scrolly
        else:
            distance_x = mousex - self.rect.centerx + world.scrollx
            distance_y = mousey - self.rect.centery + world.scrolly

            angle = math.atan2(distance_y, distance_x)
            self.hitrect.centerx = self.rect.centerx
            self.hitrect.centery = self.rect.centery
            self.hitrect.centerx += 40 * math.cos(angle)
            self.hitrect.centery += 40 * math.sin(angle)

        for mob in world.mobs:
            if mob.rect.colliderect(self.hitrect):
                hurt_sound.play()
                mob.health -= 5
                if mousex+world.scrollx > self.rect.centerx:
                    mob.dx += 5
                else:
                    mob.dx -= 5
                mob.dy -= 3
        for worm in world.worms:
            hit = False
            if worm.head_rect.colliderect(self.hitrect):
                hurt_sound.play()

                hit = True
            for wormbody in worm.body_rects:
                if wormbody.colliderect(self.hitrect):
                    hurt_sound.play()
                    hit = True
            if hit:
                worm.health -= 5
        # self.hitrect.x -= scrollx
        # self.hitrect.y -= scrolly
        # pygame.draw.rect(display, RED, self.hitrect)

    def update(self, inventory, world):
        """
        updates the player object

        Args:
            inventory, world
        """

        # drop collisions
        for drop in list(world.drops):
            if self.rect.colliderect(drop.rect):
                world.popups.append(FadingText(self.rect.centerx,
                                               self.rect.top, "+{} x {}".format(drop.amount,
                                                                                drop.item),
                                               world.current_biome))
                inventory.add_to_inventory(drop.item, drop.amount)
                world.drops.remove(drop)

        if self.sound_cooldown > 0:
            self.sound_cooldown -= 1

        if not self.moving_right and not self.moving_left:
            if self.dx > 0:
                self.dx -= 1
            elif self.dx < 0:
                self.dx += 1

        if self.dx > self.max_speed:
            self.dx = self.max_speed
        if self.dx < -self.max_speed:
            self.dx = -self.max_speed
        if self.dy > self.max_speed:
            self.dy = self.max_speed
        if self.dy < -self.max_speed:
            self.dy = -self.max_speed

        # left-right movement
        if self.moving_right:
            if self.dx < self.speed:
                self.dx += 1
            elif self.dx > self.speed:
                self.dx -= 1

        if self.moving_left:
            if self.dx > -self.speed:
                self.dx -= 1
            elif self.dx < -self.speed:
                self.dx += 1

        if self.dx != 0:
            self.walkcount += 1
            if self.walkcount >= 10:
                self.walkcount = 0
                self.i += 1
                if self.i > 1:
                    self.i = 0
                self.image = player_images[self.i]

        # death
        if self.health <= 0:
            death_sound.play()
            self.rect.x = 0
            self.rect.y = -100
            self.health = self.max_health

        # gravity and falling
        if self.collisions["down"] == False: # gravity
            if self.dy < self.max_gravity:
                self.dy += self.gravity

        if self.collisions["down"] and self.dy > 0:
            self.jumps = 2 # reset jumps if ycollide is true
            self.dy = 0
        if self.collisions["up"] and self.dy < 0:
            self.dy = 0

        # movement function
        if self.falling:
            self.rect.y += 1
            if self.rect.collidelist(world.slabs) == -1:
                self.falling = False
                self.rect.y -= 1
            else:
                self.rect.y += 3
        else:
            move(self, world, True)


    def draw(self, display, scrollx, scrolly): # pragma: no cover
        """
        draws the player character, health and chopping animation
        Args:
            display, scrollx, scrolly
        """
        # draw player to the screen
        display.blit(pygame.transform.flip(self.image, self.invert, 0), (self.rect.x-scrollx, self.rect.y-scrolly))
        # draw the health bar if health is below maximum
        draw_health_bar(self.rect.centerx-scrollx, self.rect.y-TILE_SIZE-scrolly,
                        display, self.health, self.max_health)

        # chopping animation
        if self.chopping_animation > 0:
            self.chopping_animation -= 1
            if self.chopping_animation in [7, 4]:
                self.chopping_rotation += 20
            if self.invert:
                rot = self.chopping_rotation
                chopx = self.rect.x-scrollx - 4
            else:
                rot = -self.chopping_rotation
                chopx = self.rect.x-scrollx + 2
            chopy = self.rect.y-scrolly
            display.blit(pygame.transform.rotate(pygame.transform.flip(self.chopping_image, self.invert, 0), rot), (chopx, chopy))
