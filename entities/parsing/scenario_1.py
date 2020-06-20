# --coding:utf-8--

# author:吕石磊 
# create time: 2020/01/05 



import json

from entities.parsing.operator import Operator
from utils.file_util import read_to_end
#from utils import file_util


class Scenario:

    def __init__(self):
        self.room_id = None
        self.director = None
        self.room_attr = None
        self.deduction_number = None
        self.deduction_mode = None
        self.rounds = None
        # self.data = None
        self._war_operator_dict = self._build_operator_dict()

    def fetch_operator_by_id(self, operator_id):
        if operator_id in self._war_operator_dict:
            return self._war_operator_dict[operator_id]
        return None

    def _build_operator_dict(self):
        operator_dict = dict()
        for item in self.operators:
            war_operator = Operator.parse_json(item)
            operator_dict[war_operator.operator_id] = war_operator
        return operator_dict

    @staticmethod
    def parse(scenario_json_string):
        scenario = Scenario()
        scenario_json = json.loads(scenario_json_string)
        scenario.__dict__ = scenario_json
        return scenario


if __name__ == "__main__":
    json_file_name = "data/ai_create_room_data.txt"
    json_string = read_to_end(json_file_name)
    print(json_string)
    scenario = Scenario.parse(json_string)
    print(scenario.room_id)
