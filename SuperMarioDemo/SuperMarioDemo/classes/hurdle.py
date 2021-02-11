""" Class Hurdle. """

import pygame as pg
from pygame import sprite


class Hurdle(sprite.Sprite):
    """
    This is a class for Hurdle object.

    Attributes:
        image : The image of Hurdle.
        rect : The coordinates of Hurdle.
        back_x : The value of Hurdle's 'x' coordinate on background.
        back_y : The value of Hurdle's 'y' coordinate on background.
    """

    def __init__(self, image_to_load, coo_x, back_x, coo_y):
        """
        The constructor for Hurdle class.

        Parameters:
            image_to_load : The image for Hurdle.
            coo_x, coo_y : The values of coordinates for Hurdle's object.
            back_x : The value of coordinate for Hurdle's object to show on background.
        """

        super().__init__()
        self.image = pg.image.load(image_to_load)
        self.rect = self.image.get_rect()
        self.rect.left = coo_x
        self.rect.bottom = coo_y
        self.back_x = back_x
        self.back_y = coo_y


HURDLES_GROUP = sprite.Group()
