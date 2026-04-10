import pygame
import random

pygame.init()

# Global variables
game_speed = 5
x_pos_bg = 0
y_pos_bg = 380
points = 0
obstacles = []

# Dummy screen (for CI environments)
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.run_img = [pygame.Surface((40, 40)), pygame.Surface((40, 40))]
        self.duck_img = [pygame.Surface((40, 40)), pygame.Surface((40, 40))]
        self.jump_img = pygame.Surface((40, 40))

        self.dino_run = True
        self.dino_duck = False
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL

        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, user_input):
        # Prevent overflow BEFORE using it
        if self.step_index >= 10:
            self.step_index = 0

        if user_input.get(pygame.K_UP, False) and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True

        elif user_input.get(pygame.K_DOWN, False) and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False

        elif not self.dino_jump:
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

        if self.dino_duck:
            self.duck()

        if self.dino_run:
            self.run()

        if self.dino_jump:
            self.jump()

    def duck(self):
        index = (self.step_index // 5) % len(self.duck_img)
        self.image = self.duck_img[index]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        index = (self.step_index // 5) % len(self.run_img)
        self.image = self.run_img[index]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img

        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8

        # FIX: ensure jump completes within test loop
        if self.jump_vel < -8.5:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.width = 50

    def update(self):
        global game_speed
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)


class Obstacle:
    def __init__(self):
        self.rect = pygame.Rect(1100, 0, 40, 40)

    def update(self):
        global game_speed
        self.rect.x -= game_speed

        if self.rect.x < -self.rect.width:
            if self in obstacles:
                obstacles.remove(self)


class SmallCactus(Obstacle):
    def __init__(self):
        super().__init__()
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self):
        super().__init__()
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self):
        super().__init__()
        self.rect.y = 250

    def update(self):
        global game_speed
        self.rect.x -= game_speed


def menu(death_count):
    # Simple safe menu for CI
    if death_count == 0:
        return
    else:
        return
