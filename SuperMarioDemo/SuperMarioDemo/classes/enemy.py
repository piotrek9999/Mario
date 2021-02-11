""" Class Enemy. """

import pygame as pg
from pygame import sprite


class Enemy(sprite.Sprite):
    """
    This is a class for Enemy object.

    Attributes:
        image : The image of Enemy.
        rect : The coordinates of Enemy.
        last_direction : Last direction of Enemy horizontally.
        counter : The adjunct int to update Enemy's coordinate.
        range : The range to walk Enemy.
        half : The middle of Enemy's range.
    """

    def __init__(self, image_to_load, coo_x, rang, coo_y=432):
        """
        The constructor for Enemy class.

        Parameters:
            image_to_load : The image for Enemy.
            coo_x, coo_y : The values of coordinates for Enemy's object.
            rang : The value of Enemy's range.
        """

        super().__init__()
        self.image = pg.image.load(image_to_load)
        self.image = pg.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = coo_x
        self.rect.y = coo_y
        self.last_direction = 1
        self.counter = 0
        self.range = rang

        if self.range % 2 == 0:
            self.half = self.range / 2 - 1
        else:
            self.half = self.range / 2

    def update(self):
        """Function for updating position of Enemy."""

        if self.counter < (self.half + 1):
            self.rect.x += 10
        if self.half < self.counter < self.range:
            self.rect.x -= 10

        if self.counter == self.range - 1:
            self.counter = -1

        self.counter += 1


ENEMY_GROUP = sprite.Group()
