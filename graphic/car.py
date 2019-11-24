import pygame
import math

from utils import loader
from utils import config
from graphic.map import MAP_NAVS
from fuzzy_logic import fuzzy_controller


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
        self.fuzzy_monitor = fuzzy_controller.FuzzyController()
        self.path = []
        self.image = loader.load_image("car.png", False)
        self.image_ori = self.image
        self.color = config.BLACK
        self.x = MAP_NAVS[0][0] - 10
        self.y = MAP_NAVS[0][1] - 10
        self.dir = 90.0
        self.speed = 0.3
        self.deviation = 0.0
        self.angle_deviation = 0.0
        self.acceleration = 0
        self.lights = []
        self.stones = []

        self.desired_dir = 0
        self.cur_nav = 0
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.image, self.rect = rot_center(self.image_ori, self.rect, self.dir)

    def set_path(self, path):
        self.path = path
        self.desired_dir = calculate_angle(MAP_NAVS[self.path[0]][0], MAP_NAVS[self.path[0]][1],
                                           MAP_NAVS[self.path[1]][0], MAP_NAVS[self.path[1]][1])
        self.dir = self.desired_dir
        self.cur_nav = 0

    def set_light(self, lights):
        lights_on_path = []
        for point_nav in self.path:
            if point_nav in lights:
                lights_on_path.append(lights[point_nav])
            else:
                lights_on_path.append(0)
        self.lights = lights_on_path

    def set_stone(self, stones):
        stones_on_path = []
        for point_nav in self.path:
            if point_nav in stones:
                stones_on_path.append(stones[point_nav])
            else:
                stones_on_path.append(0)
        self.stones = stones_on_path

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
                distance = math.hypot(MAP_NAVS[self.path[self.cur_nav +1]][0] - self.x, MAP_NAVS[self.path[self.cur_nav+1]][1] - self.y)
                return distance, self.lights[self.cur_nav + 1].status, math.floor(self.lights[self.cur_nav + 1].remaining_time/60)
        return 1000, 2, 15

    def control(self):
        target_nav = self.cur_nav + 1
        distance_target = math.hypot(MAP_NAVS[self.path[target_nav]][0] - self.x,
                                     MAP_NAVS[self.path[target_nav]][1] - self.y)
        print(('distance_target', distance_target))
        if distance_target < 2:
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
                # self.color = config.COLOR_LIGHT[self.cur_nav % 3]
            else:
                self.speed = 0
                return 0
        distance_light, status_light, time_remaining = self.distance_to_nearest_light()
        distance_stone = self.distance_to_nearest_stone()

        self.deviation = cal_deviation((self.x, self.y), MAP_NAVS[self.path[self.cur_nav]],
                                       MAP_NAVS[self.path[self.cur_nav + 1]])
        print((self.dir, self.desired_dir, ))
        deviation_angle = cal_deviation_angle(self.dir, self.desired_dir)
        self.angle_deviation = deviation_angle
        # use fuzzy monitor:
        x, y = self.fuzzy_monitor.control(self.deviation, status_light, distance_light, time_remaining, distance_stone, self.angle_deviation)

        # steering:
        # self.dir += self.angle_deviation
        self.dir = self.desired_dir + x
        # self.dir += x
        if self.dir < 0:
            self.dir += 360
        if self.dir > 360:
            self.dir -= 360
        # adjust speed:
        # self.speed += self.acceleration
        self.speed = y

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
        # pygame.draw.circle(screen, self.color, (math.floor(self.x), math.floor(self.y)), 5, 5)
