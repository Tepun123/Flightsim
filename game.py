
import sys

import pygame

from constants import *
from plane import Plane
from world import World
from ui import UI


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Plane Simulation")
        self.clock = pygame.time.Clock()

        self.plane = Plane()
        self.world = World()
        self.ui = UI()

        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.plane.start_moving()

    def update(self):
        keys = pygame.key.get_pressed()

        # Handle plane input
        self.plane.handle_input(keys)

        # Update physics
        self.plane.update_physics(self.world.runway_y)

        # Update world
        self.world.update(self.plane.get_speed())

        # Check landing conditions
        plane_world_x = self.world.get_plane_world_x()
        self.plane.check_landing(plane_world_x, self.world.runway_y)

    def draw(self):
        # Draw world
        self.world.draw(self.screen)

        # Draw plane
        self.plane.draw(self.screen)

        # Draw UI
        self.ui.draw_hud(self.screen, self.plane)

        if not self.plane.moving:
            self.ui.draw_start_prompt(self.screen)

        if self.plane.crashed:
            self.ui.draw_crash_message(self.screen)
        elif self.plane.landed:
            self.ui.draw_landed_message(self.screen)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            # Handle end states
            if self.plane.crashed:
                pygame.display.flip()
                pygame.time.wait(2000)
                self.running = False
            elif self.plane.landed:
                pygame.display.flip()
                pygame.time.wait(2000)
                self.running = False

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()