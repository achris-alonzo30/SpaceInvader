import pygame


class Beam:
    def __init__(self, player_rect):
        self.image = pygame.Surface((5, 20))
        self.image.fill((115, 4, 215))
        self.rect = self.image.get_rect()
        self.rect.centerx = player_rect.centerx
        self.rect.centery = player_rect.top
        self.active = True

    def handle_movement(self):
        if self.active:  # Check to see if beam is active then it will move upwards.
            self.rect.y -= 5
            if self.rect.y < 0:  # If beam is passed of the screen then beam is not active.
                self.active = False
