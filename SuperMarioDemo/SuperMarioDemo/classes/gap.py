""" Class Gap. """

import pygame as pg
from pygame import sprite


class Gap(sprite.Sprite):
    """
    This is a class for Gap object.

    Attributes:
        image : The image of Gap.
        rect : The coordinates of Gap.
        back_x : The value of Gap's 'x' coordinate on background.
    """

    def __init__(self, image_to_load, coo_x, back_x):
        """
        The constructor for Gap class.

        Parameters:
            image_to_load : The image for Gap.
            coo_x : The value of coordinate for Gap's object.
            back_x : The value of coordinate for Gap's object to show on background.
        """

        super().__init__()
        self.image = pg.image.load(image_to_load)
        self.rect = self.image.get_rect()
        self.rect.x = coo_x
        self.rect.y = 510
        self.back_x = back_x


GAP_GROUP = sprite.Group()
