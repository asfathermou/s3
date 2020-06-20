# --coding:utf-8--


class Frame:
    def __init__(self):
        self.frame_id = None
        self.frame_type = None
        self.room_id = None
        self.camp_id = None
        self.round = None
        self.time_interval = None
        self.operators = None
        self.judgements = None
        self.intercept_expel_winner_camp_ids = None
        self.other_information = None
        self.score = None

    def get_time_section_id(self):
        return self.time_interval

    @staticmethod
    def parse_json(frame_json_object):
        frame = Frame()
        frame.__dict__ = frame_json_object
        return frame
