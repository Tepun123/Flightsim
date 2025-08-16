# import pygame
# import sys
# import random
#
# # Initialize Pygame
# pygame.init()
#
# # Screen setup
# WIDTH, HEIGHT = 800, 600
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Endless Flight Landing with Clouds")
#
# # Colors
# SKY = (135, 206, 235)
# GRASS = (34, 139, 34)
# WHITE = (255, 255, 255)
# RED = (255, 0, 0)
# BLACK = (0, 0, 0)
#
# # Font
# font = pygame.font.SysFont("arial", 28)
# small_font = pygame.font.SysFont("arial", 18)
#
# # Plane setup
# plane_img = pygame.Surface((60, 20), pygame.SRCALPHA)
# pygame.draw.polygon(plane_img, WHITE, [(0, 0), (60, 10), (0, 20)])
#
# # Cloud setup
# NUM_CLOUDS = 8
# clouds = []
# for _ in range(NUM_CLOUDS):
#     x = random.randint(0, WIDTH * 3)
#     y = random.randint(50, 200)
#     size = random.randint(40, 80)
#     clouds.append({"x": x, "y": y, "size": size})
#
# # Initial state
#
# plane_y = 200
# tilt = 0
# gravity = 0.0098
# vertical_speed = 0
# max_safe_tilt = 15
# moving = False
# camera_x = 0
# wind_speed = random.randint(-10, 10)
# plane_weight = 100
# # KPH settings
# kph = 40              # Start at 0 KPH
# min_kph = 0
# max_kph = 240
#
# # Landing thresholds
# safe_landing_kph = 150
# safe_vertical_speed = 1.5
#
# # State flags
# clock = pygame.time.Clock()
# running = True
# landed = False
# crashed = False
#
# while running:
#     screen.fill(SKY)
#
#     # Draw clouds (parallax scroll)
#     for cloud in clouds:
#         cloud_x = cloud["x"] - camera_x * 0.5
#         cloud_x %= WIDTH * 3
#         size = cloud["size"]
#         y = cloud["y"]
#         pygame.draw.ellipse(screen, WHITE, (cloud_x, y, size, size // 2))
#         pygame.draw.ellipse(screen, WHITE, (cloud_x + size * 0.3, y - size * 0.15, size, size // 2))
#         pygame.draw.ellipse(screen, WHITE, (cloud_x + size * 0.6, y, size, size // 2))
#
#     # Draw scrolling ground
#     pygame.draw.rect(screen, GRASS, (-camera_x % WIDTH - WIDTH, HEIGHT - 50, WIDTH * 3, 50))
#
#     # Handle events
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_d:
#                 moving = True
#
#     # Get key input
#     keys = pygame.key.get_pressed()
#
#     # Manual KPH control
#     if keys[pygame.K_d] and kph < max_kph:
#         kph += 1
#     if keys[pygame.K_a] and kph > min_kph:
#         kph -= 1
#
#     # Take in account wind
#     if moving and kph < max_kph:
#         kph += wind_speed/plane_weight
#
#     # Tilt control
#     if keys[pygame.K_w]:
#         tilt += 0.5
#     if keys[pygame.K_s]:
#         tilt -= 0.5
#     tilt = max(min(tilt, 45), -45)
#
#     # Apply physics only after movement starts
#     if moving:
#         lift = tilt * 0.005
#         vertical_speed += gravity + lift
#         vertical_speed *= 0.98
#         plane_y += vertical_speed
#
#         # Scroll world
#         speed = kph / 60
#         camera_x += speed
#
#     # Ground collision and landing check
#     if plane_y > HEIGHT - 70:
#         plane_y = HEIGHT - 70
#
#         if not landed:
#             landed = True
#             safe_tilt = abs(tilt) <= max_safe_tilt
#             safe_descent = abs(vertical_speed) <= safe_vertical_speed
#             safe_speed = kph <= safe_landing_kph
#
#             if safe_tilt and safe_descent and safe_speed:
#                 text = font.render("Landed Safely! ", True, BLACK)
#             else:
#                 crashed = True
#                 text = font.render("CRASH! ", True, RED)
#
#             screen.blit(text, (WIDTH // 2 - 120, HEIGHT // 2))
#             pygame.display.flip()
#             pygame.time.wait(2000)
#             running = False
#
#         vertical_speed = 0
#
#     wind_text = small_font.render(f"Wind Speed: {wind_speed} km/h", True, BLACK)
#     screen.blit(wind_text, (10, 30))
#
#     # Draw plane
#     rotated_plane = pygame.transform.rotate(plane_img, -tilt)
#     rect = rotated_plane.get_rect(center=(200, plane_y))
#     screen.blit(rotated_plane, rect)
#
#     # KPH display
#     kph_text = small_font.render(f"KPH: {int(kph)}", True, BLACK)
#     screen.blit(kph_text, (10, 10))
#
#     # Prompt to start
#     if not moving:
#         prompt = small_font.render("The pilot died and now you have to take control", True, BLACK)
#         screen.blit(prompt, (WIDTH // 2.5 - 100, HEIGHT - 70))
#         prompt = small_font.render("Press D to start flying", True, BLACK)
#         screen.blit(prompt, (WIDTH // 2 - 100, HEIGHT - 40))
#
#     pygame.display.flip()
#     clock.tick(kph if kph > 0 else 60)  # prevent 0 FPS
#
# pygame.quit()
# sys.exit()
import pygame
import random
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plane Simulation")

# Colors
SKY = (135, 206, 235)
GRASS = (34, 139, 34)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
RUNWAY_COLOR = (60, 60, 60)

# Font
font = pygame.font.SysFont("arial", 28)
small_font = pygame.font.SysFont("arial", 18)

# Plane setup
plane_img = pygame.Surface((60, 20), pygame.SRCALPHA)
pygame.draw.polygon(plane_img, WHITE, [(0, 0), (60, 10), (0, 20)])

# Cloud setup
NUM_CLOUDS = 8
clouds = []
for _ in range(NUM_CLOUDS):
    x = random.randint(0, WIDTH * 3)
    y = random.randint(50, 200)
    size = random.randint(40, 80)
    clouds.append({"x": x, "y": y, "size": size})

# Initial state
plane_y = 200
tilt = 0
tilt_speed = 0.3
gravity = 0.05
vertical_speed = 0
max_safe_tilt = 15
max_tilt = 25
moving = False
camera_x = 0
wind_speed = random.randint(-10, 10)
plane_weight = 100

kph = 40
min_kph = 0
max_kph = 240

# Landing thresholds
safe_landing_kph = 150
safe_vertical_speed = 1.5

# Runway settings (looping)
runway_y = HEIGHT - 50
runway_length = 400
runway_gap = 2000  # distance between runways

# Landing state flags
clock = pygame.time.Clock()
running = True
landed = False
crashed = False
landing_phase = False
runway_progress = 0

while running:
    screen.fill(SKY)

    # Draw clouds
    for cloud in clouds:
        cloud_x = (cloud["x"] - camera_x * 0.5) % (WIDTH * 3)
        size = cloud["size"]
        y = cloud["y"]
        pygame.draw.ellipse(screen, WHITE, (cloud_x, y, size, size // 2))
        pygame.draw.ellipse(screen, WHITE, (cloud_x + size * 0.3, y - size * 0.15, size, size // 2))
        pygame.draw.ellipse(screen, WHITE, (cloud_x + size * 0.6, y, size, size // 2))

    # Draw scrolling ground
    pygame.draw.rect(screen, GRASS, (-camera_x % WIDTH - WIDTH, HEIGHT - 50, WIDTH * 3, 50))

    # Draw looping runway
    runway_screen_x = (runway_gap - (camera_x % runway_gap))
    pygame.draw.rect(screen, RUNWAY_COLOR,
                     (runway_screen_x, runway_y, runway_length, 10))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                moving = True

    # Get key input
    keys = pygame.key.get_pressed()

    # Manual KPH control
    if keys[pygame.K_d] and kph < max_kph:
        kph += 1
    if keys[pygame.K_a] and kph > min_kph:
        kph -= 1

    # Take into account wind
    if moving and kph < max_kph:
        kph += wind_speed / plane_weight
    kph = min(max(kph, min_kph), max_kph)

    # Tilt control (unchanged)
    if keys[pygame.K_w]:
        tilt += tilt_speed  # nose down
    elif keys[pygame.K_s]:
        tilt -= tilt_speed  # nose up
    else:
        # Auto-level
        if tilt > 0:
            tilt -= tilt_speed / 2
        elif tilt < 0:
            tilt += tilt_speed / 2

    # Clamp tilt
    tilt = max(min(tilt, max_tilt), -max_tilt)

    # Apply physics after movement starts
    if moving:
        lift = -tilt * 0.003  # lift effect based on tilt
        vertical_speed += gravity - lift
        vertical_speed *= 0.98
        plane_y += vertical_speed

        # Scroll world
        speed = kph / 60
        camera_x += speed

    # --- UPDATED LANDING LOGIC START ---

    # --- FIXED LANDING LOGIC ---
    plane_world_x = camera_x + 200
    current_runway_start = (plane_world_x // runway_gap) * runway_gap
    current_runway_end = current_runway_start + runway_length

    if not landed and not crashed:
        # If plane is above runway horizontally
        if current_runway_start <= plane_world_x <= current_runway_end:
            # Close to ground → try to land
            if plane_y >= runway_y - 25:
                if abs(vertical_speed) <= 3 and abs(tilt) <= max_safe_tilt and kph <= safe_landing_kph:
                    landed = True
                    vertical_speed = 0
                    plane_y = runway_y - 20
                else:
                    crashed = True
        # If touching ground outside runway → crash
        elif plane_y >= runway_y - 20:
            crashed = True

    # --- UPDATED LANDING LOGIC END ---

    # If crashed
    if crashed:
        text = font.render("CRASH!", True, RED)
        screen.blit(text, (WIDTH // 2 - 60, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    # If landed
    if landed:
        text = font.render("LANDED SAFELY!", True, BLACK)
        screen.blit(text, (WIDTH // 2 - 120, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    # Keep plane above ground
    if plane_y > runway_y - 20:
        plane_y = runway_y - 20
        vertical_speed = 0

    # Wind speed display
    wind_text = small_font.render(f"Wind Speed: {wind_speed} km/h", True, BLACK)
    screen.blit(wind_text, (10, 30))

    # Draw plane
    rotated_plane = pygame.transform.rotate(plane_img, -tilt)
    rect = rotated_plane.get_rect(center=(200, plane_y))
    screen.blit(rotated_plane, rect)

    # KPH display
    kph_text = small_font.render(f"KPH: {int(kph)}", True, BLACK)
    screen.blit(kph_text, (10, 10))

    # Prompt to start
    if not moving:
        prompt = small_font.render("The pilot died and now you have to take control", True, BLACK)
        screen.blit(prompt, (WIDTH // 2.5 - 100, HEIGHT - 70))
        prompt = small_font.render("Press D to start flying", True, BLACK)
        screen.blit(prompt, (WIDTH // 2 - 100, HEIGHT - 40))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
