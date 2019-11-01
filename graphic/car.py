import pygame


from utils import loader


class Car(pygame.sprite.Sprite):
    def __init__(self, init_x, init_y, init_dir= 0):
        super().__init__()
        self.image = loader.load_image("car2.png")
        self.rect = self.image.get_rect()
        print(self.rect)
        self.x = init_x
        self.y = init_y
        self.dir = init_dir
        self.rect.center = (self.x, self.y)

