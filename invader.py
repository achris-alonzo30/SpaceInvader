import pygame
import os
import random
from invader_bullet import InvaderBullet

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 700


# Initialize invader
class Invader:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 20, self.image.get_height() // 20))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.x_fractional = 0  # Fractional part of position
        self.speed = 0.2  # Adjust this value as needed
        self.point_value = 0

    def handle_movement(self):
        self.x_fractional += self.speed
        self.rect.x = int(self.x + self.x_fractional)
        if self.x_fractional >= 1:
            self.x += int(self.x_fractional)
            self.x_fractional -= int(self.x_fractional)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)


# Create rows of invaders
class Invaders:
    def __init__(self, invader_image, rows_count, player):
        self.invader_image = invader_image
        self.rows_count = rows_count
        self.direction = 0
        self.y = 40
        self.invaders = self.initialize_invaders()
        self.bullets = []
        self.speed = 0.2  # Initial speed
        self.last_bullet_time = 0
        self.bullet_delay = 1000
        self.point_value = 0
        self.speed_increase_timer = 0  # Timer to track speed increase
        self.speed_increase_interval = 45  # Increase score multiplier every 60 seconds
        self.score_multiplier_timer = 0
        self.player = player

    def handle_movement(self):
        for invader in self.invaders:
            if self.direction == 0:
                invader.speed = self.speed
            elif self.direction == 1:
                invader.speed = -self.speed

        if self.has_changed_direction():
            self.move_invader_down()

        for invader in self.invaders:
            invader.handle_movement()

        # Check if it's time to increase the speed
        current_time = pygame.time.get_ticks()
        if current_time - self.speed_increase_timer >= self.speed_increase_interval * 1000:
            self.speed += 0.5  # Increase speed by 0.1 units
            self.player.increase_score_multiplier(2)
            self.speed_increase_timer = current_time  # Reset the timer

    def has_changed_direction(self):
        for invader in self.invaders:
            if invader.rect.x >= SCREEN_WIDTH - 20:
                self.direction = 1
                return True
            elif invader.rect.x <= 0:
                self.direction = 0
                return True
        return False

    def move_invader_down(self):
        for invader in self.invaders:
            invader.rect.y += 3

    def initialize_invaders(self):
        invaders = []
        y = 40
        point_values = 5  # Point values for each row
        spacing_between_invaders = 50  # Increase the spacing to reduce the number of invaders

        for i in range(self.rows_count):
            if i == self.rows_count - 1:
                # Replace the last row with the new invader (invader2.png) worth 5 points
                for x in range(40, SCREEN_WIDTH - 40, spacing_between_invaders):
                    invader = Invader(x, y, os.path.join("static", "images", "invader2.png"))
                    invader.point_value = point_values
                    invaders.append(invader)
            else:
                # Use the original invader image (invader1.png) for other rows
                for x in range(40, SCREEN_WIDTH - 40, spacing_between_invaders):
                    invader = Invader(x, y, self.invader_image)
                    invader.point_value = point_values
                    invaders.append(invader)
            y += 40

        return invaders

    # Check if invader got hit by invader bullet
    def check_collision(self, beam_rect):
        invaders_to_remove = []  # Store all the invaders that got hit, to check the game if is over.

        for invader in self.invaders:
            if invader.rect.colliderect(beam_rect):
                invaders_to_remove.append(invader)

        for invader in invaders_to_remove:
            self.invaders.remove(invader)

        return len(invaders_to_remove) > 0

    def shoot_bottom_invaders(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_bullet_time >= self.bullet_delay:
            bottom_invaders = {}
            for invader in self.invaders:
                if invader.rect.bottom not in bottom_invaders:
                    bottom_invaders[invader.rect.bottom] = []

                bottom_invaders[invader.rect.bottom].append(invader)

            # Choose the invader in the last row to shoot
            last_row = max(bottom_invaders.keys())
            invader_to_shoot = bottom_invaders[last_row]

            num_bullets = random.randint(3, 6)

            # Ensure num_bullets is not greater than the number of invaders available in the last row
            num_bullets = min(num_bullets, len(invader_to_shoot))

            # Choose a random invader from the last row to shoot
            invaders_to_shoot = random.sample(invader_to_shoot, num_bullets)

            for invader in invaders_to_shoot:
                bullet_x = invader.rect.centerx
                bullet_y = invader.rect.bottom  # Use invader.rect.bottom as the bullet's y-coordinate
                bullet = InvaderBullet(bullet_x, bullet_y)  # Pass individual x and y coordinates
                self.bullets.append(bullet)

            # Adjust the delay for the next bullet
            self.last_bullet_time = current_time + self.bullet_delay

    def reset(self):
        self.direction = 0
        self.y = 40
        self.invaders = self.initialize_invaders()
        self.bullets = []
        self.speed = 0.2
        self.last_bullet_time = 0
