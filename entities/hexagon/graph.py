# --coding:utf-8--

# author:吕石磊 
# create time: 2020/01/08 

from entities.hexagon import hexagon
from entities.hexagon import path


class Graph:

    def __init__(self, min_row=1, min_col=1, max_row=10, max_col=10):
        self._direction_nums = 6
        self._min_row = min_row
        self._min_col = min_col
        self._max_row = max_row
        self._max_col = max_col

    def neighbors(self, offset):
        l_neighbors = [hexagon.hex_offset_neighbor(offset, i) for i in range(self._direction_nums)]
        l_neighbors = [neighbor for neighbor in l_neighbors if self._valid(neighbor)]
        return l_neighbors

    def cost(self, a, b):
        return hexagon.hex_offset_distance(a, b)

    def get_two_hexagon_distance(self, position_a, position_b):  # position,类似(19,23)或[23,21]
        start = hexagon.Hex_Offset(position_a[0], position_a[1])
        goal = hexagon.Hex_Offset(position_b[0], position_b[1])
        get_path = path.get_path(self, start, goal)
        distance = len(get_path) - 1
        return distance

    def get_path(self, start_position, target_position):
        start = hexagon.Hex_Offset(start_position[0], start_position[1])
        goal = hexagon.Hex_Offset(target_position[0], target_position[1])
        all_path = path.get_path(self, start, goal)
        return all_path

    def heuristic(self, a, b):
        return 0

    def _valid(self, offset):
        return self._min_row <= offset.row <= self._max_row and self._min_col <= offset.col <= self._max_col


if __name__ == "__main__":
    graph = Graph(max_row=30, max_col=30)
    the_distance = graph.get_two_hexagon_distance([1, 2], [5, 6])
    the_path = graph.get_path([1, 2], [5, 6])
    # 取(the_path[0].row, the_path[0].col)或(the_path[0][0], the_path[0][1])均可
    print('distance', the_distance)
    print('path', the_path)

