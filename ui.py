import pygame
from constants import *


class UI:
    def __init__(self):
        self.font = pygame.font.SysFont("arial", 28)
        self.small_font = pygame.font.SysFont("arial", 18)

    def draw_hud(self, screen, plane):
        # KPH display
        kph_text = self.small_font.render(f"KPH: {int(plane.kph)}", True, BLACK)
        screen.blit(kph_text, (10, 10))

        # Wind speed display
        wind_text = self.small_font.render(f"Wind Speed: {WIND_SPEED} km/h", True, BLACK)
        screen.blit(wind_text, (10, 30))

    def draw_start_prompt(self, screen):
        prompt1 = self.small_font.render("The pilot died and now you have to take control", True, BLACK)
        screen.blit(prompt1, (WIDTH // 2.5 - 100, HEIGHT - 80))
        prompt2 = self.small_font.render("Press D to start flying", True, BLACK)
        screen.blit(prompt2, (WIDTH // 2 - 100, HEIGHT - 50))
        prompt3 = self.small_font.render("Press S to go up and W to go down", True, BLACK)
        screen.blit(prompt3, (WIDTH // 2 - 100, HEIGHT - 20))


    def draw_crash_message(self, screen):
        text = self.font.render("CRASH!", True, RED)
        screen.blit(text, (WIDTH // 2 - 60, HEIGHT // 2))

    def draw_landed_message(self, screen):
        text = self.font.render("LANDED SAFELY!", True, BLACK)
        screen.blit(text, (WIDTH // 2 - 120, HEIGHT // 2))