import pygame
import random
from constants import *


class World:
    def __init__(self):
        self.camera_x = 0
        self.runway_y = HEIGHT - 50
        self.clouds = self._generate_clouds()

    def _generate_clouds(self):
        clouds = []
        for _ in range(NUM_CLOUDS):
            x = random.randint(0, WIDTH * 3)
            y = random.randint(50, 200)
            size = random.randint(40, 80)
            clouds.append({"x": x, "y": y, "size": size})
        return clouds

    def update(self, plane_speed):
        self.camera_x += plane_speed

    def draw(self, screen):
        # Clear screen
        screen.fill(SKY)

        # Draw clouds
        for cloud in self.clouds:
            cloud_x = (cloud["x"] - self.camera_x * 0.5) % (WIDTH * 3)
            size = cloud["size"]
            y = cloud["y"]
            pygame.draw.ellipse(screen, WHITE, (cloud_x, y, size, size // 2))
            pygame.draw.ellipse(screen, WHITE, (cloud_x + size * 0.3, y - size * 0.15, size, size // 2))
            pygame.draw.ellipse(screen, WHITE, (cloud_x + size * 0.6, y, size, size // 2))

        # Draw scrolling ground
        pygame.draw.rect(screen, GRASS, (-self.camera_x % WIDTH - WIDTH, HEIGHT - 50, WIDTH * 3, 50))

        # Draw looping runway
        runway_screen_x = (RUNWAY_GAP - (self.camera_x % RUNWAY_GAP))
        pygame.draw.rect(screen, RUNWAY_COLOR, (runway_screen_x, self.runway_y, RUNWAY_LENGTH, 10))

    def get_plane_world_x(self):
        return self.camera_x + 200