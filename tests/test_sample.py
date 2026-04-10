import main


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