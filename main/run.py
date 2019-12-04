import sys
import random
import xlwt
import xlrd
import math

import pygame
from pygame.locals import *

from graphic import map
from graphic import car
from graphic import light, stone
from utils import config
from graphic.map import MAP_NAVS, LIGHTS_POS, STONES_POS
from utils import loader


# def write_coordinates(tracks):
#     workbook = xlwt.Workbook(encoding='ascii')
#     worksheet = workbook.add_sheet('Map')
#     worksheet.write(0, 0, 'Index')
#     worksheet.write(0, 1, 'X')
#     worksheet.write(0, 2, 'Y')
#     for (k, v) in tracks.items():
#         worksheet.write(k, 0, k)
#         worksheet.write(k, 1, v[0])
#         worksheet.write(k, 2, v[1])
#     workbook.save('../media/toa-do.xlsx')

def main():
    fps_clock = pygame.time.Clock()
    map_city = map.Map(0, 0)

    flag = 0
    tracks = MAP_NAVS
    lights_pos = LIGHTS_POS
    # stones_pos = STONES_POS

    path = [0, 1, 2,3, 14,15, 13, 10]
    target_pos = tracks[path[-1]]
    rect_target = pygame.draw.circle(screen, (255, 0, 0), (math.floor(target_pos[0]), math.floor(target_pos[1])), 20, 20)
    car_player = car.Car()
    lights = []
    lights_on_path = {}
    # stones_on_path = {}
    # stones = []
    for i in range(len(lights_pos)):
        lights.append(light.Light(lights_pos[i][0], lights_pos[i][1], lights_pos[i][2]))
    # for i in range(len(stones_pos)):
    #     stones.append(stone.Stone(stones_pos[i][0], stones_pos[i][1], stones_pos[i][2]))
    rock = stone.Stone(0, 0, 0)


    moving = False
    running = True
    is_playing = -1
    while running:
        if is_playing == -1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        is_playing = 0
                elif event.type == MOUSEBUTTONDOWN:
                    distance = math.hypot(event.pos[0] - rect_target.center[0], event.pos[1] - rect_target.center[1])
                    if distance < 20:
                        moving = True
                    print(event.pos)
                elif event.type == MOUSEBUTTONUP:
                    moving = False
                elif event.type == MOUSEMOTION and moving:
                    rect_target.move_ip(event.rel)
                else:
                    pass
        elif is_playing == 0:
            path = map_city.get_shortest_path(rect_target.center)
            rect_target.center = (math.floor(tracks[path[-1]][0]), math.floor(tracks[path[-1]][1]))
            car_player.set_path(path)
            for index_nav in path:
                for i in range(len(lights_pos)):
                    if index_nav == lights_pos[i][2]:
                        lights_on_path[index_nav] = lights[i]
                        break
                # for i in range(len(stones_pos)):
                #     if index_nav == stones_pos[i][2]:
                #         stones_on_path[index_nav] = stones[i]
                #         break

            car_player.set_light(lights_on_path)
            car_player.set_stone(rock)
            # car_player.set_stone(stones_on_path)

            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         running = False
            #     elif event.type == pygame.KEYDOWN:
            #         if event.key == pygame.K_SPACE:
            #             is_playing = 1
            #     elif event.type == MOUSEBUTTONDOWN:
            #         print(event.pos)
            is_playing = 1

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    # index_stone = map_city.find_nearest_stone(event.pos)
                    # if index_stone != -1:
                    #     stones[index_stone].toggle_stone()

                    # print(event.pos)
                    nor_pos, indx_nav = map_city.nor_stone_position(event.pos, car_player.path)
                    print(nor_pos, indx_nav)
                    if not math.isnan(indx_nav):
                        rock.show_stone(nor_pos, indx_nav, 5)
                    # print(index_stone)
            for i in range(len(lights)):
                lights[i].update()
            rock.update_time_remaining()
            car_player.move()

        screen.blit(map_city.image, map_city.rect)
        rect_target = pygame.draw.circle(screen, config.RED, rect_target.center, 15, 15)
        # for i in range(len(path) -1):
        #     point1 = (math.floor(tracks[path[i]][0]), math.floor(tracks[path[i]][1]))
        #     point2 = (math.floor(tracks[path[i +1]][0]), math.floor(tracks[path[i +1]][1]))
        #     pygame.draw.line(screen, config.BLUE, point1, point2, 7)

        for i in range(len(lights)):
            lights[i].render(screen)
        rock.render(screen)
        # for i in range(len(stones)):
        #     stones[i].render(screen)

        for i in range(len(tracks)):
            image = font.render(str(i), True, config.RED)
            screen.blit(image, (math.floor(tracks[i][0]), math.floor(tracks[i][1])))
            pygame.draw.circle(screen, config.BLACK, (math.floor(tracks[i][0]), math.floor(tracks[i][1])), 5, 5)

        # for i in range(len(stones_pos)):
        #     pygame.draw.circle(screen, config.BLACK, (math.floor(stones_pos[i][0]), math.floor(stones_pos[i][1])), 5, 5)

        car_player.render(screen)
        pygame.display.flip()
        fps_clock.tick(config.FPS)


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((config.WIDTH_APP,config.HEIGHT_APP))
    pygame.display.set_caption(config.CAPTION_APP)
    font = pygame.font.Font(None, 24)

    main()

    pygame.quit()
    sys.exit(0)








