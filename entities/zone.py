# --coding:utf-8--


# @Author: 逸风
# @Time: 2019-12-22 17:56


class Zone:
    def __init__(self):
        self.id = -1
        self.center = ""
        self.centre_point = -1
        self.name = ""

    @staticmethod
    def parse(zones_json_object):
        zones = Zone()
        zones.__dict__ = zones_json_object
        return zones


