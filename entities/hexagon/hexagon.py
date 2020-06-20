# --coding:utf-8--

# author:吕石磊 
# create time: 2020/01/08 

import collections


'''======================Cube Coordination======================'''
_Hex_Cube = collections.namedtuple("Hex_Cube", ['q', 'r', 's'])


def Hex_Cube(q, r, s):
    assert not (round(q + r + s) != 0), "q + r + s must be 0"
    return _Hex_Cube(q, r, s)


def hex_cube_add(a, b):
    return Hex_Cube(a.q + b.q, a.r + b.r, a.s + b.s)


def hex_cube_subtract(a, b):
    return Hex_Cube(a.q - b.q, a.r - b.r, a.s - b.s)


hex_directions = [Hex_Cube(1, 0, -1), Hex_Cube(1, -1, 0), Hex_Cube(0, -1, 1), Hex_Cube(-1, 0, 1), Hex_Cube(-1, 1, 0),
                  Hex_Cube(0, 1, -1)]


def hex_cube_direction(direction):
    return hex_directions[direction]


def hex_cube_neighbor(cube, direction):
    return hex_cube_add(cube, hex_cube_direction(direction))


def hex_cube_length(cube):
    return (abs(cube.q) + abs(cube.r) + abs(cube.s)) // 2


def hex_cube_distance(a, b):
    return hex_cube_length(hex_cube_subtract(a, b))


'''======================Offset Coordination======================'''
Hex_Offset = collections.namedtuple("OffsetCoord", ["row", "col"])


def offset_from_cube(hex_cube):
    col = hex_cube.q
    row = hex_cube.r + (hex_cube.q + (hex_cube.q & 1)) // 2
    return Hex_Offset(row,col)


def offset_to_cube(hex_offset):
    q = hex_offset.col
    r = hex_offset.row - (hex_offset.col + (hex_offset.col & 1)) // 2
    s = -q - r
    return Hex_Cube(q, r, s)


def hex_offset_neighbor(offset, direction):
    hex_cube = offset_to_cube(offset)
    neighbor = hex_cube_neighbor(hex_cube,direction)
    return offset_from_cube(neighbor)


def hex_offset_distance(a, b):
    cube_a = offset_to_cube(a)
    cube_b = offset_to_cube(b)
    return hex_cube_distance(cube_a, cube_b)


if __name__ == "__main__":
    pass
