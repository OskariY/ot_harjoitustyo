import pygame
import random
from resources import ITEMS, player_images, death_sound
from settings import TILE_SIZE, BLACK, RED, GREEN, DISPLAY_WIDTH, DISPLAY_HEIGHT
from functions import move, print_text, add_to_inventory

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

    def update(self, inventory, tiles, mobs, drops, popups, slabs):
        """
        updates the player object

        Args:
            inventory, tiles, mobs, drops, popups, slabs
        """
        
        # drop collisions
        for drop in list(drops):
            if self.rect.colliderect(drop.rect):
                popups.append(FadingText(self.rect.centerx, self.rect.top, "+{} x {}".format(drop.amount, drop.item)))
                add_to_inventory(inventory, drop.item, drop.amount)
                drops.remove(drop)



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
            if self.rect.collidelist(slabs) == -1:
                self.falling = False
            else:
                self.rect.y += 3
        else:
            self.rect, self.collisions = move(self.rect, self.dx, self.dy, tiles, slabs)


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
        if item in ["dirt", "stone", "plank", "plank wall", "rock"]:
            self.image = pygame.transform.scale(self.image, (8, 8))
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.item = item
        self.dx = dx
        self.dy = dy
        self.gravity = 0.4
        self.amount = amount

    def update(self, tiles, scrollx, scrolly):
        # only update movement if drop is in the screen
        # prevents them from falling off the map
        if self.rect.x - scrollx > 0 and self.rect.x - scrollx < DISPLAY_WIDTH and self.rect.y - scrolly > 0 and self.rect.y - scrolly < DISPLAY_HEIGHT:
            self.rect, collide = move(self.rect, self.dx, self.dy, tiles)
            self.dy += self.gravity
            if collide["down"]:
                self.dy = 0
                self.dx = 0

            if collide["left"] or collide["right"]:
                self.dx = 0

    def draw(self, display, scrollx, scrolly):
        display.blit(self.image, (self.rect.x - scrollx, self.rect.y - scrolly))

fadey = 0
class FadingText():
    """
    A fading text popup that appears above the player, rises and disappears
    Args:
        x, y, text, color=BLACK
    """
    
    def __init__(self, x, y, text, color=BLACK):
        global fadey
        self.x = x
        self.y = y - fadey
        self.size = 16
        self.text = text
        self.color = color
        #if current_biome == 3 or is_night == True and color == BLACK:
        #    self.color = WHITE
        fadey += 10

    def update(self, popups):
        global fadey
        self.size -= 0.3
        self.y -= 2
        if self.size < 8:
            popups.remove(self)
            fadey -= 10

    def draw(self, display, scrollx, scrolly):
        print_text(self.text, int(self.x - scrollx), int(round(self.y) - scrolly), display, 1, int(round(self.size)), self.color)
