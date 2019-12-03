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





class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.fuzzy_monitor = fuzzy_controller.FuzzyController()
        self.path = []
        self.image = loader.load_image("car.png", False)
        self.image_ori = self.image
        self.color = config.BLACK
        self.x = MAP_NAVS[0][0]
        self.y = MAP_NAVS[0][1]

        self.dir = 90.0
        self.speed = 0.3
        self.deviation = 0.0
        self.angle_deviation = 0.0
        self.acceleration = 0
        self.lights = []

        self.desired_dir = 90.0
        self.cur_nav = 0
        self.turn = config.STRAIGHT
        self.central_point = (0,0)
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

    def set_stone(self, stone):
        self.stone = stone

    def cal_distance_stone(self):
        if self.stone.status == config.HIDDEN:
            return config.MAX_DISTANCE
        else:
            distance = math.hypot(self.stone.x - self.x, self.stone.y - self.y)
            if distance < 15:
                return config.MAX_DISTANCE
            else:
                return distance - 15

    # def set_stone(self, stones):
    #     stones_on_path = []
    #     for point_nav in self.path:
    #         if point_nav in stones:
    #             stones_on_path.append(stones[point_nav])
    #         else:
    #             stones_on_path.append(0)
    #     self.stones = stones_on_path

    # def distance_to_nearest_stone(self):
    #     if self.cur_nav != self.path[-1]:
    #         if self.stones[self.cur_nav] != 0 and self.stones[self.cur_nav].status == config.SHOW:
    #             cur_nav_to_car_distance = math.hypot(self.x - MAP_NAVS[self.path[self.cur_nav]][0], self.y - MAP_NAVS[self.path[self.cur_nav]][1])
    #             cur_nav_to_stone_distance = math.hypot(self.stones[self.cur_nav].x - MAP_NAVS[self.path[self.cur_nav]][0],
    #                                                    self.stones[self.cur_nav].y - MAP_NAVS[self.path[self.cur_nav]][1])
    #             if cur_nav_to_car_distance < cur_nav_to_stone_distance:
    #                 distance = math.hypot(self.x - self.stones[self.cur_nav].x, self.y - self.stones[self.cur_nav].y)
    #                 return distance
    #             else:
    #                 pass
    #     return config.MAX_DISTANCE

    def distance_to_nearest_light(self):
        if self.cur_nav != self.path[-1]:
            if self.lights[self.cur_nav + 1] != 0:
                distance = math.hypot(MAP_NAVS[self.path[self.cur_nav +1]][0] - self.x, MAP_NAVS[self.path[self.cur_nav+1]][1] - self.y)
                return distance, self.lights[self.cur_nav + 1].status, math.floor(self.lights[self.cur_nav + 1].remaining_time/60)
        return config.MAX_DISTANCE, 2, 10


    def cal_deviation(self, cur_pos, cur_nav, tar_nav):
        if self.turn == config.STRAIGHT:
            desir_angle = calculate_angle(cur_nav[0], cur_nav[1], tar_nav[0], tar_nav[1])
            cur_angle = calculate_angle(cur_nav[0], cur_nav[1], cur_pos[0], cur_pos[1])
            dev_angle = cal_deviation_angle(cur_angle, desir_angle)
            distance_to_cur_nav = math.hypot(cur_pos[0] - cur_nav[0], cur_pos[1] - cur_nav[1])
            distance_to_line = distance_to_cur_nav * math.sin(math.radians(abs(dev_angle)))

            if dev_angle < 0:
                deviation = config.LANE_SIZE / 2 + distance_to_line
            else:
                deviation = config.LANE_SIZE / 2 - distance_to_line
        else:
            distance_to_central_point = math.hypot(cur_pos[0] - self.central_point[0], cur_pos[1] - self.central_point[1])
            if self.turn == config.LEFT:
                deviation = distance_to_central_point
            else:
                deviation = config.LANE_SIZE - distance_to_central_point

        return deviation

    def control(self):
        target_nav = self.cur_nav + 1
        # distance_target = math.hypot(MAP_NAVS[self.path[target_nav]][0] - self.x,
        #                              MAP_NAVS[self.path[target_nav]][1] - self.y)
        # print(('distance_target', distance_target))
        # print(('Cur_pos', (self.x, self.y), 'Target_pos', (MAP_NAVS[self.path[target_nav]][0], MAP_NAVS[self.path[target_nav]][1])))
        check_pass_nav_point = False
        if self.turn == config.STRAIGHT:
            if self.desired_dir == 90 and self.y > MAP_NAVS[self.path[target_nav]][1]:
                # print('Pass Straight 90')
                check_pass_nav_point = True
            elif self.desired_dir == 0 and self.x > MAP_NAVS[self.path[target_nav]][0]:
                # print('Pass straight 0')
                check_pass_nav_point = True
        else:
            if self.turn == config.LEFT and self.x > MAP_NAVS[self.path[target_nav]][0]:
                # print('Pass left')
                check_pass_nav_point = True
            elif self.turn == config.RIGHT and self.y > MAP_NAVS[self.path[target_nav]][1]:
                # print('Pass right')
                check_pass_nav_point = True
        if check_pass_nav_point:
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

                if MAP_NAVS[self.path[self.cur_nav]][0] == MAP_NAVS[self.path[self.cur_nav +1 ]][0] or MAP_NAVS[self.path[self.cur_nav]][1] == MAP_NAVS[self.path[self.cur_nav + 1]][1]:
                    self.turn = config.STRAIGHT
                    self.central_point = (0,0)
                else:
                    pre_desired_dir = calculate_angle(MAP_NAVS[self.path[self.cur_nav - 1]][0],
                                                   MAP_NAVS[self.path[self.cur_nav - 1]][1],
                                                   MAP_NAVS[self.path[self.cur_nav]][0],
                                                   MAP_NAVS[self.path[self.cur_nav]][1])
                    if cal_deviation_angle(pre_desired_dir, self.desired_dir) > 0:
                        # print('Turn right!')
                        self.turn = config.RIGHT
                        self.central_point = (MAP_NAVS[self.path[self.cur_nav]][0], MAP_NAVS[self.path[self.cur_nav + 1]][1])
                    else:
                        # print('turn left')
                        self.turn = config.LEFT
                        self.central_point = (MAP_NAVS[self.path[self.cur_nav + 1]][0], MAP_NAVS[self.path[self.cur_nav]][1])



                # self.dir = self.desired_dir
                # self.color = config.COLOR_LIGHT[self.cur_nav % 3]
            else:
                self.speed = 0
                return 0
        distance_light, status_light, time_remaining = self.distance_to_nearest_light()
        # distance_stone = self.distance_to_nearest_stone()
        distance_stone = self.cal_distance_stone()
        print(('distance_stone', distance_stone))

        self.deviation = self.cal_deviation((self.x, self.y), MAP_NAVS[self.path[self.cur_nav]],
                                       MAP_NAVS[self.path[self.cur_nav + 1]])
        # print(self.deviation)
        # print((self.deviation, distance_light, status_light, time_remaining, distance_stone))
        deviation_angle = cal_deviation_angle(self.dir, self.desired_dir)
        self.angle_deviation = deviation_angle
        # use fuzzy monitor:
        # print((self.desired_dir, self.dir))
        steering_angle, speed = self.fuzzy_monitor.control(self.deviation, status_light, distance_light, time_remaining, distance_stone, self.angle_deviation)

        # steering:
        if speed >= 0.02:
            # adjust speed:
            # self.speed += self.acceleration
            self.speed = speed
            # self.dir += self.angle_deviation
            # self.dir = self.desired_dir + steering_angle
            self.dir += steering_angle
            # self.dir += x

            if self.dir < 0:
                self.dir += 360
            if self.dir > 360:
                self.dir -= 360
        else:
            self.speed = 0

    def move(self):
        self.control()
        # update position:
        self.x += self.speed * math.cos(math.radians(self.dir))
        self.y += self.speed * math.sin(math.radians(self.dir))

        # print((self.x, self.y))

        self.rect.center = (self.x, self.y)
        self.image, self.rect = rot_center(self.image_ori, self.rect, self.dir)
        # print((self.x, self.y, self.speed, self.dir, self.desired_dir, self.angle_deviation, self.deviation))

    def stop(self):
        self.speed = 0
        self.x += self.speed * math.cos(math.radians(self.dir))
        self.y += self.speed * math.sin(math.radians(self.dir))

        self.rect.center = (self.x, self.y, self.dir)
        self.image, self.rect = rot_center(self.image_ori, self.rect, self.dir)
        # print((self.x, self.y, self.speed, self.dir, self.desired_dir, self.angle_deviation, self.deviation))

    def render(self, screen):
        # pass
        screen.blit(self.image, self.rect)
        # pygame.draw.circle(screen, self.color, (math.floor(self.x), math.floor(self.y)), 5, 5)
