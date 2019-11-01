import os
import sys
import pygame
from pygame.locals import *


def load_image(relative_path, transparent=True):
    media_path = "../media"
    file_path = os.path.join(media_path, relative_path)
    image = pygame.image.load(file_path)
    if transparent == True:
        image = image.convert()
        # colorkey = image.get_at((0, 0))
        # image.set_colorkey(colorkey, RLEACCEL)
    else:
        image = image.convert_alpha()
    return image

