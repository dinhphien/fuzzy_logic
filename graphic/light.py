import pygame
import math
import random


from utils import loader
from utils import config




class Light(pygame.sprite.Sprite):
    def __init__(self, init_x, init_y, index_nav):
        super().__init__()
        self.x = init_x
        self.y = init_y
        self.status = random.randint(0, 2)
        self.IMAGES = [loader.load_image("green_light.png"), loader.load_image("yellow_light.png"), loader.load_image("red_light.png")]
        self.image = self.IMAGES[self.status]
        self.remaining_time = self.cal_remain_time()
        self.index_nav = index_nav
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
    def cal_remain_time(self):
        if self.status == 1:
            return random.randint(1, 5) * config.FPS
        elif self.status == 2:
            return random.randint(1, 3) * config.FPS
        return random.randint(6, 10) * config.FPS

    def update(self):
        self.remaining_time -=1
        if self.remaining_time == 0:
            self.status = (self.status + 1) % 3
            self.image = self.IMAGES[self.status]
            self.remaining_time = self.cal_remain_time()

    def render(self, screen):
        light_font = pygame.font.Font(None, 24)
        label = light_font.render(str(math.floor(self.remaining_time/config.FPS)), True, config.COLOR_LIGHT[self.status])

        screen.blit(label, (self.rect[0] + 25, self.rect[1] + 15))
        screen.blit(self.image, (self.rect[0], self.rect[1]))

