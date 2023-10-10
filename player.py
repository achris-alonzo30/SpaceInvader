import pygame
import os
import time

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 700


class Player:
    def __init__(self):
        self.image = pygame.image.load(os.path.join("static", "images", "player.png"))
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.centery = SCREEN_HEIGHT - 100
        self.speed = 2.0
        self.bullets = []
        self.lives = 3
        self.score = 0
        self.is_respawning = False  # Indicates if the player is currently respawning
        self.respawn_timer = 0  # Timer to track respawn duration
        self.respawn_duration = 2.0
        self.score_multiplier = 1
        self.is_visible = True

    def handle_movement(self):
        if not self.is_respawning:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed

            self.rect.x = max(self.rect.x, 0)
            self.rect.x = min(self.rect.x, SCREEN_WIDTH - self.rect.width)
        else:
            # Player is respawning, handle respawn timer
            current_time = time.time()
            if current_time - self.respawn_timer >= self.respawn_duration:
                # Respawn duration has passed, end respawning
                self.is_respawning = False
            else:
                # Toggle player visibility (blink) at a certain frequency
                blink_interval = 0.2  # Adjust the interval as needed
                if (current_time - self.respawn_timer) % (2 * blink_interval) < blink_interval:
                    self.is_visible = True
                else:
                    self.is_visible = False

    def draw(self, screen):
        if not self.is_respawning or self.is_visible:
            screen.blit(self.image, self.rect.topleft)

    def respawn(self):
        # Reset player position to the center bottom of the screen
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.centery = SCREEN_HEIGHT - 100

        # Decrement player lives
        self.lives -= 1

        # Set respawn timer and flag
        self.respawn_timer = time.time()
        self.is_respawning = True

    def increase_score_multiplier(self, multiplier):
        self.score_multiplier *= multiplier

    def reset(self):
        # Reset player position to the center bottom of the screen
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.centery = SCREEN_HEIGHT - 100
