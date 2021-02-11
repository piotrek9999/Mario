""" Class Background. """

import pygame as pg
from pygame import sprite


class Background(sprite.Sprite):
    """
    This is a class for background of game.

    Attributes:
        image : The image of background.
        rect : The coordinates of background.
    """

    def __init__(self, image_to_load):
        """The constructor for background class."""

        super().__init__()

        self.image = pg.image.load(image_to_load)
        self.image = pg.transform.scale(self.image, (13400, 600))
        self.rect = self.image.get_rect()


BACKGROUND = Background('images/background.png')
CLEAR_BACKGROUND = Background('images/background.png')
