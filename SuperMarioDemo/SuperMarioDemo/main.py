"""Super Mario by Piotr Grabowski and Bartlomiej Stepek"""

# pylint: disable=no-member
# pylint: disable=import-error
# pylint: disable=no-name-in-module

import sys
import pygame as pg
import classes.background
from classes.money import Money, MONEY_GROUP
from classes.enemy import Enemy, ENEMY_GROUP
from classes.gap import Gap, GAP_GROUP
from classes.hurdle import Hurdle, HURDLES_GROUP
from classes.tunnel import Tunnel, OBJECT_GROUP
from classes.wall import Wall
from classes.mario import Mario
from classes.background import CLEAR_BACKGROUND, BACKGROUND

pg.init()
pg.font.init()

size = (1200, 600)
screen = pg.display.set_mode(size)

LIST_OF_JUMPS = []


def load_image(image_name):
    """Returns loaded image."""

    return pg.image.load(image_name)


def update_jump(parameter):
    """
    Function for updating Mario's jump.

    Parameters:
        parameter : The value to define gravity of jump.
    """

    if parameter % 2 == 0:
        return (parameter * abs(parameter)) * 0.5  # gravitation
    if parameter > 0:
        return ((parameter * abs(parameter)) * 0.5) + 0.5
    return ((parameter * abs(parameter)) * 0.5) - 0.5


def run_mario(mario):
    """
    Function for define direction and navigating of Mario.

    Parameters:
        mario : The object of Mario.
    """

    global LIST_OF_JUMPS
    speed = 28
    keys = pg.key.get_pressed()

    if keys[pg.K_LEFT]:
        mario.update(-speed, 0)

    if keys[pg.K_RIGHT]:
        mario.update(speed, 0)

    if not mario.is_jump:
        if keys[pg.K_SPACE]:
            mario.is_jump = True
            play_sound('music/jump.ogg')

    else:
        if mario.jump_count >= -mario.jump:
            if not (mario.collision_during_jump() and mario.jump_count < 0) or mario.falling:
                mario.update(0, update_jump(mario.jump_count))
                mario.jump_count -= 1
            elif mario.collision_during_jump() and mario.jump_count < 0 and keys[pg.K_SPACE] \
                    and not mario.falling:
                play_sound('music/jump.ogg')
                LIST_OF_JUMPS.append(mario.jump_count)
                mario.jump_count = mario.jump

        else:
            if not LIST_OF_JUMPS:
                mario.jump_count = mario.jump
                mario.is_jump = False
            else:
                mario.jump_count = LIST_OF_JUMPS.pop()


def render():
    """Function to show SCORE during game."""

    font = pg.font.SysFont('Arial', 40)
    return font.render(f'score = {classes.mario.SCORE}', False, (255, 255, 255))


def check_mario_collision_with_gap(mario):
    """
    Function for check if Mario has collision with gap's object.

    Parameters:
        mario : The object of Mario.
    """

    if mario.collision_with_gap():
        for item in GAP_GROUP:
            if item.rect.right - 70 > mario.rect.x > item.rect.left:
                i = 0
                while i < 10:
                    mario.rect.y += 12
                    display(mario)
                    i += 1
                game_over_view()


def check_mario_collision_with_enemy(mario):
    """
    Function for check if Mario has collision with enemy's object.

    Parameters:
        mario : The object of Mario.
    """

    for item in ENEMY_GROUP:
        if abs(400 - (item.rect.x - mario.rect.x)) < 60 and \
                abs(mario.rect.y - item.rect.y) < 40:
            game_over_view()


def check_position_camera(mario):
    """
    Function for limit Mario's movement.

    Parameters:
        mario : The object of Mario.
    """

    if mario.rect.x < 500:
        return min(0, -mario.rect.x)
    return max(-12150, -mario.rect.x)


def game_over_view():
    """Function for game over."""

    pg.mixer.music.stop()
    play_sound('music/death.wav')

    start_image = load_image('images/game_over.png')
    start_image_rect = start_image.get_rect()
    start_image_rect.size = screen.get_size()

    screen.blit(start_image, start_image_rect)
    pg.display.update()

    pg.time.wait(2900)
    terminate()


def check_position_mario(mario):
    """
    Function for determine correct position of Mario.

    Parameters:
        mario : The object of Mario.
    """

    if mario.rect.x <= -396:
        return 10

    if -396 < mario.rect.x < 0:
        return 400 + mario.rect.x

    if mario.rect.x >= 12848:
        return 1090

    if 12848 > mario.rect.x > 12158:
        return mario.rect.x - 11758

    return 400


def ending_view():
    """"Function for create ending game."""

    pg.mixer.music.stop()
    play_sound('music/end.ogg')

    win_image = load_image('images/win.png')
    win_image_rect = win_image.get_rect()
    win_image_rect.size = screen.get_size()

    screen.blit(win_image, win_image_rect)
    pg.display.update()

    pg.time.wait(2900)
    terminate()


def display(mario):
    """
    Function for display everything in game.

    Parameters:
        mario : The object of Mario.
    """

    if classes.mario.TO_CLEAR:
        BACKGROUND.image.blit(CLEAR_BACKGROUND.image,
                              (CLEAR_BACKGROUND.rect.x, CLEAR_BACKGROUND.rect.y))
        classes.mario.TO_CLEAR = False
    pg.display.update()
    clock = pg.time.Clock()

    for item in MONEY_GROUP:
        BACKGROUND.image.blit(item.image, (item.back_x, item.rect.y))

    for item in ENEMY_GROUP:
        item.update()
        screen.blit(item.image, (item.rect.x - mario.rect.x, item.rect.y))

    pg.display.update()
    screen.blit(BACKGROUND.image, (check_position_camera(mario), BACKGROUND.rect.y))
    screen.blit(mario.image, (check_position_mario(mario), mario.rect.y))
    screen.blit(render(), (30, 10))
    check_mario_collision_with_gap(mario)
    check_mario_collision_with_enemy(mario)

    if mario.rect.x == 12456 and mario.rect.y > 400:
        ending_view()

    pg.display.update()
    clock.tick(60)


def terminate():
    """"Function to terminate and end a game."""

    pg.quit()
    sys.exit()


def wait_for_key():
    """"Function for waiting for pressing key."""

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    terminate()
                return


def starting_view():
    """"Function for create start game."""

    start_image = load_image('images/start.png')
    start_image_rect = start_image.get_rect()
    start_image_rect.size = screen.get_size()

    screen.blit(start_image, start_image_rect)
    pg.display.update()

    wait_for_key()


def play_sound(song):
    """"Function for start playing music."""

    effect = pg.mixer.Sound(song)
    effect.play()


def make_tunnels():
    """"Function for make all tunnels on map game."""

    tunnel1 = Tunnel('images/tunnel1.png', 1350, 1769, 420)
    tunnel2 = Tunnel('images/tunnel2.png', 7600, 7987, 385)
    tunnel3 = Tunnel('images/tunnel3.png', 2500, 2907, 329)
    tunnel4 = Tunnel('images/tunnel4.png', 3180, 3602, 329)
    tunnel5 = Tunnel('images/tunnel5.png', 9890, 10300, 420)
    tunnel6 = Tunnel('images/tunnel6.png', 10893, 11315, 420)
    OBJECT_GROUP.add(tunnel1)
    OBJECT_GROUP.add(tunnel2)
    OBJECT_GROUP.add(tunnel3)
    OBJECT_GROUP.add(tunnel4)
    OBJECT_GROUP.add(tunnel5)
    OBJECT_GROUP.add(tunnel6)


def make_walls():
    """"Function for make all walls on map game."""

    wall1 = Wall('images/wall1.png', 8150, 8597, 387)
    wall2 = Wall('images/wall2.png', 8440, 8848, 385)
    wall3 = Wall('images/wall3.png', 9060, 9483, 385)
    wall4 = Wall('images/wall4.png', 9400, 9795, 385)
    wall5 = Wall('images/wall5.png', 11270, 11694, 300)
    OBJECT_GROUP.add(wall1)
    OBJECT_GROUP.add(wall2)
    OBJECT_GROUP.add(wall3)
    OBJECT_GROUP.add(wall4)
    OBJECT_GROUP.add(wall5)


def make_hurdles():
    """"Function for make all hurdles on map game."""

    hurdle1 = Hurdle('images/hurdle1.png', 810, 1250, 227)
    hurdle2 = Hurdle('images/hurdle2.png', 4500, 4900, 325)
    hurdle3 = Hurdle('images/hurdle3.png', 4670, 5100, 125)
    hurdle4 = Hurdle('images/hurdle4.png', 5440, 5840, 325)
    hurdle5 = Hurdle('images/hurdle5.png', 10260, 10600, 235)
    HURDLES_GROUP.add(hurdle1)
    HURDLES_GROUP.add(hurdle2)
    HURDLES_GROUP.add(hurdle3)
    HURDLES_GROUP.add(hurdle4)
    HURDLES_GROUP.add(hurdle5)


def make_gaps():
    """"Function for make all gaps on map game."""

    gap1 = Gap('images/gap1.png', 3959, 4360)
    gap2 = Gap('images/gap2.png', 5039, 5430)
    gap3 = Gap('images/gap3.png', 9269, 9673)
    GAP_GROUP.add(gap1)
    GAP_GROUP.add(gap2)
    GAP_GROUP.add(gap3)


def make_moneys():
    """"Function for make all coins on map game."""

    for i in range(3):
        money = Money('images/money.png', 300 + i * 75, 200, 750 + i * 75)
        MONEY_GROUP.add(money)

    for i in range(3):
        money = Money('images/money.png', 1700 + i * 75, 170, 2150 + i * 75)
        MONEY_GROUP.add(money)

    for i in range(3):
        money = Money('images/money.png', 2800 + i * 75, 130, 3260 + i * 75)
        MONEY_GROUP.add(money)

    for i in range(3):
        money = Money('images/money.png', 7900 + i * 75, 130, 8300 + i * 75)
        MONEY_GROUP.add(money)

    for i in range(3):
        money = Money('images/money.png', 8800 + i * 75, 130, 9200 + i * 75)
        MONEY_GROUP.add(money)

    for i in range(3):
        money = Money('images/money.png', 10260 + i * 75, 170, 10660 + i * 75)
        MONEY_GROUP.add(money)

    for i in range(3):
        money = Money('images/money.png', 6000 + i * 75, 220, 6400 + i * 75)
        MONEY_GROUP.add(money)

    for i in range(6):
        money = Money('images/money.png', 4800 + i * 50, 75, 5200 + i * 50)
        MONEY_GROUP.add(money)

    for i in range(2):
        money = Money('images/money.png', 960 + i * 75, 170, 1360 + i * 75)
        MONEY_GROUP.add(money)

    for i in range(2):
        money = Money('images/money.png', 3980 + i * 50, 280, 4380 + i * 50)
        MONEY_GROUP.add(money)

    for i in range(2):
        money = Money('images/money.png', 6700 + i * 50, 280, 7100 + i * 50)
        MONEY_GROUP.add(money)


def make_enemies():
    """"Function for make all enemies on map game."""

    enemy1 = Enemy('images/enemy.png', 2600, 50)
    enemy2 = Enemy('images/enemy.png', 3020, 100)
    enemy3 = Enemy('images/enemy.png', 5940, 30)
    enemy4 = Enemy('images/enemy.png', 7040, 30)
    enemy5 = Enemy('images/enemy.png', 7840, 10)
    enemy6 = Enemy('images/enemy.png', 8730, 10)
    enemy7 = Enemy('images/enemy.png', 10450, 150)
    enemy8 = Enemy('images/enemy.png', 4000, 20)
    enemy9 = Enemy('images/enemy.png', 4710, 20)
    enemy10 = Enemy('images/enemy.png', 8130, 80)
    ENEMY_GROUP.add(enemy1)
    ENEMY_GROUP.add(enemy2)
    ENEMY_GROUP.add(enemy3)
    ENEMY_GROUP.add(enemy4)
    ENEMY_GROUP.add(enemy5)
    ENEMY_GROUP.add(enemy6)
    ENEMY_GROUP.add(enemy7)
    ENEMY_GROUP.add(enemy8)
    ENEMY_GROUP.add(enemy9)
    ENEMY_GROUP.add(enemy10)
    enemy11 = Enemy('images/enemy.png', 6600, 30)
    ENEMY_GROUP.add(enemy11)
    enemy12 = Enemy('images/enemy.png', 7500, 40)
    ENEMY_GROUP.add(enemy12)
    enemy13 = Enemy('images/enemy.png', 2000, 20)
    ENEMY_GROUP.add(enemy13)
    enemy14 = Enemy('images/enemy.png', 9000, 80)
    ENEMY_GROUP.add(enemy14)
    enemy15 = Enemy('images/enemy.png', 10000, 30)
    ENEMY_GROUP.add(enemy15)
    enemy16 = Enemy('images/enemy.png', 11500, 10)
    ENEMY_GROUP.add(enemy16)
    enemy18 = Enemy('images/enemy.png', 12070, 40)
    ENEMY_GROUP.add(enemy18)


def make_background():
    """"Function for make background with static objects."""

    for item in OBJECT_GROUP:
        CLEAR_BACKGROUND.image.blit(item.image, (item.back_x, item.back_y))

    for item in GAP_GROUP:
        CLEAR_BACKGROUND.image.blit(item.image, (item.back_x, item.rect.y))

    for item in HURDLES_GROUP:
        CLEAR_BACKGROUND.image.blit(item.image,
                                    (item.back_x, item.back_y))

    BACKGROUND.image.blit(CLEAR_BACKGROUND.image,
                          (CLEAR_BACKGROUND.rect.x, CLEAR_BACKGROUND.rect.y))


def play_game():
    """"Main function for make game."""

    mario = Mario('images/mario1.png', 'images/mario2.png')
    make_tunnels()
    make_walls()
    make_hurdles()
    make_gaps()
    make_moneys()
    make_enemies()
    make_background()

    pg.mixer.music.load('music/mario_song.wav')
    starting_view()
    pg.mixer.music.play(-1, 0.0)

    run = True
    while run:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        run_mario(mario)
        display(mario)

    pg.quit()


play_game()
