import random
import pygame
import math
from resources import ITEMS, player_images, death_sound, polarbear_images, hurt_sound, crow_images, worm_head, worm_body, worm_tail
from settings import TILE_SIZE, BLACK, RED, GREEN, DISPLAY_WIDTH, DISPLAY_HEIGHT, WHITE
from functions import move, print_text

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
        self.chop(ITEMS[weapon]["image"])
        if abs(self.rect.centerx - mousex - world.scrollx) < 40 and abs(self.rect.centery - mousey - world.scrolly) < 40:
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
            inventory, tiles, mobs, drops, popups, slabs
        """
        
        # drop collisions
        for drop in list(world.drops):
            if self.rect.colliderect(drop.rect):
                world.popups.append(FadingText(self.rect.centerx, 
                                               self.rect.top, "+{} x {}".format(drop.amount, drop.item),
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
            else:
                self.rect.y += 3
        move(self, world, True)


    def draw(self, display, scrollx, scrolly):
        """
        draws the player character, health and chopping animation
        Args:
            display, scrollx, scrolly
        """
        # draw player to the screen
        display.blit(pygame.transform.flip(self.image, self.invert, 0), (self.rect.x-scrollx, self.rect.y-scrolly))
        # draw the health bar if health is below maximum
        if self.health < self.max_health:
            healthx = self.rect.centerx - self.max_health // 2 - scrollx
            healthy = self.rect.y - TILE_SIZE - scrolly
            for x in range(self.health):
                pygame.draw.line(display, GREEN, (healthx + x, healthy), (healthx + x, healthy+2), 1)
            healthx += self.health
            for x in range(self.max_health - self.health):
                pygame.draw.line(display, RED, (healthx + x, healthy), (healthx + x, healthy+2), 1)

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

class Particle():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.dx = random.randint(0, 10) / 10 - 1
        self.dy = random.randint(0, 10) / 10 - 1
        # both timer and radius for the particle
        self.timer = random.randint(1, 7)

    def update(self, display, particles, scrollx, scrolly):
        """
        Updates and draws the particle object
        Args:
            display, particles, scrollx, scrolly
        """
        self.x += self.dx
        self.y += self.dy
        self.y += 2
        self.timer -= 0.2
        pygame.draw.circle(display, self.color, (int(self.x - scrollx), int(self.y - scrolly)), int(self.timer))
        if self.timer <= 0:
            particles.remove(self)

class DroppedItem():
    """
    Object for drops that can be picked up by the player
    Args:
        x, y, dx, dy, item, amount=1
    """
    
    def __init__(self, x, y, dx, dy, item, amount=1):
        self.image = ITEMS[item]["image"]
        #if item in ["dirt", "stone", "plank", "plank wall", "rock"]:
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
        # only update movement if drop is in the screen
        # prevents them from falling off the map
        if self.rect.x - world.scrollx > 0 and self.rect.x - world.scrollx < DISPLAY_WIDTH and self.rect.y - world.scrolly > 0 and self.rect.y - world.scrolly < DISPLAY_HEIGHT:
            move(self, world)
            self.dy += self.gravity
            if self.collisions["down"]:
                self.dy = 0
                self.dx = 0

            if self.collisions["left"] or self.collisions["right"]:
                self.dx = 0

    def draw(self, display, scrollx, scrolly):
        display.blit(self.image, (self.rect.x - scrollx, self.rect.y - scrolly))

fadey = 0
class FadingText():
    """
    A fading text popup that appears above the player, rises and disappears
    """
    
    def __init__(self, x, y, text, current_biome=1, color=BLACK):
        global fadey
        self.x = x
        self.y = y - fadey
        self.size = 16
        self.text = text
        self.color = color
        if current_biome == 3 and color == BLACK:
            self.color = WHITE
        fadey += 10

    def update(self, popups):
        global fadey
        self.size -= 0.3
        self.y -= 2
        if self.size < 8:
            popups.remove(self)
            fadey -= 10

    def draw(self, display, scrollx, scrolly):
        print_text(self.text, int(self.x - scrollx), int(round(self.y) - scrolly), 
                   display, 1, int(round(self.size)), self.color)

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

    def draw(self, display, world):
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
                pygame.draw.line(display, GREEN, (healthx + x, healthy), (healthx + x, healthy+2), 1)
            healthx += self.health
            for x in range(self.max_health - self.health):
                pygame.draw.line(display, RED, (healthx + x, healthy), (healthx + x, healthy+2), 1)

class FlyingMob():
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.image = crow_images[0]
        self.imageindex = 0
        self.invert = 0
        self.anim_repeat = 20
        self.dx = 0
        self.dy = 0
        self.speed = 2
        self.max_speed = self.speed * 2
        self.dead = False
        self.max_health = 25
        self.health = self.max_health
        self.mobtype = 0
        self.collisions = {}

    def update(self, player, world):
        # despawning
        if self.rect.x < player.rect.x - 1000 or self.rect.x > player.rect.x + 1000:
            print("Bird despawned")
            world.entities.remove(self)
            world.mobs.remove(self)

        # death
        if self.health <= 0:
            for i in range(50):
                world.particles.append(Particle(self.rect.centerx, self.rect.centery, RED))
            world.drops.append(DroppedItem(self.rect.centerx, self.rect.centery, self.dx, self.dy, "meat"))
            world.mobs.remove(self)
            world.entities.remove(self)

        # animation
        self.anim_repeat -= 1
        if self.anim_repeat <= 0:
            self.anim_repeat = 20
            self.imageindex += 1
            if self.imageindex >= len(crow_images):
                self.imageindex = 0
            self.image = crow_images[self.imageindex]

        # movement
        move(self, world)

        if self.rect.x < player.rect.x and self.dx < self.speed:
            self.dx += 0.07
            self.invert = 1
        if self.rect.x > player.rect.x and self.dx > -self.speed:
            self.dx -= 0.07
            self.invert = 0

        if abs(player.rect.x - self.rect.x) > 100:
            if self.rect.y < player.rect.y - 100 and self.dy < self.speed:
                self.dy += 0.07
            if self.rect.y > player.rect.y - 100 and self.dy > -self.speed:
                self.dy -= 0.07
        else:
            if self.rect.y < player.rect.y - 25 and self.dy < self.speed:
                self.dy += 0.2
            if self.rect.y > player.rect.y - 25 and self.dy > -self.speed:
                self.dy -= 0.2

        if self.collisions["left"] or self.collisions["right"] and self.dx > -self.speed:
             self.dy -= 0.4

        if self.dx > self.max_speed:
            self.dx = self.max_speed
        if self.dx < -self.max_speed:
            self.dx = -self.max_speed
        if self.dy > self.max_speed:
            self.dy = self.max_speed
        if self.dy < -self.max_speed:
            self.dy = -self.max_speed

    def draw(self, display, world):
        display.blit(pygame.transform.flip(self.image, self.invert, 0), (self.rect.x - world.scrollx, self.rect.y - world.scrolly))

        if self.health != self.max_health:
            healthx = self.rect.centerx - self.max_health // 2 - world.scrollx
            healthy = self.rect.y - TILE_SIZE - world.scrolly
            for x in range(self.health):
                pygame.draw.line(display, GREEN, (healthx + x, healthy), (healthx + x, healthy+2), 1)
            healthx += self.health
            for x in range(self.max_health - self.health):
                pygame.draw.line(display, RED, (healthx + x, healthy), (healthx + x, healthy+2), 1)

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
            # agro to player primarily, but also attack other mobs if they happen to be in the caves
            if abs(player.rect.x - self.head_rect.x) < 300:
                self.target = player
                self.aggroed = True
            for mob in world.mobs:
                if abs(mob.rect.x - self.head_rect.x) < 300 and abs(mob.rect.y - self.head_rect.y) < 300:
                    self.target = mob
                    self.aggroed = True
                    break

    def draw(self, display, scrollx, scrolly):
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


