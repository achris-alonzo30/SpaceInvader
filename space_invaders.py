import pygame
import sys
import os
import time
import random
from player import Player
from invader import Invaders
from player_bullet import Beam

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 700
FPS = 60
CIRCLE_GENERATE_INTERVAL = 3000

# Create the Pygame clock and screen
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")


# Function to generate random circles for background
def generate_circles():
    circle_x = random.randint(0, SCREEN_WIDTH)
    circle_y = 0
    circle_radius = 2
    circle_velocity_x = 0
    circle_velocity_y = random.uniform(0.1, 0.1)  # Vertical velocity (slower)
    return circle_x, circle_y, circle_radius, circle_velocity_x, circle_velocity_y


def main():
    # Initialize the game objects
    player = Player()
    invaders = Invaders(os.path.join("static", "images", "invader1.png"), 3, player)
    beams = []  # Store player bullets
    circles = []  # Store circles
    last_circle_generate_time = 0  # Initialize the last circle generation time
    shooting_cooldown = False
    cooldown_start_time = 0
    cooldown_duration = 2.0
    life_display_x = 10
    life_display_y = SCREEN_HEIGHT - 40

    # Load player life images
    player_life_images = [
        pygame.transform.scale(pygame.image.load(os.path.join("static", "images", "life.png")), (30, 30))
        for _ in range(player.lives)]

    # Game loop
    running = True
    while running:
        clock.tick(FPS)
        current_time = pygame.time.get_ticks()  # Get the current time
        screen.fill((0, 0, 0))

        # Draw the player's score
        font = pygame.font.Font(None, 25)
        text = font.render(f"SCORE: {player.score}", True, (119, 201, 20))
        screen.blit(text, (475, SCREEN_HEIGHT - 25))

        # Draw player and beams
        player.draw(screen)

        for beam in beams:
            screen.blit(beam.image, beam.rect.topleft)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not shooting_cooldown:
                    beam = Beam(player.rect)  # So the player bullet will come out in the middle of the player and the current location.
                    beams.append(beam)
                    shooting_cooldown = True
                    cooldown_start_time = time.time()

        # Generate new circles at the specified interval
        if current_time - last_circle_generate_time >= CIRCLE_GENERATE_INTERVAL:
            circles.append(generate_circles())
            last_circle_generate_time = current_time  # Update the last circle generation time

        # Update player and beams
        player.handle_movement()

        # Initialize beam
        for beam in beams:
            beam.handle_movement()
            # Once beam hits an invader player scores.
            if invaders.check_collision(beam.rect):
                player.score += invader.point_value * player.score_multiplier
                beam.active = False

        # This will remove the beam once it hits an invader.
        beams = [beam for beam in beams if beam.active]

        # Collision detection between player bullets and invader bullets
        for player_bullet in player.bullets:
            for invader_bullet in invaders.bullets:
                if player_bullet.rect.colliderect(invader_bullet.rect):
                    player.bullets.remove(player_bullet)
                    invaders.bullets.remove(invader_bullet)

        # Draw player lives
        for i, life_image in enumerate(player_life_images):
            life_rect = life_image.get_rect()
            life_rect.topleft = (life_display_x + i * (life_rect.width + 16), life_display_y)
            screen.blit(life_image, life_rect.topleft)

        # Update and draw circles
        updated_circles = []
        for circle in circles:
            circle_x, circle_y, circle_radius, circle_velocity_x, circle_velocity_y = circle

            # Update circle position
            circle_x += circle_velocity_x
            circle_y += circle_velocity_y

            # Remove circles that go beyond the screen's bottom edge
            if circle_y < SCREEN_HEIGHT:
                updated_circles.append((circle_x, circle_y, circle_radius, circle_velocity_x, circle_velocity_y))

            # Draw the circle with the specified color
            circle_color = (127, 127, 127)
            pygame.draw.circle(screen, circle_color, (int(circle_x), int(circle_y)), circle_radius)

        circles = updated_circles

        # Update and draw the invaders
        invaders.handle_movement()
        if invaders.has_changed_direction():
            invaders.move_invader_down()
            invaders.shoot_bottom_invaders()

        for invader in invaders.invaders:
            invader.draw(screen)
            if invader.rect.colliderect(player.rect):
                # Handle invader reaching the player's position
                running = False  # End the game as the invader reached the player
                break

        if not invaders.invaders:
            # All invaders defeated, restart the game
            player.reset()  # Reset player attributes
            invaders.reset()  # Reset invaders
            circles = []  # Clear circles

            # Display "GAME OVER" in the center of the screen
            font = pygame.font.Font(None, 50)
            game_over_text = font.render("GAME OVER", True, (119, 201, 20))
            text_x = (SCREEN_WIDTH - game_over_text.get_width()) // 2
            text_y = (SCREEN_HEIGHT - game_over_text.get_height()) // 2

            # Create a border around the "GAME OVER" text
            border_width = game_over_text.get_width() + 20
            border_height = game_over_text.get_height() + 20
            border_surface = pygame.Surface((border_width, border_height), pygame.SRCALPHA)
            pygame.draw.rect(border_surface, (0, 0, 0), (0, 0, border_width, border_height))
            pygame.draw.rect(border_surface, (119, 201, 20), (2, 2, border_width - 4, border_height - 4), 2)

            # Calculate the position of the border to center it with the text
            border_x = (SCREEN_WIDTH - border_width) // 2
            border_y = (SCREEN_HEIGHT - border_height) // 2

            # Blit the border and then the "GAME OVER" text on the screen
            screen.blit(border_surface, (border_x, border_y))
            screen.blit(game_over_text, (text_x, text_y))

        for bullet in invaders.bullets:
            bullet.handle_movement()
            bullet.draw(screen)
            if bullet.rect.colliderect(player.rect):
                # Handle player getting hit by invader bullet
                if not player.is_respawning:
                    player.lives -= 1
                    if player.lives > 0:
                        # Player loses a life but has more lives left
                        player.is_respawning = True
                        player.respawn_timer = time.time()
                        player.rect.centerx = SCREEN_WIDTH // 2
                        player.rect.centery = SCREEN_HEIGHT - 100
                        player_life_images.pop()
                    elif player.lives == 0:
                        # Player is out of lives, handle game over
                        running = False

        # Handle shooting cooldown
        if shooting_cooldown:
            current_time = time.time()
            if current_time - cooldown_start_time >= cooldown_duration:
                shooting_cooldown = False

        # Update the display
        pygame.display.update()

    # Quit the game
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
