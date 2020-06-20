# --coding:utf-8--


# @Author: 逸风
# @Time: 2019-12-18


import json
from entities.cell import Cell


class BattleState:
    """
    态势信息
    """
    def __init__(self):
        self.scenario_id = -1
        self.war_map = []
        self.cells = []

    @staticmethod
    def parse(battle_state_json_string):
        battle_state = BattleState()
        battle_state_json = json.loads(battle_state_json_string)

        battle_state.scenario_id = battle_state_json["scenario"]
        battle_state.cells = [Cell.parse(cell_json) for cell_json in battle_state_json["cells"]]

        return battle_state



