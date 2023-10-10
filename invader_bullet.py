import pygame
from player import Player

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 700

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.rect(screen, (119, 201, 20), (self.x, self.y, 3, 10))


class InvaderBullet(Bullet):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, 3, 10)  # Create a rect attribute for collision detection

    def handle_movement(self):
        self.y += 2
        self.rect.topleft = (self.x, self.y)  # Update the rect's position
