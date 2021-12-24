import math
import pygame
from settings import TILE_SIZE
from resources import player_standing, player_walking, ITEMS, hurt_sound, death_sound, \
                      player_hand, player_hand_straight, tonttulakki
from entities.fadingtext import FadingText
from functions import move, draw_health_bar

class Player():
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, 2*TILE_SIZE)
        self.hitrect = pygame.Rect(x, y, 2*TILE_SIZE, 2*TILE_SIZE)

        self.image = player_standing
        self.hand_image = player_hand
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
        # hand rotation
        self.hand1_angle = -90
        self.hand2_angle = 0
        self.hand1_pos = -6
        self.hand2_pos = 0

        # chopping animation variables
        self.chopping_animation = 0
        self.chopping_rotation = 0
        self.chopping_image = None

        self.falling = False

    def chop(self):
        self.chopping_animation = 10
        self.chopping_rotation = 10

    def hit(self, world, mousex, mousey):
        """
        Invokes the chopping animation and "hits" towards the direction of the mouse
        by placing an invisible rectangle towards the mouse and checking for collisions
        with mobs
        """
        self.chop()
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

    def _move(self, world):
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

        # gravity and falling
        if self.collisions["down"] is False: # gravity
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
            slab_collide = self.rect.collidelist(world.slabs)
            if slab_collide == -1:
                self.falling = False
                self.rect.y -= 1
            else:
                self.rect.x = world.slabs[slab_collide].x
                self.rect.y += 1
                if self.collisions["down"]:
                    self.rect.bottom = world.slabs[slab_collide].y
                    self.falling = False
                else:
                    move(self, world, True, True)
        else:
            move(self, world, True)

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
                                               world))
                inventory.add_to_inventory(drop.item, drop.amount)
                world.drops.remove(drop)

        if self.sound_cooldown > 0:
            self.sound_cooldown -= 1


        # death
        if self.health <= 0:
            death_sound.play()
            self.rect.x = 0
            self.rect.y = -100
            self.health = self.max_health

        self._move(world)
        self._animation()

    def _animation(self): # pragma: no cover
        """
        changes the player images to create the appearence of a running animation
        """
        if self.dx != 0:
            self.walkcount += 1
            if self.walkcount >= 10:
                self.walkcount = 0
                self.i += 1
                if self.i > 2:
                    self.i = 0
                self.image = player_walking[self.i]
                self.hand_image = player_hand
                if self.i == 0:
                    self.hand1_angle = 0
                    self.hand2_angle = -90
                    if self.invert:
                        self.hand1_pos = -6
                        self.hand2_pos = 0
                    else:
                        self.hand1_pos = 0
                        self.hand2_pos = -6
                elif self.i == 1:
                    self.hand1_angle = -45
                    self.hand2_angle = -45
                    self.hand1_pos = -5
                    self.hand2_pos = -5
                elif self.i == 2:
                    self.hand1_angle = -90
                    self.hand2_angle = 0
                    if self.invert:
                        self.hand1_pos = 0
                        self.hand2_pos = -6
                    else:
                        self.hand1_pos = -6
                        self.hand2_pos = 0
                if self.invert:
                    self.hand1_angle = -self.hand1_angle
                    self.hand2_angle = -self.hand2_angle
        else:
            self.image = player_standing
            self.hand_image = player_hand_straight
            self.hand1_angle = 0
            self.hand2_angle = 0
            self.hand1_pos = -5
            self.hand2_pos = -5
            if self.invert:
                self.hand2_pos += 1

    def draw(self, display, world, inventory): # pragma: no cover
        """
        draws the player character, health and chopping animation
        """

        # draw the health bar if health is below maximum
        draw_health_bar(self.rect.centerx-world.scrollx, self.rect.y-TILE_SIZE-world.scrolly,
                        display, self.health, self.max_health)

        hand_x, hand_y = self.rect.x-world.scrollx+7, self.rect.y-world.scrolly+10
        hand1 = pygame.transform.flip(self.hand_image, self.invert, 0)
        hand1 = pygame.transform.rotate(hand1, self.hand1_angle)
        display.blit(hand1, (hand_x+self.hand1_pos, hand_y))

        # draw player to the screen
        display.blit(pygame.transform.flip(self.image, self.invert, 0),
                     (self.rect.x-world.scrollx, self.rect.y-world.scrolly))

        # draw tonttulakki (important)
        display.blit(pygame.transform.flip(tonttulakki, self.invert, 0),
                     (self.rect.x-world.scrollx, self.rect.y-world.scrolly-TILE_SIZE+1))

        # chopping animation
        if self.chopping_animation > 0:
            self.chopping_animation -= 1
            self.chopping_rotation += 2
            self.hand_image = player_hand
            hand2 = pygame.transform.flip(self.hand_image, self.invert, 0)
            if self.invert:
                rot = self.chopping_rotation
                hand2 = pygame.transform.rotate(hand2, 45+self.chopping_rotation)
                self.hand2_pos = -4
                chopx = self.rect.x - world.scrollx - 9 + self.chopping_animation // 3
            else:
                rot = -self.chopping_rotation
                hand2 = pygame.transform.rotate(hand2, -45-self.chopping_rotation)
                self.hand2_pos = -4
                chopx = self.rect.x - world.scrollx + 5 - self.chopping_animation // 3
            chopy = self.rect.y-world.scrolly+2
            if inventory.equipped != "":
                item = pygame.transform.flip(ITEMS[inventory.equipped]["image"], self.invert, 0)
                if ITEMS[inventory.equipped]["tool"]:
                    display.blit(pygame.transform.rotate(item, rot), (chopx, chopy))
            display.blit(hand2, (hand_x+self.hand2_pos, hand_y))
        else:
            hand2 = pygame.transform.flip(self.hand_image, self.invert, 0)
            hand2 = pygame.transform.rotate(hand2, self.hand2_angle)
            display.blit(hand2, (hand_x+self.hand2_pos, hand_y))
