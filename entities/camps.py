# --coding:utf-8--


# @Author: 逸风
# @Time: 2019-12-22 17:54


class Camps:
    def __init__(self):
        self.camp = -1
        self.name = ""
        self.satellite_scout_num = 0

    @staticmethod
    def parse(camps_json_object):
        camp = Camps()
        camp.__dict__ = camps_json_object
        return camp



