import pygame
import os
import random

pygame.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load Assets
RUNNING = [
    pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
    pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png")),
]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [
    pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
    pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png")),
]

SMALL_CACTUS = [
    pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
    pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
    pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png")),
]

LARGE_CACTUS = [
    pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
    pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
    pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png")),
]

BIRD = [
    pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
    pygame.image.load(os.path.join("Assets/Bird", "Bird2.png")),
]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))
BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))


# ================== CLASSES ==================

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL

        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, user_input):
        if self.dino_duck:
            self.duck()
        elif self.dino_run:
            self.run()
        elif self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if user_input.get(pygame.K_UP, False) and not self.dino_jump:
            self.dino_jump = True
            self.dino_run = False
            self.dino_duck = False
        elif user_input.get(pygame.K_DOWN, False) and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not self.dino_jump:
            self.dino_run = True
            self.dino_duck = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        self.dino_rect.y -= self.jump_vel * 4
        self.jump_vel -= 0.8

        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD

    def update(self):
        self.x -= game_speed
        if self.x < -self.image.get_width():
            self.x = SCREEN_WIDTH + random.randint(2000, 3000)
            self.y = random.randint(50, 100)

    def draw(self):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, index):
        self.image = image
        self.index = index
        self.rect = self.image[self.index].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.remove(self)

    def draw(self):
        SCREEN.blit(self.image[self.index], self.rect)


class SmallCactus(Obstacle):
    def __init__(self):
        super().__init__(SMALL_CACTUS, random.randint(0, 2))
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self):
        super().__init__(LARGE_CACTUS, random.randint(0, 2))
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self):
        super().__init__(BIRD, 0)
        self.rect.y = 250
        self.step_index = 0

    def draw(self):
        if self.step_index >= 10:
            self.step_index = 0
        SCREEN.blit(self.image[self.step_index // 5], self.rect)
        self.step_index += 1


# ================== GAME FUNCTIONS ==================

def main():
    global game_speed, x_pos_bg, points, obstacles

    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()

    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    obstacles = []

    font = pygame.font.Font(None, 20)
    run = True

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render(f"Points: {points}", True, (0, 0, 0))
        SCREEN.blit(text, (850, 40))

    def background():
        global x_pos_bg
        image_width = BG.get_width()

        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))

        if x_pos_bg <= -image_width:
            x_pos_bg = 0

        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        user_input = pygame.key.get_pressed()

        player.update(user_input)
        player.draw()

        if not obstacles:
            rand = random.randint(0, 2)
            if rand == 0:
                obstacles.append(SmallCactus())
            elif rand == 1:
                obstacles.append(LargeCactus())
            else:
                obstacles.append(Bird())

        for obstacle in obstacles[:]:
            obstacle.update()
            obstacle.draw()

            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(1000)
                menu()
                return

        background()
        cloud.update()
        cloud.draw()
        score()

        clock.tick(30)
        pygame.display.update()


def menu():
    run = True
    font = pygame.font.Font(None, 30)

    while run:
        SCREEN.fill((255, 255, 255))
        text = font.render("Press any key to start", True, (0, 0, 0))
        SCREEN.blit(text, (400, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                main()

        pygame.display.update()


if __name__ == "__main__":
    menu()
