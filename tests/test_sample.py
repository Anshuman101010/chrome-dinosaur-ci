import sys
import os

# Fix path BEFORE importing main
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import main  # noqa: E402


def test_dinosaur_init():
    dino = main.Dinosaur()
    assert dino.dino_rect.x == 80
    assert dino.dino_rect.y == 310


def test_dinosaur_run():
    dino = main.Dinosaur()
    dino.run()
    assert dino.dino_rect.y == 310


def test_dinosaur_duck():
    dino = main.Dinosaur()
    dino.dino_duck = True
    dino.duck()
    assert dino.dino_rect.y == 340


def test_dinosaur_jump():
    dino = main.Dinosaur()
    dino.dino_jump = True
    old_y = dino.dino_rect.y
    dino.jump()
    assert dino.dino_rect.y < old_y


def test_cloud():
    cloud = main.Cloud()
    assert cloud.x > 0
    assert 50 <= cloud.y <= 100


def test_small_cactus():
    c = main.SmallCactus()
    assert c.rect.y == 325


def test_large_cactus():
    c = main.LargeCactus()
    assert c.rect.y == 300


def test_bird():
    b = main.Bird()
    assert b.rect.y == 250

def test_dinosaur_update_run():
    dino = main.Dinosaur()
    keys = {key: False for key in range(512)}  # fake keys
    dino.update(keys)
    assert dino.dino_run is True


def test_dinosaur_update_jump():
    dino = main.Dinosaur()
    keys = {key: False for key in range(512)}
    keys[main.pygame.K_UP] = True

    dino.update(keys)
    assert dino.dino_jump is True


def test_cloud_update():
    cloud = main.Cloud()
    global game_speed
    main.game_speed = 5

    old_x = cloud.x
    cloud.update()
    assert cloud.x < old_x


def test_obstacle_update_removal():
    main.game_speed = 100  # fast move
    obstacle = main.SmallCactus()
    main.obstacles = [obstacle]

    obstacle.rect.x = -100  # force off screen
    obstacle.update()

    assert obstacle not in main.obstacles


def test_background_movement():
    main.game_speed = 5
    main.x_pos_bg = 0

    # simulate background function
    main.x_pos_bg -= main.game_speed

    assert main.x_pos_bg == -5

