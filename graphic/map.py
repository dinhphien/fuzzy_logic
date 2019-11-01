import pygame
from utils import loader
from utils import config


class Map(pygame.sprite.Sprite):
    def __init__(self, init_x, init_y):
        super().__init__()
        self.image = loader.load_image("map.png")
        self.rect = self.image.get_rect()
        print(self.rect)
        self.x = init_x
        self.y = init_y

    def update(self, update_x, update_y):
        self.rect.topleft = self.x - update_x + 600, self.y - update_y + 300
        # self.rect.topleft = update_x, update_y




