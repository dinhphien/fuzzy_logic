import pygame

from utils import loader, config


class Stone(pygame.sprite.Sprite):
    def __init__(self, init_x, init_y, index_nav):
        super().__init__()
        self.x = init_x
        self.y = init_y
        self.image_ori = loader.load_image('stone.png')
        self.image = self.image_ori
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        self.index_nav = index_nav
        self.status = config.HIDDEN

    def toggle_stone(self):
        if self.status == config.HIDDEN:
            self.status = config.SHOW
        else:
            self.status = config.HIDDEN

    def render(self, screen):
        if self.status == config.SHOW:
            screen.blit(self.image, (self.rect[0], self.rect[1]))
        else:
            pass






