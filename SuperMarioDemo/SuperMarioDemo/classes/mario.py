""" Class Mario. """

# pylint: disable=import-error
# pylint: disable=no-name-in-module

import pygame as pg
from pygame import sprite
from classes.money import MONEY_GROUP
from classes.gap import GAP_GROUP
from classes.hurdle import HURDLES_GROUP
from classes.tunnel import OBJECT_GROUP

SCORE = 0
TO_CLEAR = False


def play_sound(song):
    """"Function for start playing music."""

    effect = pg.mixer.Sound(song)
    effect.play()


class Mario(sprite.Sprite):
    """
    This is a class for Mario's object.

    Attributes:
        image : The actual animation image of Mario.
        image1 : First animation image of Mario.
        image2 : Second animation image of Mario.
        rect : The coordinates of Mario.
        jump : The general value of Mario's jump.
        is_jump : The boolean value to check if Mario is in jump or not.
        jump_count : Current value of Mario's jump.
        last_direction_x : Last direction of Mario horizontally.
        last_direction_y : Last direction of Mario vertical.
        falling : The boolean value to check if Mario falling or not.
        on_top : The boolean value to check if Mario is on object or not.
    """

    def __init__(self, image_to_load1, image_to_load2):
        """
        The constructor for Mario class.

        Parameters:
            image_to_load1, image_to_load2 : The images for Mario's animation.
        """

        super().__init__()
        self.image = pg.image.load(image_to_load1)
        self.image = pg.transform.scale(self.image, (80, 80))
        self.image1 = pg.image.load(image_to_load1)
        self.image1 = pg.transform.scale(self.image1, (80, 80))
        self.image2 = pg.image.load(image_to_load2)
        self.image2 = pg.transform.scale(self.image2, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.center = (400, 472)
        self.jump = 10
        self.is_jump = False
        self.jump_count = self.jump
        self.last_direction_x = 1
        self.last_direction_y = 1
        self.falling = False
        self.on_top = False

    def collision_with_object(self):
        """Returns if Mario has collision with objects on map."""

        if sprite.spritecollide(self, OBJECT_GROUP, dokill=False):
            return True
        return False

    def collision_with_gap(self):
        """Returns if Mario has collision with gaps on map."""

        if sprite.spritecollide(self, GAP_GROUP, dokill=False):
            return True
        return False

    def collision_with_money(self):
        """Returns if Mario has collision with money on map."""

        if sprite.spritecollide(self, MONEY_GROUP, dokill=True):
            play_sound('music/coin.ogg')
            return True
        return False

    def collision_with_hurdle(self):
        """Returns if Mario has collision with hurdles on map."""

        if sprite.spritecollide(self, HURDLES_GROUP, dokill=False):
            return True
        return False

    def collision_during_jump(self):
        """Returns if Mario has collision during jump."""

        return self.collision_with_object() or self.collision_with_hurdle()

    def update(self, run_x, run_y):
        """
        Function for updating Mario object.

        Parameters:
            run_x : Value to change Mario's coordinate.
            run_y : Value to change Mario's coordinate.
        """
        if run_x > 0 or (run_x == 0 and self.last_direction_x == 1):
            self.image = self.image1
        else:
            self.image = self.image2

        if (not self.collision_during_jump() or self.on_top) or \
                (self.collision_during_jump() and self.jump_count < 3) and \
                12848 > self.rect.x > -396:
            self.rect.x += run_x

        if (self.rect.x == -396 and run_x > 0) or (self.rect.x == 12848 and run_x < 0):
            self.rect.x += run_x

        if self.collision_with_object():
            if (self.last_direction_x == 1 and run_x < 0) \
                    or self.last_direction_x == -1 and run_x > 0:
                self.rect.x += run_x

        if run_x != 0:
            self.last_direction_x = 1 if run_x > 0 else -1

        if run_y != 0:
            self.last_direction_y = 1 if run_y > 0 else -1
            if 9 > self.jump_count > 0:
                if self.collision_with_hurdle():
                    self.jump_count = -self.jump_count
                    self.falling = True
                    return

            if self.falling:
                self.rect.y -= run_y
                self.falling = False

            elif not (self.jump_count < 0 and self.collision_during_jump()):
                self.rect.y -= run_y

            if self.collision_during_jump():
                self.on_top = True

        if self.jump_count == self.jump:
            self.on_top = False

        if self.collision_with_money():
            global SCORE
            global TO_CLEAR
            SCORE += 1
            TO_CLEAR = True
