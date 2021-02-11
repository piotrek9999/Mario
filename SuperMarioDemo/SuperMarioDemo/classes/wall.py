""" Class Wall. """

import pygame as pg
from pygame import sprite


class Wall(sprite.Sprite):
    """
    This is a class for Wall object.

    Attributes:
        image : The image of Wall.
        rect : The coordinates of Wall.
        back_x : The value of Wall's 'x' coordinate on background.
        back_y : The value of Wall's 'y' coordinate on background.
    """

    def __init__(self, image_to_load, coo_x, back_x, back_y):
        """
        The constructor for Wall class.

        Parameters:
            image_to_load : The image for Wall.
            coo_x : The value of coordinate for Wall's object.
            back_x, back_y : The values of coordinates for Wall's object to show on background.
        """

        super().__init__()
        self.image = pg.image.load(image_to_load)
        self.rect = self.image.get_rect()
        self.rect.left = coo_x
        self.rect.bottom = 512
        self.back_x = back_x
        self.back_y = back_y
