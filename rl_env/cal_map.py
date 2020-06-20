# coding=utf-8
import time, sys
# sys.path.append("../")
#
# from landwar.core.env.wgloader.loader import Loader
# from landwar.core.env.wgmap.terrain import Terrain

import numpy as np
from numba import jitclass, int32
import data

spec = [('row', int32), ('col', int32)]


def rect_to_cube(row, col):
    # 将偶数列偏移坐标转换为立方坐标 seawar
    x = col
    z = row - (col + (col & 1)) / 2
    y = - x - z
    return x, y, z

    # # 将偶数行偏移坐标转换为立方坐标 landwar
    # x = col - (row - (row & 1)) / 2
    # z = row
    # y = -x - z


def rect_distance(rect1, rect2):
    x1, y1, z1 = rect_to_cube(rect1[0], rect1[1])
    x2, y2, z2 = rect_to_cube(rect2[0], rect2[1])
    return max(abs(x1 - x2), abs(y1 - y2), abs(z1 - z2))


def get_cube_neighbors(x, y, z):
    # maybe out of map
    neighbors = set()
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            dz = -dx - dy
            if abs(dz) > 1:
                continue
            # array_row, array_col = self.cube_to_rect(x+dx, y+dy, z+dz)
            # array_row = int(min(max(array_row, 0), self.row-1))
            # array_col = int(min(max(array_col, 0), self.col-1))

            neighbors.add((x + dx, y + dy, z + dz))

    neighbors.discard((x, y, z))
    return neighbors


class Hex(object):
    def __init__(self, row, col):
        self.row = row  # row number of map array
        self.col = col  # col number of map array

    def set_row_col(self, row, col):
        self.row = row
        self.col = col

    def cube_to_rect(self, x, y, z):
        # 将立方坐标转换为偶数列偏移坐标 seawar
        col = x
        row = z + (x + (x & 1)) / 2

        # # 将立方坐标转换为奇数行偏移坐标 landwar
        # col = x + (z - (z & 1)) / 2
        # row = z

        return row, col

    def cube_distance(self, hex1, hex2):
        return max(abs(hex1[0] - hex2[0]), abs(hex1[1] - hex2[1]), abs(hex1[2] - hex2[2]))

    def get_neighbors(self, row, col):
        x, y, z = rect_to_cube(row, col)
        neighbors = set()
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                dz = -dx - dy
                if abs(dz) > 1:
                    continue
                array_row, array_col = self.cube_to_rect(x + dx, y + dy, z + dz)
                array_row = int(min(max(array_row, 0), self.row - 1))
                array_col = int(min(max(array_col, 0), self.col - 1))
                neighbors.add((array_row, array_col))

        neighbors.discard((row, col))
        return neighbors

    def get_radius(self, row, col, radius):
        x, y, z = rect_to_cube(row, col)
        map_array = np.zeros((self.row, self.col), dtype=np.int32)
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                dz = -dx - dy
                if abs(dz) > radius:
                    continue
                array_row, array_col = self.cube_to_rect(x + dx, y + dy, z + dz)
                array_row = min(max(array_row, 0), self.row - 1)
                array_col = min(max(array_col, 0), self.col - 1)
                map_array[int(array_row), int(array_col)] = 1

        return map_array



    def get_line_neighbors(self, hex, hex1, hex2, distance, line_neighbors):
        cub_neibs = get_cube_neighbors(hex[0], hex[1], hex[2])
        for neib in cub_neibs:
            if neib in line_neighbors:
                continue
            if self.cube_distance(hex1, neib) + self.cube_distance(neib, hex2) == distance:
                line_neighbors.add(neib)
                self.get_line_neighbors(neib, hex1, hex2, distance, line_neighbors)

        return line_neighbors

    def get_line(self, rect1, rect2):
        x1, y1, z1 = rect_to_cube(rect1[0], rect1[1])
        x2, y2, z2 = rect_to_cube(rect2[0], rect2[1])
        distance = self.cube_distance((x1, y1, z1), (x2, y2, z2))
        neighbors = set()
        line_neighbors = self.get_line_neighbors((x1, y1, z1), (x1, y1, z1), (x2, y2, z2), distance, neighbors)
        return [h.cube_to_rect(hex[0], hex[1], hex[2]) for hex in line_neighbors]


def fanjiandaodan_68(dian5, half_blood, fangyuzhi, destroy_level, judge_table, fanjiandaodan_fenpeizhi):
    # fenpei_level 0, 1 for half_blood= True,  fenpei_level 0, 1, 2 for half_blood= False
    '''
    input:
    dian5
        half_blood = True, operator has been has been damaged
        fangyuzhi: currently left fangyuzhi
        destroy_level 0, 1 for half_blood= True,  destroy_level 0, 1, 2 for half_blood= False
        judge_table
        fanjiandaodan_fenpeizhi: hejizhandouli row of judge_table
    return:
        fenpeizhi
    '''
    if destroy_level == 0:
        return 0
    judge_table_row_num = min(max(dian5, -7), 12) + 7
    judge_table_row = judge_table[judge_table_row_num]
    if half_blood:
        fenpei_index = np.min(np.where(judge_table_row >= fangyuzhi)[0])
        return fanjiandaodan_fenpeizhi[int(fenpei_index)]
    else:
        if destroy_level == 2:
            fenpei_index = np.min(np.where(judge_table_row >= fangyuzhi)[0])
            return fanjiandaodan_fenpeizhi[int(fenpei_index)]
        else:  # destroy_level == 1
            fenpei_index = np.min(np.where(judge_table_row >= fangyuzhi * 0.5)[0])
            return fanjiandaodan_fenpeizhi[int(fenpei_index)]


if __name__ == '__main__':
    # terrain = Terrain(Loader(scenario=1231, data_dir="../core"))
    # neighbors = terrain.get_neighbors(3030)
    attack_position_list = []

    h = Hex(8, 8)
    attack_map = h.get_radius(5, 2, 2)
    attack_position = attack_map.nonzero()
    for z in range(len(attack_position[0])):
        attack_position_list.append([attack_position[0][z], attack_position[1][z]])
    print(attack_map)
    # neib = np.where(arr > 0)
    # coords = [xy for xy in zip(neib[0], neib[1])]
    #
    # coords = h.get_neighbors(4, 8)
    # coords = h.get_cube_neighbors(3,5,6)
    #
    # distance = h.rect_distance( (5,4), (11,8) )
    #
    # line_neighbors = h.get_line( (5,4), (11,8) )
    # arr = 0*arr
    # for neib in line_neighbors:
    #     arr[int(neib[0]),int(neib[1])] = 1
    #
    # begin = time.time()
    # print('{}'.format(h.get_radius(30,30,15)))
    # print('Total time {}'.format(time.time() - begin))
    #
    # #fanjiandaodan 6-8
    # judge_table = np.array(data.judge_table)
    # fanjiandaodan_fenpeizhi = np.array([1, 3, 6, 9, 15, 21, 28, 36, 46, 58, 72, 90])
    # fenpeizhi = fanjiandaodan_68(5, False, 4, 1, judge_table, fanjiandaodan_fenpeizhi)
    # a = 1
