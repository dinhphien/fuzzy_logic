import sys
import random

import pygame
from pygame.locals import *

from graphic import map
from graphic import car
from utils import config


def main():
    fps_clock = pygame.time.Clock()
    running = True

    map_city = map.Map(0, 0)
    car_player = car.Car(228, 45)

    is_playing = False
    flag = 0
    tracks = {}
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                flag += 1
                tracks[flag] = event.pos
                print(event.pos)



        if not is_playing:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                is_playing = True

        # screen.blit(background, (0, 0))
        # x += 3
        # y += 3
        # map_city.update(x, y)
        screen.blit(map_city.image, map_city.rect)
        screen.blit(car_player.image, car_player.rect)
        for (k, v) in tracks.items():
            image = font.render(str(k), True, (255, 0, 0))
            screen.blit(image, v)
            pygame.draw.circle(screen, (0,0,0), v, 5, 5)


        pygame.display.flip()
        fps_clock.tick(config.FPS)






if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((config.WIDTH_APP,config.HEIGHT_APP))
    pygame.display.set_caption(config.CAPTION_APP)
    font = pygame.font.Font(None, 24)


    # new background surface
    # background = pygame.Surface(screen.get_size())
    # background = background.convert_alpha(background)
    # background.fill((82, 86, 94))

    main()

    pygame.quit()
    sys.exit(0)








