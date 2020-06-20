# --coding:utf-8--


class Operator:
    def __init__(self):
        # self.id = None
        # self.country = None
        # self.state = None
        # self.is_find = None
        # self.is_find_last = None
        # self.position = None
        # self.rel_position = None
        # self.direction_point_pair = None
        # self.seat = None
        # self.camp = None
        # self.mine_injury = None
        # self.is_ground_building = None
        # self.is_formation = None
        # self.formation_id = None
        self.operator_id = -1
        self.type2 = -1
        self.country_id = -1
        self.state = 0
        self.is_found = False
        self.position = None
        self.is_ground_building = False
        self.is_formation = False
        self.formation_id = -1

        self._camp_id = -1  # init by country_id

    def get_camp_id(self):
        return self._camp_id

    def set_camp_id(self, camp_id):
        self._camp_id = camp_id

    @staticmethod
    def parse_json(frame_json_object):
        operator = Operator()
        operator.__dict__ = frame_json_object
        return operator
