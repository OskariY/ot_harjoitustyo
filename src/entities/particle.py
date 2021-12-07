import random
import pygame

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

