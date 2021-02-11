""" Class Money """
import pygame as pg
from pygame import sprite


class Money(sprite.Sprite):
    """
    This is a class for Money object.

    Attributes:
        image : The image of Money.
        rect : The coordinates of Money.
        back_x : The value of Money's 'x' coordinate on background.
    """

    def __init__(self, image_to_load, coo_x, coo_y, back_x):
        """
        The constructor for Money class.

        Parameters:
            image_to_load : The image for Money.
            coo_x, coo_y : The values of coordinates for Money's object.
            back_x : The value of coordinate for Money's object to show on background.
        """

        super().__init__()
        self.image = pg.image.load(image_to_load)
        self.image = pg.transform.scale(self.image, (30, 50))
        self.rect = self.image.get_rect()
        self.rect.x = coo_x
        self.rect.y = coo_y
        self.back_x = back_x


MONEY_GROUP = sprite.Group()
