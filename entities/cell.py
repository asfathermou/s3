# --coding:utf-8--


# @Author: 逸风
# @Time: 2019-12-18

class Cell:
    def __init__(self):
        self.map_id = -1,
        self.coordinate = (8,20),
        self.terrain = -1,
        self.country_id = -1,
        self.zone_id = -1,
        self.weather = -1,
        self.mark = None

    @staticmethod
    def parse(cell_json):
        cell = Cell()
        cell.map_id = cell_json['map_id']
        cell.coordinate = cell_json['coordinate']
        cell.terrain = cell_json['terrain']
        cell.country_id = cell_json["country_id"]
        cell.zone_id = cell_json['zone_id']
        cell.weather = cell_json['weather']
        cell.mark = cell_json['mark']

        return cell



