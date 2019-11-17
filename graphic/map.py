import pygame
from utils import loader
from utils import config
import xlrd
import math
import numpy as np
from scipy.spatial import distance as dt
from scipy.sparse.csgraph import shortest_path

MAP_NAVS = []
EDGES = []
LIGHTS_POS = []
STONES_POS = []

def find_index_target(target_position):
    if len(MAP_NAVS) == 0:
        return -1
    tar_pos = np.array([target_position])
    coordinates_array = np.array(MAP_NAVS)
    target_distance = dt.cdist(tar_pos, coordinates_array, 'euclidean')
    target_index = np.argmin(target_distance)
    return target_index


class Map(pygame.sprite.Sprite):
    def __init__(self, init_x, init_y):
        super().__init__()
        self.image = loader.load_image("map.png")
        self.rect = self.image.get_rect()
        self.x = init_x
        self.y = init_y

        self.get_map_nav()
        self.get_edges()
        self.shortest_paths = self.find_shortest_paths()
        self.get_light_pos()
        self.get_stone_pos()

    def get_map_nav(self):
        with xlrd.open_workbook('../media/toa-do.xlsx') as book:
            sheet = book.sheet_by_index(0)
            x_coordinate = [x for x in sheet.col_values(1)]
            y_coordinate = [y for y in sheet.col_values(2)]
            for i in range (1, sheet.nrows):
                MAP_NAVS.append((x_coordinate[i], y_coordinate[i]))

    def get_edges(self):
        with xlrd.open_workbook('../media/toa-do.xlsx') as book:
            sheet = book.sheet_by_index(1)
            start_index = [x for x in sheet.col_values(0)]
            end_index = [y for y in sheet.col_values(1)]
            for i in range(1, sheet.nrows):
                EDGES.append((math.floor(start_index[i]), math.floor(end_index[i])))

    def get_light_pos(self):
        with xlrd.open_workbook('../media/toa-do.xlsx') as book:
            sheet = book.sheet_by_index(2)
            coor_x = [x for x in sheet.col_values(0)]
            coor_y = [y for y in sheet.col_values(1)]
            index_nav = [ z for z in sheet.col_values(2)]

            for i in range (1, len(coor_x)):
                LIGHTS_POS.append((coor_x[i], coor_y[i], math.floor(index_nav[i])))

    def get_stone_pos(self):
        with xlrd.open_workbook('../media/toa-do.xlsx') as book:
            sheet = book.sheet_by_index(3)
            coor_x = [x for x in sheet.col_values(0)]
            coor_y = [y for y in sheet.col_values(1)]
            index_nav = [ z for z in sheet.col_values(2)]

            for i in range (1, len(coor_x)):
                STONES_POS.append((coor_x[i], coor_y[i], math.floor(index_nav[i])))


    def find_shortest_paths(self):
        coordinates = np.array(MAP_NAVS)
        pair_distance = dt.squareform(dt.pdist(coordinates))
        for x in range(0, pair_distance.shape[0]):
            for y in range(0, pair_distance.shape[1]):
                if (x,y) not in EDGES and x != y:
                    pair_distance[x,y] = config.MAX_DISTANCE
        distance_array, pr = shortest_path(pair_distance, directed=False, method='D', return_predecessors=True)
        return pr[0]

    def get_shortest_path(self, tar_pos):
        target_index = find_index_target(tar_pos)
        path = []
        if self.shortest_paths[target_index] == -9999:
            return path
        path.append(target_index)
        i = target_index
        while self.shortest_paths[i] != -9999:
            path.append(self.shortest_paths[i])
            i = self.shortest_paths[i]
        path.reverse()
        return path

    def find_nearest_stone(self, pos):
        index = -1
        cur_pos = np.array([pos])
        stones = np.array(STONES_POS)[:,: 2]
        print(stones)
        print(cur_pos)
        distance = dt.cdist(cur_pos, stones, 'euclidean')
        print(distance)
        index = np.argmin(distance)
        if distance[0, index] > 500:
            index = -1
        return index



    # def update(self, update_x, update_y):
    #     self.rect.topleft = self.x - update_x + 600, self.y - update_y + 300
        # self.rect.topleft = update_x, update_y


# map = Map(0, 0)
# map.find_nearest_stone((760, 120))


