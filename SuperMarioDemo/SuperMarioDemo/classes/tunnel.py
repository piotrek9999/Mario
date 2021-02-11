""" Class Tunnel. """

import pygame as pg
from pygame import sprite


class Tunnel(sprite.Sprite):
    """
    This is a class for Tunnel object.

    Attributes:
        image : The image of Tunnel.
        rect : The coordinates of Tunnel.
        back_x : The value of Tunnel's 'x' coordinate on background.
        back_y : The value of Tunnel's 'y' coordinate on background.
    """

    def __init__(self, image_to_load, coo_x, back_x, back_y):
        """
        The constructor for Tunnel class.

        Parameters:
            image_to_load : The image for Tunnel.
            coo_x, coo_y : The values of coordinates for Tunnel's object.
            back_x, back_y : The values of coordinates for Tunnel's object to show on background.
        """

        super().__init__()
        self.image = pg.image.load(image_to_load)
        self.rect = self.image.get_rect()
        self.rect.x = coo_x
        self.rect.y = back_y
        self.back_x = back_x
        self.back_y = back_y


OBJECT_GROUP = sprite.Group()
