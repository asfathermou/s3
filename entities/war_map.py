# --coding:utf-8--


# @Author: 逸风
# @Time: 2019-12-18


from entities.cell import Cell


class WarMap:
    def __init__(self):
        self.cells = []
        self.rows = -1
        self.cols = -1

    @staticmethod
    def parse(war_map_json_string):
        war_map = WarMap()
        war_map_obj = war_map_json_string['cells']

        war_map.cells = [Cell.parse(war_map_obj) for war_map_obj in war_map_obj]
        war_map.rows = war_map_json_string['rows']
        war_map.cols = war_map_json_string['cols']

        return war_map


