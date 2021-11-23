from resources import *
from settings import *
from functions import *

class Player():
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.hitrect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

        self.original_image = player_image1
        self.image = player_image1
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

    def update(self, scrollx, scrolly, tiles, mobs, drops, popups, slabs):
        """
        player.update: updates the player object

        Args:
            scrollx, scrolly, tiles, mobs, drops, popups, slabs
        Returns:
            None

        """

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
            self.rect.x = spawn_x
            self.rect.y = spawn_y
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
        display.blit(pygame.transform.flip(self.image, self.invert, 0), (self.rect.x-scrollx, self.rect.y-scrolly))
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
