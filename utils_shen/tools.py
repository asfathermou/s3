from rl_env.cal_map import Hex


def get_reach_range(row, col, radius, map_row, map_col):
    reach_position_list = []
    h = Hex(map_row + 1, map_col + 1)
    reach_map = h.get_radius(row, col, radius)
    reach_position = reach_map.nonzero()
    for z in range(len(reach_position[0])):
        r = reach_position[0][z]
        c = reach_position[1][z]
        if 0 < r < map_row + 1 and 0 < c < map_col + 1:
            reach_position_list.append([r,c])
    return reach_position_list

if __name__ == '__main__':

    attack_position_list = get_reach_range(8,8,2,8,8)
    print(attack_position_list)

