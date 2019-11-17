import pygame
import math

from utils import loader
from utils import config
from graphic.map import MAP_NAVS


# Rotate car.
def rot_center(image, rect, angle):
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, - angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image, rot_rect


def calculate_angle(start_x, start_y, target_x, target_y):
    angle = math.atan2(abs(target_y - start_y), abs(target_x - start_x)) * 180 / math.pi
    if target_y < start_y:
        if target_x > start_x:
            angle = 360 - angle
        else:
            angle += 180
    else:
        if target_x < start_x:
            angle = 180 - angle
    return angle


def cal_deviation_angle(current_angle, desired_angle):
    dev_angle = desired_angle - current_angle
    if dev_angle > 180:
        dev_angle -= 360
    if dev_angle < -180:
        dev_angle += 360
    return dev_angle


def cal_deviation(cur_pos, cur_nav, tar_nav):
    desir_angle = calculate_angle(cur_nav[0], cur_nav[1], tar_nav[0], tar_nav[1])
    cur_angle = calculate_angle(cur_nav[0], cur_nav[1], cur_pos[0], cur_pos[1])
    dev_angle = cal_deviation_angle(cur_angle, desir_angle)
    distance_to_cur_nav = math.hypot(cur_pos[0] - cur_nav[0], cur_pos[1] - cur_nav[1])
    distance_to_line = distance_to_cur_nav * math.sin(math.radians(abs(dev_angle)))
    if dev_angle < 0:
        deviation = 15 - distance_to_line
    else:
        deviation = 15 + distance_to_line
    return deviation


class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.path = []
        self.image = loader.load_image("car.png", False)
        self.image_ori = self.image
        self.x = MAP_NAVS[0][0] - 10
        self.y = MAP_NAVS[0][1] - 10
        self.dir = 90.0
        self.speed = 0.2
        self.deviation = 0.0
        self.angle_deviation = 0.0
        self.acceleration = 0
        self.lights = []
        self.stones = []

        self.desired_dir = 0
        self.cur_nav = 0
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.image, self.rect = rot_center(self.image_ori, self.rect, self.dir)
        # print((self.x, self.y, self.speed, self.dir, self.desired_dir, self.angle_deviation))

    def set_path(self, path):
        self.path = path
        self.desired_dir = calculate_angle(MAP_NAVS[self.path[0]][0], MAP_NAVS[self.path[0]][1],
                                           MAP_NAVS[self.path[1]][0], MAP_NAVS[self.path[1]][1])
        self.cur_nav = 0

    def set_light(self, lights):
        # print(lights)
        # print(self.path)
        lights_on_path = []
        for point_nav in self.path:
            if point_nav in lights:
                lights_on_path.append(lights[point_nav])
            else:
                lights_on_path.append(0)
        self.lights = lights_on_path
        # print("In car")
        # print(self.lights)
        # for light in self.lights:
        #     if light == 0:
        #         pass
        #     else:
        #         print(light.index_nav)

    def set_stone(self, stones):
        stones_on_path = []
        for point_nav in self.path:
            if point_nav in stones:
                stones_on_path.append(stones[point_nav])
            else:
                stones_on_path.append(0)
        self.stones = stones_on_path
        # for stone in self.stones:
        #     if stone ==0:
        #         pass
        #     else:
        #         print(stone.index_nav)

    def distance_to_nearest_stone(self):
        if self.cur_nav != self.path[-1]:
            if self.stones[self.cur_nav] != 0 and self.stones[self.cur_nav].status == config.SHOW:
                cur_nav_to_car_distance = math.hypot(self.x - MAP_NAVS[self.path[self.cur_nav]][0], self.y - MAP_NAVS[self.path[self.cur_nav]][1])
                cur_nav_to_stone_distance = math.hypot(self.stones[self.cur_nav].x - MAP_NAVS[self.path[self.cur_nav]][0],
                                                       self.stones[self.cur_nav].y - MAP_NAVS[self.path[self.cur_nav]][1])
                if cur_nav_to_car_distance < cur_nav_to_stone_distance:
                    distance = math.hypot(self.x - self.stones[self.cur_nav].x, self.y - self.stones[self.cur_nav].y)
                    return distance
                else:
                    pass
        return float('nan')

    def distance_to_nearest_light(self):
        if self.cur_nav != self.path[-1]:
            if self.lights[self.cur_nav + 1] != 0:
                # print(self.path[i])
                distance = math.hypot(MAP_NAVS[self.path[self.cur_nav +1]][0] - self.x, MAP_NAVS[self.path[self.cur_nav+1]][1] - self.y)
                return distance, self.lights[self.cur_nav + 1].status, math.floor(self.lights[self.cur_nav + 1].remaining_time/60)
        return float('nan'), float('nan'), float('nan')

    def control(self):
        target_nav = self.cur_nav + 1
        distance_target = math.hypot(MAP_NAVS[self.path[target_nav]][0] - self.x,
                                     MAP_NAVS[self.path[target_nav]][1] - self.y)
        # print(distance_target)
        if distance_target < 10:
            print(
                "---------------------------------------------------------------------------------------------------------")
            print(
                "---------------------------------------------------------------------------------------------------------")
            print(
                "---------------------------------------------------------------------------------------------------------")
            print(
                "---------------------------------------------------------------------------------------------------------")
            print(
                "---------------------------------------------------------------------------------------------------------")
            if target_nav < len(self.path) - 1:
                self.cur_nav += 1
                self.desired_dir = calculate_angle(MAP_NAVS[self.path[self.cur_nav]][0],
                                                   MAP_NAVS[self.path[self.cur_nav]][1],
                                                   MAP_NAVS[self.path[self.cur_nav + 1]][0],
                                                   MAP_NAVS[self.path[self.cur_nav + 1]][1])
            else:
                self.speed = 0
                return 0
        dt_light, st, ti = self.distance_to_nearest_light()
        dt_stone = self.distance_to_nearest_stone()
        print(dt_stone)
        print(dt_light, st, ti)

        # steering:
        self.deviation = cal_deviation((self.x, self.y), MAP_NAVS[self.path[self.cur_nav]],
                                       MAP_NAVS[self.path[self.cur_nav + 1]])
        deviation_angle = cal_deviation_angle(self.dir, self.desired_dir)
        self.angle_deviation = deviation_angle / 10
        self.dir += self.angle_deviation
        if self.dir < 0:
            self.dir += 360
        if self.dir > 360:
            self.dir -= 360
        # adjust speed:
        self.speed += self.acceleration

    def move(self):
        self.control()
        # update position:
        self.x += self.speed * math.cos(math.radians(self.dir))
        self.y += self.speed * math.sin(math.radians(self.dir))

        self.rect.center = (self.x, self.y)
        self.image, self.rect = rot_center(self.image_ori, self.rect, self.dir)
        # print((self.x, self.y, self.speed, self.dir, self.desired_dir, self.angle_deviation, self.deviation))

    def stop(self):
        self.speed = 0
        self.x += self.speed * math.cos(math.radians(self.dir))
        self.y += self.speed * math.sin(math.radians(self.dir))

        self.rect.center = (self.x, self.y)
        self.image, self.rect = rot_center(self.image_ori, self.rect, self.dir)
        # print((self.x, self.y, self.speed, self.dir, self.desired_dir, self.angle_deviation, self.deviation))

    def render(self, screen):
        screen.blit(self.image, self.rect)
