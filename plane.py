import pygame

from constants import *


class Plane:
    def __init__(self):
        self.y = 200
        self.tilt = 0
        self.vertical_speed = 0
        self.kph = 60
        self.moving = False
        self.landed = False
        self.crashed = False

        # Create plane image
        self.image = pygame.Surface((60, 20), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, WHITE, [(0, 0), (60, 10), (0, 20)])

    def handle_input(self, keys):
        # Manual KPH control
        if keys[pygame.K_d] and self.kph < MAX_KPH:
            self.kph += 1
        if keys[pygame.K_a] and self.kph > MIN_KPH:
            self.kph -= 1

        # Tilt control
        if keys[pygame.K_w]:
            self.tilt += TILT_SPEED  # nose down
        elif keys[pygame.K_s]:
            self.tilt -= TILT_SPEED  # nose up
        else:
            # Auto-level
            if self.tilt > 0:
                self.tilt -= TILT_SPEED / 2
            elif self.tilt < 0:
                self.tilt += TILT_SPEED / 2

        # Clamp tilt
        self.tilt = max(min(self.tilt, MAX_TILT), -MAX_TILT)

    def update_physics(self, runway_y):
        if self.moving:
            # Take into account wind
            if self.kph < MAX_KPH:
                self.kph += WIND_SPEED / PLANE_WEIGHT
            self.kph = min(max(self.kph, MIN_KPH), MAX_KPH)

            # Apply physics
            lift = -self.tilt * 0.003  # lift effect based on tilt
            self.vertical_speed += GRAVITY - lift
            self.vertical_speed *= 0.98
            self.y += self.vertical_speed

            # Keep plane above ground
            if self.y > runway_y - 20:
                self.y = runway_y - 20
                self.vertical_speed = 0

    def check_landing(self, plane_world_x, runway_y):
        if self.landed or self.crashed:
            return

        current_runway_start = (plane_world_x // RUNWAY_GAP) * RUNWAY_GAP
        current_runway_end = current_runway_start + RUNWAY_LENGTH

        # If plane is above runway horizontally
        if current_runway_start <= plane_world_x <= current_runway_end:
            # Close to ground → try to land
            if self.y >= runway_y - 25:
                if abs(self.vertical_speed) <= 3 and abs(self.tilt) <= MAX_SAFE_TILT and self.kph <= SAFE_LANDING_KPH:
                    self.landed = True
                    self.vertical_speed = 0
                    self.y = runway_y - 20
                else:
                    self.crashed = True
        # If touching ground outside runway → crash
        elif self.y >= runway_y - 20:
            self.crashed = True

    def get_speed(self):
        return self.kph / 60 if self.moving else 0

    def start_moving(self):
        self.moving = True

    def draw(self, screen):
        rotated_plane = pygame.transform.rotate(self.image, -self.tilt)
        rect = rotated_plane.get_rect(center=(200, self.y))
        screen.blit(rotated_plane, rect)