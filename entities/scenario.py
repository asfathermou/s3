# --coding:utf-8--


# @Author: 逸风
# @Time: 2019-12-18


import json
from entities.season import Season
from entities.camps import Camps
from entities.zone import Zone
from entities.countries import Countries
from entities.seats import Seats
from entities.war_operator import WarOperator as Operator
from entities.war_map import WarMap
from entities.hexagon.graph import Graph
import logging

class Scenario:
    def __init__(self):
        self.scenario_id = ""
        self.name = ""
        self.season_list = []
        self.camps = []
        self.zones = []
        self.countries = []
        self.seats = []
        self.operators = []
        self.war_map = []
        # self._war_operator_dict = self._build_operator_dict()
        self._war_operator_dict = None
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='tmp/tests.log',
                            filemode='w')

    @staticmethod
    def parse(scenario_json_object):
        scenario = Scenario()
        scenario.scenario_id = scenario_json_object['scenario']["scenario_id"]
        scenario.name = scenario_json_object['scenario']["name"]
        scenario.season_list = [Season.parse(scenario_json_object) for scenario_json_object in scenario_json_object['scenario']["season_list"]]
        scenario.camps = [Camps.parse(scenario_json_object) for scenario_json_object in scenario_json_object['scenario']['camps']]
        scenario.zones = [Zone.parse(scenario_json_object) for scenario_json_object in scenario_json_object['scenario']['zones']]
        scenario.countries = [Countries.parse(scenario_json_object) for scenario_json_object in scenario_json_object['scenario']['countries']]
        scenario.seats = [Seats.parse(scenario_json_object) for scenario_json_object in scenario_json_object['scenario']['seats']]

        scenario.graph = Graph(max_row=int(scenario_json_object['war_map'][0]['rows']), max_col=int(scenario_json_object['war_map'][0]['cols']))
        scenario.operators = [Operator.parse(scenario_json_object) for scenario_json_object in scenario_json_object['scenario']['operators']]

        # 需先建立算子(operators)，再建立算子字典(_war_operator_dict),再初始化编队状态(_init_formation_state)
        scenario._war_operator_dict = scenario._build_operator_dict()
        scenario._init_formation_state()

        scenario._init_operators_camp_id()

        scenario.war_map = WarMap.parse(scenario_json_object['war_map'][0])

        return scenario

    def _init_operators_camp_id(self):
        for war_operator in self.operators:
            war_operator._camp_id = self.fetch_camp_id_by_country_id(war_operator.country_id)

    def fetch_camp_id_by_country_id(self, country_id):
        for country in self.countries:
            if country.id == country_id:
                return country.camp
        return -1

    def _init_formation_state(self):
        for war_operator in self.operators:
            if war_operator.is_formation:
                states = []
                for member_id in war_operator.members:
                    member = self._fetch_operator_by_id(member_id)
                    if member:
                        states.append(member.state)
                if not states:
                    print(war_operator.operator_id)
                war_operator.state = min(states)

    def update_operator(self, frame_operator):
        logging.debug("请求的内容：%s" % frame_operator)
        target_operator = self._fetch_operator_by_id(frame_operator["id"])
        target_operator.is_find = frame_operator["is_find"]
        target_operator.position = frame_operator["position"]
        target_operator.state = frame_operator["state"]

        if "is_formation" in frame_operator and frame_operator["is_formation"]:
            target_operator.is_formation = True
            target_operator.formation_id = frame_operator["formation_id"]
        else:
            target_operator.is_formation = False

        # attributes = [a for a in target_operator.attributes if a.attribute_name == "state"]
        # if len(attributes) >= 1:
        #     attribute = attributes[0]
        #     attribute.attribute_value = str(frame_operator["state"])
        #
        #
        # else:
        #     print("想定数据有问题")
        return target_operator

    def _fetch_operator_by_id(self, operator_id):
        if operator_id in self._war_operator_dict:
            return self._war_operator_dict[operator_id]
        return None

    def _build_operator_dict(self):
        operator_dict = dict()
        for item in self.operators:
            operator_dict[item.operator_id] = item
        return operator_dict

    @staticmethod
    def _test():
        input = '''
        
        {
    "data": {
        "war_map": [
            {
                "cells": [
                    {
                        "map_id": 63601,
                        "coordinate": "1,1",
                        "terrain": "3",
                        "country_id": 1,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63602,
                        "coordinate": "2,1",
                        "terrain": "3",
                        "country_id": 1,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63603,
                        "coordinate": "3,1",
                        "terrain": "3",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63604,
                        "coordinate": "4,1",
                        "terrain": "3",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63605,
                        "coordinate": "5,1",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63606,
                        "coordinate": "6,1",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63607,
                        "coordinate": "7,1",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63608,
                        "coordinate": "8,1",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63609,
                        "coordinate": "9,1",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63610,
                        "coordinate": "10,1",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63611,
                        "coordinate": "1,2",
                        "terrain": "3",
                        "country_id": 1,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63612,
                        "coordinate": "2,2",
                        "terrain": "4",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63613,
                        "coordinate": "3,2",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63614,
                        "coordinate": "4,2",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63615,
                        "coordinate": "5,2",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63616,
                        "coordinate": "6,2",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63617,
                        "coordinate": "7,2",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63618,
                        "coordinate": "8,2",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63619,
                        "coordinate": "9,2",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63620,
                        "coordinate": "10,2",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63621,
                        "coordinate": "1,3",
                        "terrain": "3",
                        "country_id": 1,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": "海口"
                    },
                    {
                        "map_id": 63622,
                        "coordinate": "2,3",
                        "terrain": "4",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63623,
                        "coordinate": "3,3",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63624,
                        "coordinate": "4,3",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63625,
                        "coordinate": "5,3",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63626,
                        "coordinate": "6,3",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63627,
                        "coordinate": "7,3",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63628,
                        "coordinate": "8,3",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63629,
                        "coordinate": "9,3",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63630,
                        "coordinate": "10,3",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63631,
                        "coordinate": "1,4",
                        "terrain": "4",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63632,
                        "coordinate": "2,4",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63633,
                        "coordinate": "3,4",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63634,
                        "coordinate": "4,4",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63635,
                        "coordinate": "5,4",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63636,
                        "coordinate": "6,4",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63637,
                        "coordinate": "7,4",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63638,
                        "coordinate": "8,4",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63639,
                        "coordinate": "9,4",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63640,
                        "coordinate": "10,4",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63641,
                        "coordinate": "1,5",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63642,
                        "coordinate": "2,5",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63643,
                        "coordinate": "3,5",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63644,
                        "coordinate": "4,5",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63645,
                        "coordinate": "5,5",
                        "terrain": "5",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": "西表岛"
                    },
                    {
                        "map_id": 63646,
                        "coordinate": "6,5",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63647,
                        "coordinate": "7,5",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63648,
                        "coordinate": "8,5",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63649,
                        "coordinate": "9,5",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63650,
                        "coordinate": "10,5",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63651,
                        "coordinate": "1,6",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63652,
                        "coordinate": "2,6",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63653,
                        "coordinate": "3,6",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63654,
                        "coordinate": "4,6",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63655,
                        "coordinate": "5,6",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63656,
                        "coordinate": "6,6",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63657,
                        "coordinate": "7,6",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63658,
                        "coordinate": "8,6",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63659,
                        "coordinate": "9,6",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63660,
                        "coordinate": "10,6",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63661,
                        "coordinate": "1,7",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63662,
                        "coordinate": "2,7",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63663,
                        "coordinate": "3,7",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63664,
                        "coordinate": "4,7",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63665,
                        "coordinate": "5,7",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63666,
                        "coordinate": "6,7",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63667,
                        "coordinate": "7,7",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63668,
                        "coordinate": "8,7",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63669,
                        "coordinate": "9,7",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63670,
                        "coordinate": "10,7",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63671,
                        "coordinate": "1,8",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63672,
                        "coordinate": "2,8",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63673,
                        "coordinate": "3,8",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63674,
                        "coordinate": "4,8",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63675,
                        "coordinate": "5,8",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63676,
                        "coordinate": "6,8",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63677,
                        "coordinate": "7,8",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63678,
                        "coordinate": "8,8",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63679,
                        "coordinate": "9,8",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63680,
                        "coordinate": "10,8",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63681,
                        "coordinate": "1,9",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63682,
                        "coordinate": "2,9",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63683,
                        "coordinate": "3,9",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63684,
                        "coordinate": "4,9",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63685,
                        "coordinate": "5,9",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63686,
                        "coordinate": "6,9",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63687,
                        "coordinate": "7,9",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63688,
                        "coordinate": "8,9",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63689,
                        "coordinate": "9,9",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63690,
                        "coordinate": "10,9",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63691,
                        "coordinate": "1,10",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63692,
                        "coordinate": "2,10",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63693,
                        "coordinate": "3,10",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63694,
                        "coordinate": "4,10",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63695,
                        "coordinate": "5,10",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63696,
                        "coordinate": "6,10",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63697,
                        "coordinate": "7,10",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63698,
                        "coordinate": "8,10",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63699,
                        "coordinate": "9,10",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63700,
                        "coordinate": "10,10",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63701,
                        "coordinate": "1,11",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63702,
                        "coordinate": "2,11",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63703,
                        "coordinate": "3,11",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63704,
                        "coordinate": "4,11",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63705,
                        "coordinate": "5,11",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63706,
                        "coordinate": "6,11",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63707,
                        "coordinate": "7,11",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63708,
                        "coordinate": "8,11",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63709,
                        "coordinate": "9,11",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63710,
                        "coordinate": "10,11",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63711,
                        "coordinate": "1,12",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63712,
                        "coordinate": "2,12",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63713,
                        "coordinate": "3,12",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63714,
                        "coordinate": "4,12",
                        "terrain": "6",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63715,
                        "coordinate": "5,12",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63716,
                        "coordinate": "6,12",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63717,
                        "coordinate": "7,12",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63718,
                        "coordinate": "8,12",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63719,
                        "coordinate": "9,12",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63720,
                        "coordinate": "10,12",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63721,
                        "coordinate": "1,13",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63722,
                        "coordinate": "2,13",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63723,
                        "coordinate": "3,13",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63724,
                        "coordinate": "4,13",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63725,
                        "coordinate": "5,13",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63726,
                        "coordinate": "6,13",
                        "terrain": "5",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": "永兴岛"
                    },
                    {
                        "map_id": 63727,
                        "coordinate": "7,13",
                        "terrain": "5",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": "甘泉岛"
                    },
                    {
                        "map_id": 63728,
                        "coordinate": "8,13",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63729,
                        "coordinate": "9,13",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63730,
                        "coordinate": "10,13",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63731,
                        "coordinate": "1,14",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63732,
                        "coordinate": "2,14",
                        "terrain": "5",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": "金银岛"
                    },
                    {
                        "map_id": 63733,
                        "coordinate": "3,14",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63734,
                        "coordinate": "4,14",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63735,
                        "coordinate": "5,14",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63736,
                        "coordinate": "6,14",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63737,
                        "coordinate": "7,14",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63738,
                        "coordinate": "8,14",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63739,
                        "coordinate": "9,14",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63740,
                        "coordinate": "10,14",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63741,
                        "coordinate": "1,15",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63742,
                        "coordinate": "2,15",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63743,
                        "coordinate": "3,15",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63744,
                        "coordinate": "4,15",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63745,
                        "coordinate": "5,15",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63746,
                        "coordinate": "6,15",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63747,
                        "coordinate": "7,15",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63748,
                        "coordinate": "8,15",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63749,
                        "coordinate": "9,15",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63750,
                        "coordinate": "10,15",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63751,
                        "coordinate": "1,16",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63752,
                        "coordinate": "2,16",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63753,
                        "coordinate": "3,16",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63754,
                        "coordinate": "4,16",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63755,
                        "coordinate": "5,16",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63756,
                        "coordinate": "6,16",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63757,
                        "coordinate": "7,16",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63758,
                        "coordinate": "8,16",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63759,
                        "coordinate": "9,16",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63760,
                        "coordinate": "10,16",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63761,
                        "coordinate": "1,17",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63762,
                        "coordinate": "2,17",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63763,
                        "coordinate": "3,17",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63764,
                        "coordinate": "4,17",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63765,
                        "coordinate": "5,17",
                        "terrain": "5",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": "中业岛"
                    },
                    {
                        "map_id": 63766,
                        "coordinate": "6,17",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63767,
                        "coordinate": "7,17",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63768,
                        "coordinate": "8,17",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63769,
                        "coordinate": "9,17",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63770,
                        "coordinate": "10,17",
                        "terrain": "3",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63771,
                        "coordinate": "1,18",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63772,
                        "coordinate": "2,18",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63773,
                        "coordinate": "3,18",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63774,
                        "coordinate": "4,18",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63775,
                        "coordinate": "5,18",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63776,
                        "coordinate": "6,18",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63777,
                        "coordinate": "7,18",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63778,
                        "coordinate": "8,18",
                        "terrain": "6",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63779,
                        "coordinate": "9,18",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63780,
                        "coordinate": "10,18",
                        "terrain": "3",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63781,
                        "coordinate": "1,19",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63782,
                        "coordinate": "2,19",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63783,
                        "coordinate": "3,19",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63784,
                        "coordinate": "4,19",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63785,
                        "coordinate": "5,19",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63786,
                        "coordinate": "6,19",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63787,
                        "coordinate": "7,19",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63788,
                        "coordinate": "8,19",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63789,
                        "coordinate": "9,19",
                        "terrain": "4",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63790,
                        "coordinate": "10,19",
                        "terrain": "3",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63791,
                        "coordinate": "1,20",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63792,
                        "coordinate": "2,20",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63793,
                        "coordinate": "3,20",
                        "terrain": "6",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63794,
                        "coordinate": "4,20",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63795,
                        "coordinate": "5,20",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63796,
                        "coordinate": "6,20",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63797,
                        "coordinate": "7,20",
                        "terrain": "1",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63798,
                        "coordinate": "8,20",
                        "terrain": "4",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": null
                    },
                    {
                        "map_id": 63799,
                        "coordinate": "9,20",
                        "terrain": "3",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": "芽庄"
                    },
                    {
                        "map_id": 63800,
                        "coordinate": "10,20",
                        "terrain": "3",
                        "country_id": 0,
                        "zone_id": 1,
                        "weather": "0",
                        "mark": "富吉"
                    }
                ],
                "rows": 10,
                "cols": 20
            }
        ],
        "scenario": {
            "id": 1,
            "scenario_id": 1,
            "name": "想定地图一",
            "season_list": [
                {
                    "scenario_id": 1,
                    "season_name": "天气设置时节",
                    "season_id": 10101,
                    "times": 30
                },
                {
                    "scenario_id": 1,
                    "season_name": "兵力调整时节",
                    "season_id": 10201,
                    "times": 40
                },
                {
                    "scenario_id": 1,
                    "season_name": "参战状态变更时节",
                    "season_id": 10301,
                    "times": 30
                },
                {
                    "scenario_id": 1,
                    "season_name": "派兵时节",
                    "season_id": 20101,
                    "times": 15
                },
                {
                    "scenario_id": 1,
                    "season_name": "初始位置调整时节",
                    "season_id": 20102,
                    "times": 30
                },
                {
                    "scenario_id": 1,
                    "season_name": "情报支援时节",
                    "season_id": 30101,
                    "times": 15
                },
                {
                    "scenario_id": 1,
                    "season_name": "航空任务分派时节",
                    "season_id": 40301,
                    "times": 60
                },
                {
                    "scenario_id": 1,
                    "season_name": "截击时节",
                    "season_id": 40401,
                    "times": 30
                },
                {
                    "scenario_id": 1,
                    "season_name": "驱逐时节",
                    "season_id": 40501,
                    "times": 30
                },
                {
                    "scenario_id": 1,
                    "season_name": "布雷时节",
                    "season_id": 40601,
                    "times": 20
                },
                {
                    "scenario_id": 1,
                    "season_name": "侦察时节",
                    "season_id": 40701,
                    "times": 5
                },
                {
                    "scenario_id": 1,
                    "season_name": "预警指挥机部署时节",
                    "season_id": 40801,
                    "times": 30
                },
                {
                    "scenario_id": 1,
                    "season_name": "战斗空中巡逻部署时节",
                    "season_id": 40901,
                    "times": 30
                },
                {
                    "scenario_id": 1,
                    "season_name": "扫雷时节",
                    "season_id": 41001,
                    "times": 5
                },
                {
                    "scenario_id": 1,
                    "season_name": "岸基单位筹划时节",
                    "season_id": 50101,
                    "times": 40
                },
                {
                    "scenario_id": 1,
                    "season_name": "作战命令下达时节",
                    "season_id": 50201,
                    "times": 60
                },
                {
                    "scenario_id": 1,
                    "season_name": "编队调整时节",
                    "season_id": 50301,
                    "times": 50
                },
                {
                    "scenario_id": 1,
                    "season_name": "潜艇航行模式宣告时节",
                    "season_id": 50401,
                    "times": 30
                },
                {
                    "scenario_id": 1,
                    "season_name": "作战筹划时节",
                    "season_id": 50501,
                    "times": 180
                },
                {
                    "scenario_id": 1,
                    "season_name": "行动裁决时节",
                    "season_id": 60101,
                    "times": 40
                },
                {
                    "scenario_id": 1,
                    "season_name": "岸基单位行动裁决时节",
                    "season_id": 60201,
                    "times": 20
                },
                {
                    "scenario_id": 1,
                    "season_name": "裁决结果",
                    "season_id": 60301,
                    "times": 15
                },
                {
                    "scenario_id": 1,
                    "season_name": "飞机返航时节",
                    "season_id": 70101,
                    "times": 20
                },
                {
                    "scenario_id": 1,
                    "season_name": "修复补给时节",
                    "season_id": 70201,
                    "times": 5
                },
                {
                    "scenario_id": 1,
                    "season_name": "推演分数",
                    "season_id": 70301,
                    "times": 10
                }
            ],
            "camps": [
                {
                    "camp": "1",
                    "name": "红方"
                },
                {
                    "camp": "2",
                    "name": "蓝方"
                }
            ],
            "zones": [
                {
                    "id": 1,
                    "center": "5,10",
                    "centre_point": "1",
                    "name": "区域1"
                }
            ],
            "countries": [
                {
                    "id": 1,
                    "name": "中国",
                    "code": "China",
                    "camp": "1"
                },
                {
                    "id": 2,
                    "name": "日本",
                    "code": "Japan",
                    "camp": "2"
                },
                {
                    "id": 5,
                    "name": "台湾",
                    "code": "Taiwan",
                    "camp": "2"
                }
            ],
            "seats": [
                {
                    "id": 14968,
                    "country_id": 1,
                    "seat_id": 101,
                    "seat_name": "飞机+水面编队指挥员"
                },
                {
                    "id": 14987,
                    "country_id": 1,
                    "seat_id": 102,
                    "seat_name": "岸基+潜艇指挥员"
                },
                {
                    "id": 14993,
                    "country_id": 2,
                    "seat_id": 201,
                    "seat_name": "日本编队指挥员"
                },
                {
                    "id": 15011,
                    "country_id": 5,
                    "seat_id": 501,
                    "seat_name": "美国编队指挥员"
                }
            ],
            "operators": [
                {
                    "id": 14968,
                    "operator_name": "ZDK-03",
                    "operator_id": 130101,
                    "category_id2": 301,
                    "country_id": 1,
                    "is_find": "1",
                    "seat_id": 101,
                    "position": "1,2",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/f0592860eff2d595ced43fb0ebfa70fd.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/1f539b7b956ce9257f0bdc8ea528e4d2.png;http://img.wgengine.bkw100.com/uploads/20190923/724f643dd94b9a2ac5700b995cdf696f.png",
                    "score": "2",
                    "category_ch_name": "预警机",
                    "category_en_name": "awacs",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "28,24"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "8,5"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "1"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "40,20"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "8"
                        },
                        {
                            "name": "反舰导弹多批攻击能力",
                            "attribute_name": "is_batch",
                            "attribute_value": "1"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "9,5"
                        },
                        {
                            "name": "是否具有超视距",
                            "attribute_name": "is_blos",
                            "attribute_value": "0"
                        },
                        {
                            "name": "超视距距离",
                            "attribute_name": "blos_range",
                            "attribute_value": "0"
                        },
                        {
                            "name": "作战能力",
                            "attribute_name": "combat_capability",
                            "attribute_value": "0"
                        },
                        {
                            "name": "等待回合",
                            "attribute_name": "wait_round",
                            "attribute_value": "0"
                        },
                        {
                            "name": "滞空时间",
                            "attribute_name": "retention_round",
                            "attribute_value": "1"
                        },
                        {
                            "name": "轰炸值",
                            "attribute_name": "bomb",
                            "attribute_value": "20,12"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "警戒范围",
                            "attribute_name": "warning_range",
                            "attribute_value": "0,0"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 14969,
                    "operator_name": "空警-2000",
                    "operator_id": 130102,
                    "category_id2": 301,
                    "country_id": 1,
                    "is_find": "1",
                    "seat_id": 101,
                    "position": "3,8",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/f0592860eff2d595ced43fb0ebfa70fd.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/1f539b7b956ce9257f0bdc8ea528e4d2.png;http://img.wgengine.bkw100.com/uploads/20190923/724f643dd94b9a2ac5700b995cdf696f.png",
                    "score": "3",
                    "category_ch_name": "预警机",
                    "category_en_name": "awacs",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "24,16"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "8,5"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "2"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "50,25"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "8"
                        },
                        {
                            "name": "反舰导弹多批攻击能力",
                            "attribute_name": "is_batch",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "27,13"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "2"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "1"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "24,16"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "7,3"
                        },
                        {
                            "name": "是否具有超视距",
                            "attribute_name": "is_blos",
                            "attribute_value": "0"
                        },
                        {
                            "name": "超视距距离",
                            "attribute_name": "blos_range",
                            "attribute_value": "0"
                        },
                        {
                            "name": "作战能力",
                            "attribute_name": "combat_capability",
                            "attribute_value": "0"
                        },
                        {
                            "name": "等待回合",
                            "attribute_name": "wait_round",
                            "attribute_value": "4"
                        },
                        {
                            "name": "滞空时间",
                            "attribute_name": "retention_round",
                            "attribute_value": "1"
                        },
                        {
                            "name": "轰炸值",
                            "attribute_name": "bomb",
                            "attribute_value": "20,12"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "警戒范围",
                            "attribute_name": "warning_range",
                            "attribute_value": "0,0"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 14970,
                    "operator_name": "空警-500",
                    "operator_id": 130201,
                    "category_id2": 302,
                    "country_id": 1,
                    "is_find": "1",
                    "seat_id": 101,
                    "position": "3,8",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/2212ec18ff5e15dff6d55ddd64e622b4.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/1d7e5c052ee86c0ade7523f051508fd8.png;http://img.wgengine.bkw100.com/uploads/20190923/ac169b04663a56bc44950f293648e59f.png",
                    "score": "1",
                    "category_ch_name": "预警指挥机",
                    "category_en_name": "early_warning_command_aircraft",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "38,34"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "8,5"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "30,15"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "8"
                        },
                        {
                            "name": "反舰导弹多批攻击能力",
                            "attribute_name": "is_batch",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "18,9"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "3"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "1"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "38,34"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "8,5"
                        },
                        {
                            "name": "是否具有超视距",
                            "attribute_name": "is_blos",
                            "attribute_value": "1"
                        },
                        {
                            "name": "超视距距离",
                            "attribute_name": "blos_range",
                            "attribute_value": "40"
                        },
                        {
                            "name": "作战能力",
                            "attribute_name": "combat_capability",
                            "attribute_value": "2"
                        },
                        {
                            "name": "等待回合",
                            "attribute_name": "wait_round",
                            "attribute_value": "0"
                        },
                        {
                            "name": "滞空时间",
                            "attribute_name": "retention_round",
                            "attribute_value": "2"
                        },
                        {
                            "name": "轰炸值",
                            "attribute_name": "bomb",
                            "attribute_value": "20,12"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "警戒范围",
                            "attribute_name": "warning_range",
                            "attribute_value": "4,4"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 14971,
                    "operator_name": "运-８",
                    "operator_id": 130202,
                    "category_id2": 302,
                    "country_id": 1,
                    "is_find": "1",
                    "seat_id": 101,
                    "position": "1,2",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/2212ec18ff5e15dff6d55ddd64e622b4.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/1d7e5c052ee86c0ade7523f051508fd8.png;http://img.wgengine.bkw100.com/uploads/20190923/ac169b04663a56bc44950f293648e59f.png",
                    "score": "2",
                    "category_ch_name": "预警指挥机",
                    "category_en_name": "early_warning_command_aircraft",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "38,34"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "8,5"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "29,14"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "10"
                        },
                        {
                            "name": "反舰导弹多批攻击能力",
                            "attribute_name": "is_batch",
                            "attribute_value": "1"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "14,7"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "1"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "38,34"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "9,5"
                        },
                        {
                            "name": "是否具有超视距",
                            "attribute_name": "is_blos",
                            "attribute_value": "0"
                        },
                        {
                            "name": "超视距距离",
                            "attribute_name": "blos_range",
                            "attribute_value": "0"
                        },
                        {
                            "name": "作战能力",
                            "attribute_name": "combat_capability",
                            "attribute_value": "0"
                        },
                        {
                            "name": "等待回合",
                            "attribute_name": "wait_round",
                            "attribute_value": "0"
                        },
                        {
                            "name": "滞空时间",
                            "attribute_name": "retention_round",
                            "attribute_value": "1"
                        },
                        {
                            "name": "轰炸值",
                            "attribute_name": "bomb",
                            "attribute_value": "20,12"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "警戒范围",
                            "attribute_name": "warning_range",
                            "attribute_value": "3,3"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 14972,
                    "operator_name": "JH-7",
                    "operator_id": 130301,
                    "category_id2": 303,
                    "country_id": 1,
                    "is_find": "1",
                    "seat_id": 101,
                    "position": "3,8",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/12b189242947ee5aa09ab6d71e491bff.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/8d44ff80b480364417a9a04c1e0dc0c0.png;http://img.wgengine.bkw100.com/uploads/20190923/9dc44d15a3947602edf761f0b94348eb.png",
                    "score": "1",
                    "category_ch_name": "攻击/歼轰机",
                    "category_en_name": "attack_fighter_bombers",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "42,30"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "8,5"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "2"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "27,13"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "10"
                        },
                        {
                            "name": "反舰导弹多批攻击能力",
                            "attribute_name": "is_batch",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "28,14"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "1"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "1"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "42,30"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "7,3"
                        },
                        {
                            "name": "是否具有超视距",
                            "attribute_name": "is_blos",
                            "attribute_value": "1"
                        },
                        {
                            "name": "超视距距离",
                            "attribute_name": "blos_range",
                            "attribute_value": "32"
                        },
                        {
                            "name": "作战能力",
                            "attribute_name": "combat_capability",
                            "attribute_value": "1"
                        },
                        {
                            "name": "等待回合",
                            "attribute_name": "wait_round",
                            "attribute_value": "2"
                        },
                        {
                            "name": "滞空时间",
                            "attribute_name": "retention_round",
                            "attribute_value": "1"
                        },
                        {
                            "name": "轰炸值",
                            "attribute_name": "bomb",
                            "attribute_value": "22,14"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "警戒范围",
                            "attribute_name": "warning_range",
                            "attribute_value": "0,0"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 14973,
                    "operator_name": "AT-3",
                    "operator_id": 130302,
                    "category_id2": 303,
                    "country_id": 1,
                    "is_find": "1",
                    "seat_id": 101,
                    "position": "3,8",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/12b189242947ee5aa09ab6d71e491bff.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/8d44ff80b480364417a9a04c1e0dc0c0.png;http://img.wgengine.bkw100.com/uploads/20190923/9dc44d15a3947602edf761f0b94348eb.png",
                    "score": "4",
                    "category_ch_name": "攻击/歼轰机",
                    "category_en_name": "attack_fighter_bombers",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "44,32"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "8,5"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "1"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "18,9"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "10"
                        },
                        {
                            "name": "反舰导弹多批攻击能力",
                            "attribute_name": "is_batch",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "9,5"
                        },
                        {
                            "name": "是否具有超视距",
                            "attribute_name": "is_blos",
                            "attribute_value": "0"
                        },
                        {
                            "name": "超视距距离",
                            "attribute_name": "blos_range",
                            "attribute_value": "0"
                        },
                        {
                            "name": "作战能力",
                            "attribute_name": "combat_capability",
                            "attribute_value": "0"
                        },
                        {
                            "name": "等待回合",
                            "attribute_name": "wait_round",
                            "attribute_value": "0"
                        },
                        {
                            "name": "滞空时间",
                            "attribute_name": "retention_round",
                            "attribute_value": "1"
                        },
                        {
                            "name": "轰炸值",
                            "attribute_name": "bomb",
                            "attribute_value": "24,16"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "警戒范围",
                            "attribute_name": "warning_range",
                            "attribute_value": "0,0"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 14974,
                    "operator_name": "轰-5",
                    "operator_id": 130401,
                    "category_id2": 304,
                    "country_id": 1,
                    "is_find": "1",
                    "seat_id": 101,
                    "position": "1,2",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/000bbb6edcc0b71fbba568e7461e3e9b.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/0af2436037f7804edf410e04400285fa.png;http://img.wgengine.bkw100.com/uploads/20190923/8bd51451d90034956a41f7ae42a96506.png",
                    "score": "3",
                    "category_ch_name": "轰炸机",
                    "category_en_name": "bomber",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "28,24"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "12,7"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "14,7"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "10"
                        },
                        {
                            "name": "反舰导弹多批攻击能力",
                            "attribute_name": "is_batch",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "6,4"
                        },
                        {
                            "name": "是否具有超视距",
                            "attribute_name": "is_blos",
                            "attribute_value": "1"
                        },
                        {
                            "name": "超视距距离",
                            "attribute_name": "blos_range",
                            "attribute_value": "50"
                        },
                        {
                            "name": "作战能力",
                            "attribute_name": "combat_capability",
                            "attribute_value": "3"
                        },
                        {
                            "name": "等待回合",
                            "attribute_name": "wait_round",
                            "attribute_value": "2"
                        },
                        {
                            "name": "滞空时间",
                            "attribute_name": "retention_round",
                            "attribute_value": "2"
                        },
                        {
                            "name": "轰炸值",
                            "attribute_name": "bomb",
                            "attribute_value": "34,24"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "警戒范围",
                            "attribute_name": "warning_range",
                            "attribute_value": "0,0"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 14975,
                    "operator_name": "轰-6k",
                    "operator_id": 130403,
                    "category_id2": 304,
                    "country_id": 1,
                    "is_find": "1",
                    "seat_id": 101,
                    "position": "1,2",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/000bbb6edcc0b71fbba568e7461e3e9b.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/0af2436037f7804edf410e04400285fa.png;http://img.wgengine.bkw100.com/uploads/20190923/8bd51451d90034956a41f7ae42a96506.png",
                    "score": "1",
                    "category_ch_name": "轰炸机",
                    "category_en_name": "bomber",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "24,12"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "12,7"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "28,14"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "10"
                        },
                        {
                            "name": "反舰导弹多批攻击能力",
                            "attribute_name": "is_batch",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "9,5"
                        },
                        {
                            "name": "是否具有超视距",
                            "attribute_name": "is_blos",
                            "attribute_value": "0"
                        },
                        {
                            "name": "超视距距离",
                            "attribute_name": "blos_range",
                            "attribute_value": "0"
                        },
                        {
                            "name": "作战能力",
                            "attribute_name": "combat_capability",
                            "attribute_value": "0"
                        },
                        {
                            "name": "等待回合",
                            "attribute_name": "wait_round",
                            "attribute_value": "0"
                        },
                        {
                            "name": "滞空时间",
                            "attribute_name": "retention_round",
                            "attribute_value": "1"
                        },
                        {
                            "name": "轰炸值",
                            "attribute_name": "bomb",
                            "attribute_value": "34,24"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "警戒范围",
                            "attribute_name": "warning_range",
                            "attribute_value": "0,0"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 14976,
                    "operator_name": "图154MD",
                    "operator_id": 130501,
                    "category_id2": 305,
                    "country_id": 1,
                    "is_find": "1",
                    "seat_id": 101,
                    "position": "1,2",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/0925426ab8b69e62503bc52e5fc27157.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/3b0c8de8997ebf0acbfabb9b6a380ea4.png;http://img.wgengine.bkw100.com/uploads/20190923/721843fa105f4eca60d3266214d3b009.png",
                    "score": "2",
                    "category_ch_name": "电子战机",
                    "category_en_name": "electronic_fighter_aircraft",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "144,98"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "6,4"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "28,18"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "10"
                        },
                        {
                            "name": "反舰导弹多批攻击能力",
                            "attribute_name": "is_batch",
                            "attribute_value": "1"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "7,3"
                        },
                        {
                            "name": "是否具有超视距",
                            "attribute_name": "is_blos",
                            "attribute_value": "0"
                        },
                        {
                            "name": "超视距距离",
                            "attribute_name": "blos_range",
                            "attribute_value": "0"
                        },
                        {
                            "name": "作战能力",
                            "attribute_name": "combat_capability",
                            "attribute_value": "3"
                        },
                        {
                            "name": "等待回合",
                            "attribute_name": "wait_round",
                            "attribute_value": "0"
                        },
                        {
                            "name": "滞空时间",
                            "attribute_name": "retention_round",
                            "attribute_value": "2"
                        },
                        {
                            "name": "轰炸值",
                            "attribute_name": "bomb",
                            "attribute_value": "12,10"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "警戒范围",
                            "attribute_name": "warning_range",
                            "attribute_value": "0,0"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 14977,
                    "operator_name": "T-CH-1",
                    "operator_id": 130701,
                    "category_id2": 307,
                    "country_id": 1,
                    "is_find": "1",
                    "seat_id": 101,
                    "position": "1,2",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/101b70be521806d986d76b8cb6839dfd.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/1d7e5c052ee86c0ade7523f051508fd8.png;http://img.wgengine.bkw100.com/uploads/20190923/86e6c25ad9e306fb6f38968d9ea78fdb.png",
                    "score": "2",
                    "category_ch_name": "侦察机",
                    "category_en_name": "reconnaissance_aircraft",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "64,50"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "6,4"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "3"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "29,14"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "10"
                        },
                        {
                            "name": "反舰导弹多批攻击能力",
                            "attribute_name": "is_batch",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "8,5"
                        },
                        {
                            "name": "是否具有超视距",
                            "attribute_name": "is_blos",
                            "attribute_value": "1"
                        },
                        {
                            "name": "超视距距离",
                            "attribute_name": "blos_range",
                            "attribute_value": "34"
                        },
                        {
                            "name": "作战能力",
                            "attribute_name": "combat_capability",
                            "attribute_value": "0"
                        },
                        {
                            "name": "等待回合",
                            "attribute_name": "wait_round",
                            "attribute_value": "5"
                        },
                        {
                            "name": "滞空时间",
                            "attribute_name": "retention_round",
                            "attribute_value": "1"
                        },
                        {
                            "name": "轰炸值",
                            "attribute_name": "bomb",
                            "attribute_value": "10,6"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "警戒范围",
                            "attribute_name": "warning_range",
                            "attribute_value": "0,0"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 14978,
                    "operator_name": "歼侦-6",
                    "operator_id": 130702,
                    "category_id2": 307,
                    "country_id": 1,
                    "is_find": "1",
                    "seat_id": 101,
                    "position": "1,2",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/101b70be521806d986d76b8cb6839dfd.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/1d7e5c052ee86c0ade7523f051508fd8.png;http://img.wgengine.bkw100.com/uploads/20190923/86e6c25ad9e306fb6f38968d9ea78fdb.png",
                    "score": "3",
                    "category_ch_name": "侦察机",
                    "category_en_name": "reconnaissance_aircraft",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "68,50"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "6,4"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "29,14"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "6"
                        },
                        {
                            "name": "反舰导弹多批攻击能力",
                            "attribute_name": "is_batch",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "9,5"
                        },
                        {
                            "name": "是否具有超视距",
                            "attribute_name": "is_blos",
                            "attribute_value": "0"
                        },
                        {
                            "name": "超视距距离",
                            "attribute_name": "blos_range",
                            "attribute_value": "0"
                        },
                        {
                            "name": "作战能力",
                            "attribute_name": "combat_capability",
                            "attribute_value": "0"
                        },
                        {
                            "name": "等待回合",
                            "attribute_name": "wait_round",
                            "attribute_value": "0"
                        },
                        {
                            "name": "滞空时间",
                            "attribute_name": "retention_round",
                            "attribute_value": "1"
                        },
                        {
                            "name": "轰炸值",
                            "attribute_name": "bomb",
                            "attribute_value": "10,6"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "警戒范围",
                            "attribute_name": "warning_range",
                            "attribute_value": "0,0"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 14979,
                    "operator_name": "中国机场1",
                    "operator_id": 150101,
                    "category_id2": 501,
                    "country_id": 1,
                    "is_find": "1",
                    "seat_id": 0,
                    "position": "1,2",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/3addc3b516212a2d1547b303d96de403.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/365903893a99217586fd551dc9783e92.png;http://img.wgengine.bkw100.com/uploads/20190923/5c8345c08e59111c3db706a1e569db5a.png",
                    "score": "7",
                    "category_ch_name": "机场",
                    "category_en_name": "airport",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        }
                    ],
                    "is_ground_building": 1,
                    "members": [
                        "130101",
                        "130102",
                        "130201",
                        "130202",
                        "130301",
                        "130302",
                        "130401",
                        "130403",
                        "130501",
                        "130701",
                        "130702"
                    ],
                    "is_formation": 0
                },
                {
                    "id": 14980,
                    "operator_name": "编队—1",
                    "operator_id": 160101,
                    "category_id2": 601,
                    "country_id": 1,
                    "is_find": "0",
                    "seat_id": 101,
                    "position": "3,7",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/6704fdd7e1d1a91de665df6856b76c91.png",
                    "model_image": "",
                    "score": "0",
                    "category_ch_name": "任务编组",
                    "category_en_name": "task_force",
                    "attributes": [
                        {
                            "name": "侦察范围",
                            "attribute_name": "scout_range",
                            "attribute_value": "5"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 1,
                    "members": [
                        "110402",
                        "110201"
                    ]
                },
                {
                    "id": 14981,
                    "operator_name": "昆明172",
                    "operator_id": 110201,
                    "category_id2": 102,
                    "country_id": 1,
                    "is_find": "0",
                    "seat_id": 101,
                    "position": "3,7",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/4221719efec80bb928f87adf6a82a6bd.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/6f7df25c834b2397f6cc50d73ea1df9c.png;http://img.wgengine.bkw100.com/uploads/20190923/f99f214f92b8e42cc893bd77fc72b253.png",
                    "score": "3",
                    "category_ch_name": "驱逐舰",
                    "category_en_name": "destroyer",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "30,15"
                        },
                        {
                            "name": "防御值",
                            "attribute_name": "defense",
                            "attribute_value": "12,6"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "25,12"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "3"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "20,10"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "15"
                        },
                        {
                            "name": "反舰导弹补给",
                            "attribute_name": "asm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "15,7"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "3"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "1"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "28,14"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "6,3"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "反潜弹药数量",
                            "attribute_name": "antisubmarine_num",
                            "attribute_value": "10"
                        },
                        {
                            "name": "反潜弹药补给能力",
                            "attribute_name": "is_antisubmarine_supply",
                            "attribute_value": "1"
                        },
                        {
                            "name": "近战/登陆值",
                            "attribute_name": "close_combat",
                            "attribute_value": "28,15"
                        },
                        {
                            "name": "近距防空值",
                            "attribute_name": "close_air_defense",
                            "attribute_value": "6,3"
                        },
                        {
                            "name": "区域防空值",
                            "attribute_name": "regional_air_defense",
                            "attribute_value": "20,10"
                        },
                        {
                            "name": "区域防空性质",
                            "attribute_name": "rad_nature",
                            "attribute_value": "2"
                        },
                        {
                            "name": "rad_num",
                            "attribute_name": "rad_num",
                            "attribute_value": "5"
                        },
                        {
                            "name": "区域防空导弹补给能力",
                            "attribute_name": "is_rad_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "是否携带直升机",
                            "attribute_name": "is_helicopter",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机载反舰导弹数量",
                            "attribute_name": "hasm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机载反舰导弹补给能力",
                            "attribute_name": "is_hasm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "炮弹数量",
                            "attribute_name": "shell_num",
                            "attribute_value": "50"
                        },
                        {
                            "name": "炮弹补给能力",
                            "attribute_name": "shell_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "052D"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "旅洋Ⅲ级"
                        },
                        {
                            "name": "侦察范围",
                            "attribute_name": "scout_range",
                            "attribute_value": "5"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 14982,
                    "operator_name": "海口171",
                    "operator_id": 110202,
                    "category_id2": 102,
                    "country_id": 1,
                    "is_find": "0",
                    "seat_id": 101,
                    "position": "3,7",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/4221719efec80bb928f87adf6a82a6bd.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/6f7df25c834b2397f6cc50d73ea1df9c.png;http://img.wgengine.bkw100.com/uploads/20190923/f99f214f92b8e42cc893bd77fc72b253.png",
                    "score": "4",
                    "category_ch_name": "驱逐舰",
                    "category_en_name": "destroyer",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "29,14"
                        },
                        {
                            "name": "防御值",
                            "attribute_name": "defense",
                            "attribute_value": "12,6"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "22,11"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "2"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "20,10"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "15"
                        },
                        {
                            "name": "反舰导弹补给",
                            "attribute_name": "asm_supply",
                            "attribute_value": "1"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "15,7"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "3"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "28,18"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "6,3"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "反潜弹药数量",
                            "attribute_name": "antisubmarine_num",
                            "attribute_value": "10"
                        },
                        {
                            "name": "反潜弹药补给能力",
                            "attribute_name": "is_antisubmarine_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "近战/登陆值",
                            "attribute_name": "close_combat",
                            "attribute_value": "28,15"
                        },
                        {
                            "name": "近距防空值",
                            "attribute_name": "close_air_defense",
                            "attribute_value": "6,3"
                        },
                        {
                            "name": "区域防空值",
                            "attribute_name": "regional_air_defense",
                            "attribute_value": "29,14"
                        },
                        {
                            "name": "区域防空性质",
                            "attribute_name": "rad_nature",
                            "attribute_value": "0"
                        },
                        {
                            "name": "rad_num",
                            "attribute_name": "rad_num",
                            "attribute_value": "5"
                        },
                        {
                            "name": "区域防空导弹补给能力",
                            "attribute_name": "is_rad_supply",
                            "attribute_value": "1"
                        },
                        {
                            "name": "是否携带直升机",
                            "attribute_name": "is_helicopter",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机载反舰导弹数量",
                            "attribute_name": "hasm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机载反舰导弹补给能力",
                            "attribute_name": "is_hasm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "炮弹数量",
                            "attribute_name": "shell_num",
                            "attribute_value": "32"
                        },
                        {
                            "name": "炮弹补给能力",
                            "attribute_name": "shell_supply",
                            "attribute_value": "1"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "052C"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "旅洋Ⅱ级"
                        },
                        {
                            "name": "侦察范围",
                            "attribute_name": "scout_range",
                            "attribute_value": "5"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 14983,
                    "operator_name": "三亚574",
                    "operator_id": 110401,
                    "category_id2": 104,
                    "country_id": 1,
                    "is_find": "0",
                    "seat_id": 101,
                    "position": "3,6",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/eb6a124fd1b7a9654436779950a24314.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/09d07c1acec6904ca53f9295ec939a8f.png;http://img.wgengine.bkw100.com/uploads/20190923/9df1b485fe71121abc790957fdf3d2b6.png",
                    "score": "2",
                    "category_ch_name": "护卫舰",
                    "category_en_name": "frigate",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "27,13"
                        },
                        {
                            "name": "防御值",
                            "attribute_name": "defense",
                            "attribute_value": "10,5"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "20,10"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "1"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "18,9"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "10"
                        },
                        {
                            "name": "反舰导弹补给",
                            "attribute_name": "asm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "6,3"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "反潜弹药数量",
                            "attribute_name": "antisubmarine_num",
                            "attribute_value": "8"
                        },
                        {
                            "name": "反潜弹药补给能力",
                            "attribute_name": "is_antisubmarine_supply",
                            "attribute_value": "1"
                        },
                        {
                            "name": "近战/登陆值",
                            "attribute_name": "close_combat",
                            "attribute_value": "22,11"
                        },
                        {
                            "name": "近距防空值",
                            "attribute_name": "close_air_defense",
                            "attribute_value": "8,4"
                        },
                        {
                            "name": "区域防空值",
                            "attribute_name": "regional_air_defense",
                            "attribute_value": "20,10"
                        },
                        {
                            "name": "区域防空性质",
                            "attribute_name": "rad_nature",
                            "attribute_value": "1"
                        },
                        {
                            "name": "rad_num",
                            "attribute_name": "rad_num",
                            "attribute_value": "10"
                        },
                        {
                            "name": "区域防空导弹补给能力",
                            "attribute_name": "is_rad_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "是否携带直升机",
                            "attribute_name": "is_helicopter",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机载反舰导弹数量",
                            "attribute_name": "hasm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机载反舰导弹补给能力",
                            "attribute_name": "is_hasm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "炮弹数量",
                            "attribute_name": "shell_num",
                            "attribute_value": "10"
                        },
                        {
                            "name": "炮弹补给能力",
                            "attribute_name": "shell_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "054A"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "江凯II级"
                        },
                        {
                            "name": "侦察范围",
                            "attribute_name": "scout_range",
                            "attribute_value": "5"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 14984,
                    "operator_name": "紫金山929",
                    "operator_id": 110302,
                    "category_id2": 103,
                    "country_id": 1,
                    "is_find": "0",
                    "seat_id": 101,
                    "position": "3,7",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/4346774c747aa86e9e7a4755ee5db96e.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/f6d8137f33a807becf6c81522839b044.png;http://img.wgengine.bkw100.com/uploads/20190923/eb8760cd53649038ee6f76a3c899cc11.png",
                    "score": "3",
                    "category_ch_name": "登陆舰",
                    "category_en_name": "landing_ship",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "14,7"
                        },
                        {
                            "name": "防御值",
                            "attribute_name": "defense",
                            "attribute_value": "6,3"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "14,7"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "14,7"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "5"
                        },
                        {
                            "name": "反舰导弹补给",
                            "attribute_name": "asm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "反潜弹药数量",
                            "attribute_name": "antisubmarine_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反潜弹药补给能力",
                            "attribute_name": "is_antisubmarine_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "近战/登陆值",
                            "attribute_name": "close_combat",
                            "attribute_value": "18,9"
                        },
                        {
                            "name": "近距防空值",
                            "attribute_name": "close_air_defense",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "区域防空值",
                            "attribute_name": "regional_air_defense",
                            "attribute_value": "30,15"
                        },
                        {
                            "name": "区域防空性质",
                            "attribute_name": "rad_nature",
                            "attribute_value": "0"
                        },
                        {
                            "name": "rad_num",
                            "attribute_name": "rad_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "区域防空导弹补给能力",
                            "attribute_name": "is_rad_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "是否携带直升机",
                            "attribute_name": "is_helicopter",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机载反舰导弹数量",
                            "attribute_name": "hasm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机载反舰导弹补给能力",
                            "attribute_name": "is_hasm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "炮弹数量",
                            "attribute_name": "shell_num",
                            "attribute_value": "24"
                        },
                        {
                            "name": "炮弹补给能力",
                            "attribute_name": "shell_supply",
                            "attribute_value": "1"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "072"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "玉康级"
                        },
                        {
                            "name": "侦察范围",
                            "attribute_name": "scout_range",
                            "attribute_value": "5"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 14985,
                    "operator_name": "惠州596",
                    "operator_id": 110402,
                    "category_id2": 104,
                    "country_id": 1,
                    "is_find": "0",
                    "seat_id": 101,
                    "position": "4,6",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/eb6a124fd1b7a9654436779950a24314.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/09d07c1acec6904ca53f9295ec939a8f.png;http://img.wgengine.bkw100.com/uploads/20190923/9df1b485fe71121abc790957fdf3d2b6.png",
                    "score": "4",
                    "category_ch_name": "护卫舰",
                    "category_en_name": "frigate",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "28,14"
                        },
                        {
                            "name": "防御值",
                            "attribute_name": "defense",
                            "attribute_value": "10,5"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "20,10"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "3"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "18,9"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "10"
                        },
                        {
                            "name": "反舰导弹补给",
                            "attribute_name": "asm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "6,3"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "反潜弹药数量",
                            "attribute_name": "antisubmarine_num",
                            "attribute_value": "8"
                        },
                        {
                            "name": "反潜弹药补给能力",
                            "attribute_name": "is_antisubmarine_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "近战/登陆值",
                            "attribute_name": "close_combat",
                            "attribute_value": "24,12"
                        },
                        {
                            "name": "近距防空值",
                            "attribute_name": "close_air_defense",
                            "attribute_value": "8,4"
                        },
                        {
                            "name": "区域防空值",
                            "attribute_name": "regional_air_defense",
                            "attribute_value": "16,7"
                        },
                        {
                            "name": "区域防空性质",
                            "attribute_name": "rad_nature",
                            "attribute_value": "3"
                        },
                        {
                            "name": "rad_num",
                            "attribute_name": "rad_num",
                            "attribute_value": "10"
                        },
                        {
                            "name": "区域防空导弹补给能力",
                            "attribute_name": "is_rad_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "是否携带直升机",
                            "attribute_name": "is_helicopter",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机载反舰导弹数量",
                            "attribute_name": "hasm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机载反舰导弹补给能力",
                            "attribute_name": "is_hasm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "炮弹数量",
                            "attribute_name": "shell_num",
                            "attribute_value": "8"
                        },
                        {
                            "name": "炮弹补给能力",
                            "attribute_name": "shell_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "056"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "江岛级"
                        },
                        {
                            "name": "侦察范围",
                            "attribute_name": "scout_range",
                            "attribute_value": "5"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 14986,
                    "operator_name": "辽宁号",
                    "operator_id": 110101,
                    "category_id2": 101,
                    "country_id": 1,
                    "is_find": "0",
                    "seat_id": 101,
                    "position": "3,8",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/712e1e3d7bf75c3c81844390dd6a48e8.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/6f7df25c834b2397f6cc50d73ea1df9c.png;http://img.wgengine.bkw100.com/uploads/20190923/f99f214f92b8e42cc893bd77fc72b253.png",
                    "score": "10",
                    "category_ch_name": "航空母舰",
                    "category_en_name": "aircraft_carrier",
                    "attributes": [
                        {
                            "name": "近战/登陆值",
                            "attribute_name": "close_combat",
                            "attribute_value": "28,14"
                        },
                        {
                            "name": "侦察范围",
                            "attribute_name": "scout_range",
                            "attribute_value": "5"
                        }
                    ],
                    "is_ground_building": 0,
                    "members": [
                        "130101",
                        "130102",
                        "130301",
                        "130302"
                    ],
                    "is_formation": 0
                },
                {
                    "id": 14987,
                    "operator_name": "094",
                    "operator_id": 120101,
                    "category_id2": 201,
                    "country_id": 1,
                    "is_find": "0",
                    "seat_id": 102,
                    "position": "6,6",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/24cd923c46732b9052b1eb8d646cde18.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/620151ab0d4f258a6ec1aad57633a24b.png;http://img.wgengine.bkw100.com/uploads/20190923/db1a5b7c782fda168a4eece1c45cf066.png",
                    "score": "5",
                    "category_ch_name": "核潜艇",
                    "category_en_name": "nuclear_powered_submarine",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "64,32"
                        },
                        {
                            "name": "防御值",
                            "attribute_name": "defense",
                            "attribute_value": "24,16"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "18,12"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "1"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "14,7"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "8"
                        },
                        {
                            "name": "反舰导弹补给",
                            "attribute_name": "asm_supply",
                            "attribute_value": "1"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "9,5"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "反潜弹药数量",
                            "attribute_name": "antisubmarine_num",
                            "attribute_value": "6"
                        },
                        {
                            "name": "反潜弹药补给能力",
                            "attribute_name": "is_antisubmarine_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "8,5"
                        },
                        {
                            "name": "鱼攻值",
                            "attribute_name": "torpedo_attack",
                            "attribute_value": "22,13"
                        },
                        {
                            "name": "鱼雷数量",
                            "attribute_name": "torpedo_num",
                            "attribute_value": "4"
                        },
                        {
                            "name": "鱼雷补给能力",
                            "attribute_name": "torpedo_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "侦察范围",
                            "attribute_name": "scout_range",
                            "attribute_value": "2"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 14988,
                    "operator_name": "043",
                    "operator_id": 120201,
                    "category_id2": 202,
                    "country_id": 1,
                    "is_find": "0",
                    "seat_id": 102,
                    "position": "6,7",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/a9447263fcc05e752778e9b53d70ff22.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/620151ab0d4f258a6ec1aad57633a24b.png;http://img.wgengine.bkw100.com/uploads/20190923/db1a5b7c782fda168a4eece1c45cf066.png",
                    "score": "7",
                    "category_ch_name": "常规潜艇",
                    "category_en_name": "conventional_submarine",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "28,14"
                        },
                        {
                            "name": "防御值",
                            "attribute_name": "defense",
                            "attribute_value": "16,7"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "12,7"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "10,6"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "6"
                        },
                        {
                            "name": "反舰导弹补给",
                            "attribute_name": "asm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "6,4"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "反潜弹药数量",
                            "attribute_name": "antisubmarine_num",
                            "attribute_value": "5"
                        },
                        {
                            "name": "反潜弹药补给能力",
                            "attribute_name": "is_antisubmarine_supply",
                            "attribute_value": "1"
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "3,2"
                        },
                        {
                            "name": "鱼攻值",
                            "attribute_name": "torpedo_attack",
                            "attribute_value": "20,12"
                        },
                        {
                            "name": "鱼雷数量",
                            "attribute_name": "torpedo_num",
                            "attribute_value": "3"
                        },
                        {
                            "name": "鱼雷补给能力",
                            "attribute_name": "torpedo_supply",
                            "attribute_value": "1"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "侦察范围",
                            "attribute_name": "scout_range",
                            "attribute_value": "2"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 14989,
                    "operator_name": "035",
                    "operator_id": 120202,
                    "category_id2": 202,
                    "country_id": 1,
                    "is_find": "0",
                    "seat_id": 102,
                    "position": "7,6",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/a9447263fcc05e752778e9b53d70ff22.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/620151ab0d4f258a6ec1aad57633a24b.png;http://img.wgengine.bkw100.com/uploads/20190923/db1a5b7c782fda168a4eece1c45cf066.png",
                    "score": "6",
                    "category_ch_name": "常规潜艇",
                    "category_en_name": "conventional_submarine",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "28,14"
                        },
                        {
                            "name": "防御值",
                            "attribute_name": "defense",
                            "attribute_value": "16,7"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "12,7"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "10,6"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "6"
                        },
                        {
                            "name": "反舰导弹补给",
                            "attribute_name": "asm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "6,4"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "反潜弹药数量",
                            "attribute_name": "antisubmarine_num",
                            "attribute_value": "5"
                        },
                        {
                            "name": "反潜弹药补给能力",
                            "attribute_name": "is_antisubmarine_supply",
                            "attribute_value": "1"
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "3,2"
                        },
                        {
                            "name": "鱼攻值",
                            "attribute_name": "torpedo_attack",
                            "attribute_value": "20,12"
                        },
                        {
                            "name": "鱼雷数量",
                            "attribute_name": "torpedo_num",
                            "attribute_value": "3"
                        },
                        {
                            "name": "鱼雷补给能力",
                            "attribute_name": "torpedo_supply",
                            "attribute_value": "1"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "分值",
                            "attribute_name": "score",
                            "attribute_value": "7"
                        },
                        {
                            "name": "侦查范围",
                            "attribute_name": "scout_range",
                            "attribute_value": "2"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 14990,
                    "operator_name": "AR-5",
                    "operator_id": 140201,
                    "category_id2": 402,
                    "country_id": 1,
                    "is_find": "1",
                    "seat_id": 102,
                    "position": "2,1",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/7b6ed47a15836098ce479b43acb9d0d3.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/9e319c47a9c6ec07122be6a17d0c780a.png;http://img.wgengine.bkw100.com/uploads/20190923/503782e78dd5534a4a801bb0237dba17.png",
                    "score": "5",
                    "category_ch_name": "弹道导弹",
                    "category_en_name": "ballistic_missile",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "8,6"
                        },
                        {
                            "name": "防御值",
                            "attribute_name": "defense",
                            "attribute_value": "3,3"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反舰导弹补给",
                            "attribute_name": "asm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "10,6"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "7"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "18,10"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "12,6"
                        },
                        {
                            "name": "是否具有反导能力",
                            "attribute_name": "is_anti_missile",
                            "attribute_value": "0"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "侦察范围",
                            "attribute_name": "scout_range",
                            "attribute_value": "1"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 14991,
                    "operator_name": "红鸟",
                    "operator_id": 140301,
                    "category_id2": 403,
                    "country_id": 1,
                    "is_find": "1",
                    "seat_id": 102,
                    "position": "3,1",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/b79231dd604c89e86b89ebf716bc5db2.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/9e319c47a9c6ec07122be6a17d0c780a.png;http://img.wgengine.bkw100.com/uploads/20190923/503782e78dd5534a4a801bb0237dba17.png",
                    "score": "4",
                    "category_ch_name": "巡航导弹",
                    "category_en_name": "cruise_missile",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "6,3"
                        },
                        {
                            "name": "防御值",
                            "attribute_name": "defense",
                            "attribute_value": "4,4"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反舰导弹补给",
                            "attribute_name": "asm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "20,10"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "10"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "30,15"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "10,5"
                        },
                        {
                            "name": "是否具有反导能力",
                            "attribute_name": "is_anti_missile",
                            "attribute_value": "1"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "侦察范围",
                            "attribute_name": "scout_range",
                            "attribute_value": "1"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 14992,
                    "operator_name": "AR-6",
                    "operator_id": 140202,
                    "category_id2": 402,
                    "country_id": 1,
                    "is_find": "1",
                    "seat_id": 102,
                    "position": "4,1",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/7b6ed47a15836098ce479b43acb9d0d3.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/9e319c47a9c6ec07122be6a17d0c780a.png;http://img.wgengine.bkw100.com/uploads/20190923/503782e78dd5534a4a801bb0237dba17.png",
                    "score": "4",
                    "category_ch_name": "弹道导弹",
                    "category_en_name": "ballistic_missile",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "8,6"
                        },
                        {
                            "name": "防御值",
                            "attribute_name": "defense",
                            "attribute_value": "3,3"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反舰导弹补给",
                            "attribute_name": "asm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "10,6"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "7"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "18,10"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "12,6"
                        },
                        {
                            "name": "是否具有反导能力",
                            "attribute_name": "is_anti_missile",
                            "attribute_value": "0"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "分值",
                            "attribute_name": "score",
                            "attribute_value": "5"
                        },
                        {
                            "name": "侦查范围",
                            "attribute_name": "scout_range",
                            "attribute_value": "1"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 14993,
                    "operator_name": "E-3B",
                    "operator_id": 230101,
                    "category_id2": 301,
                    "country_id": 2,
                    "is_find": "1",
                    "seat_id": 201,
                    "position": "10,20",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/8c3668ebadafac63cbd5e270dd114279.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/f7fffc2534c7f7e00d7aad75b985b34c.png;http://img.wgengine.bkw100.com/uploads/20190923/91a723d54281b1eab598b7c9efbba1af.png",
                    "score": "3",
                    "category_ch_name": "预警机",
                    "category_en_name": "awacs",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "28,18"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "10,8"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "25,12"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "12"
                        },
                        {
                            "name": "反舰导弹多批攻击能力",
                            "attribute_name": "is_batch",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "10,5"
                        },
                        {
                            "name": "是否具有超视距",
                            "attribute_name": "is_blos",
                            "attribute_value": "0"
                        },
                        {
                            "name": "超视距距离",
                            "attribute_name": "blos_range",
                            "attribute_value": "0"
                        },
                        {
                            "name": "作战能力",
                            "attribute_name": "combat_capability",
                            "attribute_value": "0"
                        },
                        {
                            "name": "等待回合",
                            "attribute_name": "wait_round",
                            "attribute_value": "0"
                        },
                        {
                            "name": "滞空时间",
                            "attribute_name": "retention_round",
                            "attribute_value": "1"
                        },
                        {
                            "name": "轰炸值",
                            "attribute_name": "bomb",
                            "attribute_value": "8,4"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "警戒范围",
                            "attribute_name": "warning_range",
                            "attribute_value": "0,0"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 14994,
                    "operator_name": "E-2C",
                    "operator_id": 230102,
                    "category_id2": 301,
                    "country_id": 2,
                    "is_find": "1",
                    "seat_id": 201,
                    "position": "10,20",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/8c3668ebadafac63cbd5e270dd114279.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/f7fffc2534c7f7e00d7aad75b985b34c.png;http://img.wgengine.bkw100.com/uploads/20190923/91a723d54281b1eab598b7c9efbba1af.png",
                    "score": "3",
                    "category_ch_name": "预警机",
                    "category_en_name": "awacs",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "32,24"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "10,8"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "1"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "22,11"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "12"
                        },
                        {
                            "name": "反舰导弹多批攻击能力",
                            "attribute_name": "is_batch",
                            "attribute_value": "1"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "10,5"
                        },
                        {
                            "name": "是否具有超视距",
                            "attribute_name": "is_blos",
                            "attribute_value": "1"
                        },
                        {
                            "name": "超视距距离",
                            "attribute_name": "blos_range",
                            "attribute_value": "22"
                        },
                        {
                            "name": "作战能力",
                            "attribute_name": "combat_capability",
                            "attribute_value": "2"
                        },
                        {
                            "name": "等待回合",
                            "attribute_name": "wait_round",
                            "attribute_value": "5"
                        },
                        {
                            "name": "滞空时间",
                            "attribute_name": "retention_round",
                            "attribute_value": "2"
                        },
                        {
                            "name": "轰炸值",
                            "attribute_name": "bomb",
                            "attribute_value": "8,4"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "警戒范围",
                            "attribute_name": "warning_range",
                            "attribute_value": "0,0"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 14995,
                    "operator_name": "E-767",
                    "operator_id": 230201,
                    "category_id2": 302,
                    "country_id": 2,
                    "is_find": "1",
                    "seat_id": 201,
                    "position": "10,20",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/1b0d7ac00f45de98b6f2c79b4837a79a.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/c9a66e1fe3c301b9dae2aeb864bfe045.png;http://img.wgengine.bkw100.com/uploads/20190923/0c3fd969da7c7e506929019fbf03c8a7.png",
                    "score": "2",
                    "category_ch_name": "预警指挥机",
                    "category_en_name": "early_warning_command_aircraft",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "52,42"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "18,14"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "20,10"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "12"
                        },
                        {
                            "name": "反舰导弹多批攻击能力",
                            "attribute_name": "is_batch",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "20,10"
                        },
                        {
                            "name": "是否具有超视距",
                            "attribute_name": "is_blos",
                            "attribute_value": "0"
                        },
                        {
                            "name": "超视距距离",
                            "attribute_name": "blos_range",
                            "attribute_value": "0"
                        },
                        {
                            "name": "作战能力",
                            "attribute_name": "combat_capability",
                            "attribute_value": "1"
                        },
                        {
                            "name": "等待回合",
                            "attribute_name": "wait_round",
                            "attribute_value": "0"
                        },
                        {
                            "name": "滞空时间",
                            "attribute_name": "retention_round",
                            "attribute_value": "1"
                        },
                        {
                            "name": "轰炸值",
                            "attribute_name": "bomb",
                            "attribute_value": "10,6"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "警戒范围",
                            "attribute_name": "warning_range",
                            "attribute_value": "6,6"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 14996,
                    "operator_name": "神龙",
                    "operator_id": 230301,
                    "category_id2": 303,
                    "country_id": 2,
                    "is_find": "1",
                    "seat_id": 201,
                    "position": "10,20",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/0d4b7dfb693ab645f63e187cf81433fe.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/be7fdffba08b9362c59091dcf06b6bef.png;http://img.wgengine.bkw100.com/uploads/20190923/0be5d5f9d012d4104480c15d49df939e.png",
                    "score": "3",
                    "category_ch_name": "攻击/歼轰机",
                    "category_en_name": "attack_fighter_bombers",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "46,36"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "18,14"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "2"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "24,12"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "8"
                        },
                        {
                            "name": "反舰导弹多批攻击能力",
                            "attribute_name": "is_batch",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "20,10"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "6"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "1"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "48,32"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "6,3"
                        },
                        {
                            "name": "是否具有超视距",
                            "attribute_name": "is_blos",
                            "attribute_value": "0"
                        },
                        {
                            "name": "超视距距离",
                            "attribute_name": "blos_range",
                            "attribute_value": "0"
                        },
                        {
                            "name": "作战能力",
                            "attribute_name": "combat_capability",
                            "attribute_value": "0"
                        },
                        {
                            "name": "等待回合",
                            "attribute_name": "wait_round",
                            "attribute_value": "2"
                        },
                        {
                            "name": "滞空时间",
                            "attribute_name": "retention_round",
                            "attribute_value": "2"
                        },
                        {
                            "name": "轰炸值",
                            "attribute_name": "bomb",
                            "attribute_value": "20,12"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "警戒范围",
                            "attribute_name": "warning_range",
                            "attribute_value": "0,0"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 14997,
                    "operator_name": "Ki115",
                    "operator_id": 230302,
                    "category_id2": 303,
                    "country_id": 2,
                    "is_find": "1",
                    "seat_id": 201,
                    "position": "10,20",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/0d4b7dfb693ab645f63e187cf81433fe.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/be7fdffba08b9362c59091dcf06b6bef.png;http://img.wgengine.bkw100.com/uploads/20190923/0be5d5f9d012d4104480c15d49df939e.png",
                    "score": "1",
                    "category_ch_name": "攻击/歼轰机",
                    "category_en_name": "attack_fighter_bombers",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "44,34"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "18,14"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "2"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "14,7"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "8"
                        },
                        {
                            "name": "反舰导弹多批攻击能力",
                            "attribute_name": "is_batch",
                            "attribute_value": "1"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "6,3"
                        },
                        {
                            "name": "是否具有超视距",
                            "attribute_name": "is_blos",
                            "attribute_value": "1"
                        },
                        {
                            "name": "超视距距离",
                            "attribute_name": "blos_range",
                            "attribute_value": "38"
                        },
                        {
                            "name": "作战能力",
                            "attribute_name": "combat_capability",
                            "attribute_value": "2"
                        },
                        {
                            "name": "等待回合",
                            "attribute_name": "wait_round",
                            "attribute_value": "0"
                        },
                        {
                            "name": "滞空时间",
                            "attribute_name": "retention_round",
                            "attribute_value": "1"
                        },
                        {
                            "name": "轰炸值",
                            "attribute_name": "bomb",
                            "attribute_value": "20,12"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "警戒范围",
                            "attribute_name": "warning_range",
                            "attribute_value": "0,0"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 14998,
                    "operator_name": "P1Y银河",
                    "operator_id": 230401,
                    "category_id2": 304,
                    "country_id": 2,
                    "is_find": "1",
                    "seat_id": 201,
                    "position": "10,20",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/6924c0eae172fab7de4adaa05b840cb9.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/48072ca7cd417742e56b2d24d2a260df.png;http://img.wgengine.bkw100.com/uploads/20190923/645c51cfc2b816ed24fd14359b2ede31.png",
                    "score": "1",
                    "category_ch_name": "轰炸机",
                    "category_en_name": "bomber",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "25,32"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "12,7"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "3"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "20,10"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "10"
                        },
                        {
                            "name": "反舰导弹多批攻击能力",
                            "attribute_name": "is_batch",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "15,6"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "4"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "46,20"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "8,4"
                        },
                        {
                            "name": "是否具有超视距",
                            "attribute_name": "is_blos",
                            "attribute_value": "0"
                        },
                        {
                            "name": "超视距距离",
                            "attribute_name": "blos_range",
                            "attribute_value": "0"
                        },
                        {
                            "name": "作战能力",
                            "attribute_name": "combat_capability",
                            "attribute_value": "0"
                        },
                        {
                            "name": "等待回合",
                            "attribute_name": "wait_round",
                            "attribute_value": "0"
                        },
                        {
                            "name": "滞空时间",
                            "attribute_name": "retention_round",
                            "attribute_value": "2"
                        },
                        {
                            "name": "轰炸值",
                            "attribute_name": "bomb",
                            "attribute_value": "34,24"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "警戒范围",
                            "attribute_name": "warning_range",
                            "attribute_value": "0,0"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 14999,
                    "operator_name": "G10N富士山",
                    "operator_id": 230402,
                    "category_id2": 304,
                    "country_id": 2,
                    "is_find": "1",
                    "seat_id": 201,
                    "position": "10,20",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/6924c0eae172fab7de4adaa05b840cb9.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/48072ca7cd417742e56b2d24d2a260df.png;http://img.wgengine.bkw100.com/uploads/20190923/645c51cfc2b816ed24fd14359b2ede31.png",
                    "score": "3",
                    "category_ch_name": "轰炸机",
                    "category_en_name": "bomber",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "24,18"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "12,7"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "1"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "10,8"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "8"
                        },
                        {
                            "name": "反舰导弹多批攻击能力",
                            "attribute_name": "is_batch",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "8,4"
                        },
                        {
                            "name": "是否具有超视距",
                            "attribute_name": "is_blos",
                            "attribute_value": "1"
                        },
                        {
                            "name": "超视距距离",
                            "attribute_name": "blos_range",
                            "attribute_value": "0"
                        },
                        {
                            "name": "作战能力",
                            "attribute_name": "combat_capability",
                            "attribute_value": "0"
                        },
                        {
                            "name": "等待回合",
                            "attribute_name": "wait_round",
                            "attribute_value": "4"
                        },
                        {
                            "name": "滞空时间",
                            "attribute_name": "retention_round",
                            "attribute_value": "1"
                        },
                        {
                            "name": "轰炸值",
                            "attribute_name": "bomb",
                            "attribute_value": "34,24"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "警戒范围",
                            "attribute_name": "warning_range",
                            "attribute_value": "0,0"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 15000,
                    "operator_name": "J4M极电",
                    "operator_id": 230601,
                    "category_id2": 306,
                    "country_id": 2,
                    "is_find": "1",
                    "seat_id": 201,
                    "position": "10,20",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/eb5b6ff35496c64182d70991b5a01a40.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/c5e7852c14447f91f3678056375f4e26.png;http://img.wgengine.bkw100.com/uploads/20190923/503ea22d6085ff4c34dda2286bd5c3dc.png",
                    "score": "1",
                    "category_ch_name": "截/歼击机",
                    "category_en_name": "interceptor_fighter",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "48,32"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "12,7"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "10,8"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "10"
                        },
                        {
                            "name": "反舰导弹多批攻击能力",
                            "attribute_name": "is_batch",
                            "attribute_value": "1"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "9,5"
                        },
                        {
                            "name": "是否具有超视距",
                            "attribute_name": "is_blos",
                            "attribute_value": "0"
                        },
                        {
                            "name": "超视距距离",
                            "attribute_name": "blos_range",
                            "attribute_value": "0"
                        },
                        {
                            "name": "作战能力",
                            "attribute_name": "combat_capability",
                            "attribute_value": "3"
                        },
                        {
                            "name": "等待回合",
                            "attribute_name": "wait_round",
                            "attribute_value": "2"
                        },
                        {
                            "name": "滞空时间",
                            "attribute_name": "retention_round",
                            "attribute_value": "2"
                        },
                        {
                            "name": "轰炸值",
                            "attribute_name": "bomb",
                            "attribute_value": "32,20"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "警戒范围",
                            "attribute_name": "warning_range",
                            "attribute_value": "0,0"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 15001,
                    "operator_name": "JK1阵风",
                    "operator_id": 230602,
                    "category_id2": 306,
                    "country_id": 2,
                    "is_find": "1",
                    "seat_id": 201,
                    "position": "10,20",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/eb5b6ff35496c64182d70991b5a01a40.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/c5e7852c14447f91f3678056375f4e26.png;http://img.wgengine.bkw100.com/uploads/20190923/503ea22d6085ff4c34dda2286bd5c3dc.png",
                    "score": "2",
                    "category_ch_name": "截/歼击机",
                    "category_en_name": "interceptor_fighter",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "46,20"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "12,7"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "1"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "18,14"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "10"
                        },
                        {
                            "name": "反舰导弹多批攻击能力",
                            "attribute_name": "is_batch",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "7,3"
                        },
                        {
                            "name": "是否具有超视距",
                            "attribute_name": "is_blos",
                            "attribute_value": "1"
                        },
                        {
                            "name": "超视距距离",
                            "attribute_name": "blos_range",
                            "attribute_value": "42"
                        },
                        {
                            "name": "作战能力",
                            "attribute_name": "combat_capability",
                            "attribute_value": "0"
                        },
                        {
                            "name": "等待回合",
                            "attribute_name": "wait_round",
                            "attribute_value": "1"
                        },
                        {
                            "name": "滞空时间",
                            "attribute_name": "retention_round",
                            "attribute_value": "1"
                        },
                        {
                            "name": "轰炸值",
                            "attribute_name": "bomb",
                            "attribute_value": "32,20"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "警戒范围",
                            "attribute_name": "warning_range",
                            "attribute_value": "0,0"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 15002,
                    "operator_name": "RC-2",
                    "operator_id": 230701,
                    "category_id2": 307,
                    "country_id": 2,
                    "is_find": "1",
                    "seat_id": 201,
                    "position": "10,20",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/6273c425796dbb925f8901bfa151bb38.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/cd4a5108342a69d593edbb2e8fcf5d9d.png;http://img.wgengine.bkw100.com/uploads/20190923/8358c20e6203449cfc7ed0b52b378574.png",
                    "score": "4",
                    "category_ch_name": "侦察机",
                    "category_en_name": "reconnaissance_aircraft",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "22,12"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "6,4"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "18,14"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "10"
                        },
                        {
                            "name": "反舰导弹多批攻击能力",
                            "attribute_name": "is_batch",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "28,14"
                        },
                        {
                            "name": "是否具有超视距",
                            "attribute_name": "is_blos",
                            "attribute_value": "0"
                        },
                        {
                            "name": "超视距距离",
                            "attribute_name": "blos_range",
                            "attribute_value": "0"
                        },
                        {
                            "name": "作战能力",
                            "attribute_name": "combat_capability",
                            "attribute_value": "2"
                        },
                        {
                            "name": "等待回合",
                            "attribute_name": "wait_round",
                            "attribute_value": "0"
                        },
                        {
                            "name": "滞空时间",
                            "attribute_name": "retention_round",
                            "attribute_value": "1"
                        },
                        {
                            "name": "轰炸值",
                            "attribute_name": "bomb",
                            "attribute_value": "20,12"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "警戒范围",
                            "attribute_name": "warning_range",
                            "attribute_value": "0,0"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 15003,
                    "operator_name": "日本机场1",
                    "operator_id": 250102,
                    "category_id2": 501,
                    "country_id": 2,
                    "is_find": "1",
                    "seat_id": 0,
                    "position": "10,20",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/d9ec1e0086da0f33b4dd5d292f89cad7.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/365903893a99217586fd551dc9783e92.png;http://img.wgengine.bkw100.com/uploads/20190923/5c8345c08e59111c3db706a1e569db5a.png",
                    "score": "7",
                    "category_ch_name": "机场",
                    "category_en_name": "airport",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        }
                    ],
                    "is_ground_building": 1,
                    "members": [
                        "230101",
                        "230102",
                        "230201",
                        "230301",
                        "230302",
                        "230401",
                        "230402",
                        "230601",
                        "230602",
                        "230701"
                    ],
                    "is_formation": 0
                },
                {
                    "id": 15004,
                    "operator_name": "编队—1",
                    "operator_id": 260201,
                    "category_id2": 602,
                    "country_id": 2,
                    "is_find": "0",
                    "seat_id": 201,
                    "position": "7,17",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/e06f97d5a691c450955cc2b8950e3b4b.png",
                    "model_image": "",
                    "score": "0",
                    "category_ch_name": "特混编组",
                    "category_en_name": "task_grouping",
                    "attributes": [
                        {
                            "name": "侦察范围",
                            "attribute_name": "scout_range",
                            "attribute_value": "5"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 1,
                    "members": [
                        "210201",
                        "210202",
                        "210402"
                    ]
                },
                {
                    "id": 15005,
                    "operator_name": "村雨DDG101",
                    "operator_id": 210201,
                    "category_id2": 102,
                    "country_id": 2,
                    "is_find": "0",
                    "seat_id": 201,
                    "position": "7,17",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/0f37fe355bef337e499153b1ed139fb2.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/3046749d8a8439fdbf1eec4f90af222d.png;http://img.wgengine.bkw100.com/uploads/20190923/b1f687b95bbcbebedaf102717af9cd26.png",
                    "score": "5",
                    "category_ch_name": "驱逐舰",
                    "category_en_name": "destroyer",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "30,15"
                        },
                        {
                            "name": "防御值",
                            "attribute_name": "defense",
                            "attribute_value": "12,6"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "22,11"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "2"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "20,10"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "15"
                        },
                        {
                            "name": "反舰导弹补给",
                            "attribute_name": "asm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "6,3"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "反潜弹药数量",
                            "attribute_name": "antisubmarine_num",
                            "attribute_value": "10"
                        },
                        {
                            "name": "反潜弹药补给能力",
                            "attribute_name": "is_antisubmarine_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "近战/登陆值",
                            "attribute_name": "close_combat",
                            "attribute_value": "26,13"
                        },
                        {
                            "name": "近距防空值",
                            "attribute_name": "close_air_defense",
                            "attribute_value": "6,3"
                        },
                        {
                            "name": "区域防空值",
                            "attribute_name": "regional_air_defense",
                            "attribute_value": "29,14"
                        },
                        {
                            "name": "区域防空性质",
                            "attribute_name": "rad_nature",
                            "attribute_value": "1"
                        },
                        {
                            "name": "rad_num",
                            "attribute_name": "rad_num",
                            "attribute_value": "5"
                        },
                        {
                            "name": "区域防空导弹补给能力",
                            "attribute_name": "is_rad_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "是否携带直升机",
                            "attribute_name": "is_helicopter",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机载反舰导弹数量",
                            "attribute_name": "hasm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机载反舰导弹补给能力",
                            "attribute_name": "is_hasm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "炮弹数量",
                            "attribute_name": "shell_num",
                            "attribute_value": "28"
                        },
                        {
                            "name": "炮弹补给能力",
                            "attribute_name": "shell_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "村雨级"
                        },
                        {
                            "name": "侦察范围",
                            "attribute_name": "scout_range",
                            "attribute_value": "5"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 15006,
                    "operator_name": "高波DD110",
                    "operator_id": 210202,
                    "category_id2": 102,
                    "country_id": 2,
                    "is_find": "0",
                    "seat_id": 201,
                    "position": "7,17",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/0f37fe355bef337e499153b1ed139fb2.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/3046749d8a8439fdbf1eec4f90af222d.png;http://img.wgengine.bkw100.com/uploads/20190923/b1f687b95bbcbebedaf102717af9cd26.png",
                    "score": "4",
                    "category_ch_name": "驱逐舰",
                    "category_en_name": "destroyer",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "30,15"
                        },
                        {
                            "name": "防御值",
                            "attribute_name": "defense",
                            "attribute_value": "12,6"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "22,11"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "2"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "20,10"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "15"
                        },
                        {
                            "name": "反舰导弹补给",
                            "attribute_name": "asm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "10,8"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "4"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "1"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "30,15"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "6,3"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "反潜弹药数量",
                            "attribute_name": "antisubmarine_num",
                            "attribute_value": "10"
                        },
                        {
                            "name": "反潜弹药补给能力",
                            "attribute_name": "is_antisubmarine_supply",
                            "attribute_value": "1"
                        },
                        {
                            "name": "近战/登陆值",
                            "attribute_name": "close_combat",
                            "attribute_value": "26,13"
                        },
                        {
                            "name": "近距防空值",
                            "attribute_name": "close_air_defense",
                            "attribute_value": "6,3"
                        },
                        {
                            "name": "区域防空值",
                            "attribute_name": "regional_air_defense",
                            "attribute_value": "20,10"
                        },
                        {
                            "name": "区域防空性质",
                            "attribute_name": "rad_nature",
                            "attribute_value": "0"
                        },
                        {
                            "name": "rad_num",
                            "attribute_name": "rad_num",
                            "attribute_value": "5"
                        },
                        {
                            "name": "区域防空导弹补给能力",
                            "attribute_name": "is_rad_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "是否携带直升机",
                            "attribute_name": "is_helicopter",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机载反舰导弹数量",
                            "attribute_name": "hasm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机载反舰导弹补给能力",
                            "attribute_name": "is_hasm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "炮弹数量",
                            "attribute_name": "shell_num",
                            "attribute_value": "34"
                        },
                        {
                            "name": "炮弹补给能力",
                            "attribute_name": "shell_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "高波级"
                        },
                        {
                            "name": "侦察范围",
                            "attribute_name": "scout_range",
                            "attribute_value": "5"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 15007,
                    "operator_name": "熊代DE225",
                    "operator_id": 210401,
                    "category_id2": 104,
                    "country_id": 2,
                    "is_find": "0",
                    "seat_id": 201,
                    "position": "7,17",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/74ec4bd695926011a5fa59a28bd024c7.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190904/79441455bf399c42e251e6f32bc69172.png;http://img.wgengine.bkw100.com/uploads/20190923/a1d6fa94ee0bb84953986965a7a2540c.png",
                    "score": "2",
                    "category_ch_name": "护卫舰",
                    "category_en_name": "frigate",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "24,12"
                        },
                        {
                            "name": "防御值",
                            "attribute_name": "defense",
                            "attribute_value": "10,5"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "20,10"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "18,9"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "10"
                        },
                        {
                            "name": "反舰导弹补给",
                            "attribute_name": "asm_supply",
                            "attribute_value": "1"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "6,3"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "反潜弹药数量",
                            "attribute_name": "antisubmarine_num",
                            "attribute_value": "8"
                        },
                        {
                            "name": "反潜弹药补给能力",
                            "attribute_name": "is_antisubmarine_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "近战/登陆值",
                            "attribute_name": "close_combat",
                            "attribute_value": "24,12"
                        },
                        {
                            "name": "近距防空值",
                            "attribute_name": "close_air_defense",
                            "attribute_value": "8,4"
                        },
                        {
                            "name": "区域防空值",
                            "attribute_name": "regional_air_defense",
                            "attribute_value": "40,20"
                        },
                        {
                            "name": "区域防空性质",
                            "attribute_name": "rad_nature",
                            "attribute_value": "3"
                        },
                        {
                            "name": "rad_num",
                            "attribute_name": "rad_num",
                            "attribute_value": "10"
                        },
                        {
                            "name": "区域防空导弹补给能力",
                            "attribute_name": "is_rad_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "是否携带直升机",
                            "attribute_name": "is_helicopter",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机载反舰导弹数量",
                            "attribute_name": "hasm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机载反舰导弹补给能力",
                            "attribute_name": "is_hasm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "炮弹数量",
                            "attribute_name": "shell_num",
                            "attribute_value": "27"
                        },
                        {
                            "name": "炮弹补给能力",
                            "attribute_name": "shell_supply",
                            "attribute_value": "1"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "筑后级"
                        },
                        {
                            "name": "侦察范围",
                            "attribute_name": "scout_range",
                            "attribute_value": "5"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 15008,
                    "operator_name": "DDE228",
                    "operator_id": 210402,
                    "category_id2": 104,
                    "country_id": 2,
                    "is_find": "0",
                    "seat_id": 201,
                    "position": "6,17",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/74ec4bd695926011a5fa59a28bd024c7.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190904/79441455bf399c42e251e6f32bc69172.png;http://img.wgengine.bkw100.com/uploads/20190923/a1d6fa94ee0bb84953986965a7a2540c.png",
                    "score": "6",
                    "category_ch_name": "护卫舰",
                    "category_en_name": "frigate",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "24,12"
                        },
                        {
                            "name": "防御值",
                            "attribute_name": "defense",
                            "attribute_value": "10,5"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "20,10"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "18,9"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "10"
                        },
                        {
                            "name": "反舰导弹补给",
                            "attribute_name": "asm_supply",
                            "attribute_value": "1"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "6,3"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "反潜弹药数量",
                            "attribute_name": "antisubmarine_num",
                            "attribute_value": "8"
                        },
                        {
                            "name": "反潜弹药补给能力",
                            "attribute_name": "is_antisubmarine_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "近战/登陆值",
                            "attribute_name": "close_combat",
                            "attribute_value": "24,12"
                        },
                        {
                            "name": "近距防空值",
                            "attribute_name": "close_air_defense",
                            "attribute_value": "8,4"
                        },
                        {
                            "name": "区域防空值",
                            "attribute_name": "regional_air_defense",
                            "attribute_value": "40,20"
                        },
                        {
                            "name": "区域防空性质",
                            "attribute_name": "rad_nature",
                            "attribute_value": "3"
                        },
                        {
                            "name": "区域防空导弹数量",
                            "attribute_name": "rad_num",
                            "attribute_value": "10"
                        },
                        {
                            "name": "区域防空导弹补给能力",
                            "attribute_name": "is_rad_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "是否携带直升机",
                            "attribute_name": "is_helicopter",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机载反舰导弹数量",
                            "attribute_name": "hasm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机载反舰导弹补给能力",
                            "attribute_name": "is_hasm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "炮弹数量",
                            "attribute_name": "shell_num",
                            "attribute_value": "27"
                        },
                        {
                            "name": "炮弹补给能力",
                            "attribute_name": "shell_supply",
                            "attribute_value": "1"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "筑后级"
                        },
                        {
                            "name": "分值",
                            "attribute_name": "score",
                            "attribute_value": "2"
                        },
                        {
                            "name": "侦查范围",
                            "attribute_name": "scout_range",
                            "attribute_value": "5"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 15009,
                    "operator_name": "翔龙号",
                    "operator_id": 220101,
                    "category_id2": 201,
                    "country_id": 2,
                    "is_find": "0",
                    "seat_id": 201,
                    "position": "8,15",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/f9d02934e6bffb45d8cf8956abbc5fb8.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/8d62cb2274378a1724e183c47ecc6322.png;http://img.wgengine.bkw100.com/uploads/20190923/a289144f2fb8870ef970a13cee0a617e.png",
                    "score": "8",
                    "category_ch_name": "核潜艇",
                    "category_en_name": "nuclear_powered_submarine",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "18,10"
                        },
                        {
                            "name": "防御值",
                            "attribute_name": "defense",
                            "attribute_value": "12,4"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "10,8"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "16,8"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "6"
                        },
                        {
                            "name": "反舰导弹补给",
                            "attribute_name": "asm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "10,4"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "4"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "5,2"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "5,3"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "反潜弹药数量",
                            "attribute_name": "antisubmarine_num",
                            "attribute_value": "7"
                        },
                        {
                            "name": "反潜弹药补给能力",
                            "attribute_name": "is_antisubmarine_supply",
                            "attribute_value": "1"
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "8,5"
                        },
                        {
                            "name": "鱼攻值",
                            "attribute_name": "torpedo_attack",
                            "attribute_value": "25,13"
                        },
                        {
                            "name": "鱼雷数量",
                            "attribute_name": "torpedo_num",
                            "attribute_value": "8"
                        },
                        {
                            "name": "鱼雷补给能力",
                            "attribute_name": "torpedo_supply",
                            "attribute_value": "1"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "侦察范围",
                            "attribute_name": "scout_range",
                            "attribute_value": "2"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 15010,
                    "operator_name": "赤龙号",
                    "operator_id": 220201,
                    "category_id2": 202,
                    "country_id": 2,
                    "is_find": "0",
                    "seat_id": 201,
                    "position": "9,15",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/f5d0e81b91a02f9b26673225783846cd.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/8d62cb2274378a1724e183c47ecc6322.png;http://img.wgengine.bkw100.com/uploads/20190923/a289144f2fb8870ef970a13cee0a617e.png",
                    "score": "6",
                    "category_ch_name": "常规潜艇",
                    "category_en_name": "conventional_submarine",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "16,9"
                        },
                        {
                            "name": "防御值",
                            "attribute_name": "defense",
                            "attribute_value": "12,6"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "10,8"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "2"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "14,7"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "8"
                        },
                        {
                            "name": "反舰导弹补给",
                            "attribute_name": "asm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "8,3"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "4"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "6,3"
                        },
                        {
                            "name": "反潜值",
                            "attribute_name": "antisubmarine",
                            "attribute_value": "5,2"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "反潜弹药数量",
                            "attribute_name": "antisubmarine_num",
                            "attribute_value": "5"
                        },
                        {
                            "name": "反潜弹药补给能力",
                            "attribute_name": "is_antisubmarine_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "6,3"
                        },
                        {
                            "name": "鱼攻值",
                            "attribute_name": "torpedo_attack",
                            "attribute_value": "18,8"
                        },
                        {
                            "name": "鱼雷数量",
                            "attribute_name": "torpedo_num",
                            "attribute_value": "7"
                        },
                        {
                            "name": "鱼雷补给能力",
                            "attribute_name": "torpedo_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "侦察范围",
                            "attribute_name": "scout_range",
                            "attribute_value": "2"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 15011,
                    "operator_name": "ZSD",
                    "operator_id": 540301,
                    "category_id2": 403,
                    "country_id": 5,
                    "is_find": "1",
                    "seat_id": 501,
                    "position": "10,18",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/7b7d4415f8a486cf86fb53a90b1b42be.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/4cccd5cf29ef6c62bd909bc4c33c1f07.png;http://img.wgengine.bkw100.com/uploads/20190923/076da7267b27779eb0c5526c4e2d9282.png",
                    "score": "5",
                    "category_ch_name": "巡航导弹",
                    "category_en_name": "cruise_missile",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "防御值",
                            "attribute_name": "defense",
                            "attribute_value": "18,9"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反舰导弹补给",
                            "attribute_name": "asm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "30,15"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "12"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "1"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "40,20"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "10,5"
                        },
                        {
                            "name": "是否具有反导能力",
                            "attribute_name": "is_anti_missile",
                            "attribute_value": "1"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "侦察范围",
                            "attribute_name": "scout_range",
                            "attribute_value": "1"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 15012,
                    "operator_name": "ZSX",
                    "operator_id": 540201,
                    "category_id2": 402,
                    "country_id": 5,
                    "is_find": "1",
                    "seat_id": 501,
                    "position": "10,19",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/fca3499fe004dbb8eb278641c3b1a0b9.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/413f8477143fc06df646e2aba2724363.png;http://img.wgengine.bkw100.com/uploads/20190923/1d1318fbe039bf66a6652106cc14c3c7.png",
                    "score": "3",
                    "category_ch_name": "弹道导弹",
                    "category_en_name": "ballistic_missile",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "10,5"
                        },
                        {
                            "name": "防御值",
                            "attribute_name": "defense",
                            "attribute_value": "16,7"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反舰导弹补给",
                            "attribute_name": "asm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "16,8"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "7"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "18,10"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "8,6"
                        },
                        {
                            "name": "是否具有反导能力",
                            "attribute_name": "is_anti_missile",
                            "attribute_value": "1"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "侦察范围",
                            "attribute_name": "scout_range",
                            "attribute_value": "1"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                },
                {
                    "id": 15013,
                    "operator_name": "ZSA",
                    "operator_id": 540101,
                    "category_id2": 401,
                    "country_id": 5,
                    "is_find": "1",
                    "seat_id": 501,
                    "position": "10,17",
                    "army_image": "http://img.wgengine.bkw100.com/uploads/20190923/ebad74a8013656ee1d88dc357e524d71.png",
                    "model_image": "http://img.wgengine.bkw100.com/uploads/20190923/fe38538f2c15c8964f81789c85798e80.png;http://img.wgengine.bkw100.com/uploads/20190923/5df92086b2ebfe0937d9a249d23a7104.png",
                    "score": "4",
                    "category_ch_name": "岸舰导弹",
                    "category_en_name": "shore_to_ship_missile",
                    "attributes": [
                        {
                            "name": "状态",
                            "attribute_name": "state",
                            "attribute_value": "0"
                        },
                        {
                            "name": "机动值",
                            "attribute_name": "move",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "防御值",
                            "attribute_name": "defense",
                            "attribute_value": "20,10"
                        },
                        {
                            "name": "反舰导弹攻击值",
                            "attribute_name": "asm_attack",
                            "attribute_value": "14,7"
                        },
                        {
                            "name": "反舰导弹性质",
                            "attribute_name": "asm_nature",
                            "attribute_value": "0"
                        },
                        {
                            "name": "反舰导弹射程",
                            "attribute_name": "asm_range",
                            "attribute_value": "18,9"
                        },
                        {
                            "name": "反舰导弹数量",
                            "attribute_name": "asm_num",
                            "attribute_value": "7"
                        },
                        {
                            "name": "反舰导弹补给",
                            "attribute_name": "asm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹攻击值",
                            "attribute_name": "cm_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "巡航导弹数量",
                            "attribute_name": "cm_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹补给能力",
                            "attribute_name": "cm_supply",
                            "attribute_value": "0"
                        },
                        {
                            "name": "巡航导弹射程",
                            "attribute_name": "cm_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹攻击值",
                            "attribute_name": "ba_attack",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "弹道导弹数量",
                            "attribute_name": "ba_num",
                            "attribute_value": "0"
                        },
                        {
                            "name": "弹道导弹射程",
                            "attribute_name": "ba_range",
                            "attribute_value": "0,0"
                        },
                        {
                            "name": "反潜性质",
                            "attribute_name": "antisubmarine_nature",
                            "attribute_value": null
                        },
                        {
                            "name": "对空值",
                            "attribute_name": "to_air",
                            "attribute_value": "12,6"
                        },
                        {
                            "name": "是否具有反导能力",
                            "attribute_name": "is_anti_missile",
                            "attribute_value": "0"
                        },
                        {
                            "name": "北约代号",
                            "attribute_name": "nato_code",
                            "attribute_value": "A-1"
                        },
                        {
                            "name": "平台型号",
                            "attribute_name": "platform_type",
                            "attribute_value": "B-1"
                        },
                        {
                            "name": "侦察范围",
                            "attribute_name": "scout_range",
                            "attribute_value": "1"
                        }
                    ],
                    "is_ground_building": 0,
                    "is_formation": 0
                }
            ]
        }
    }
}
        
        '''
        input_json_object = json.loads(input)
        if "data" in input_json_object and "scenario" in input_json_object["data"]:
            scenario = Scenario.parse(input_json_object["data"]["scenario"])
            return scenario
            # print(scenario)
        else:
            print("http response is error")


if __name__ == "__main__":
    # s = Scenario._test()
    # print(s.seats)
    # for i in s.zones:
    #
    #     print(i.name)

    from utils import file_util
    json_file_name = "data/ai_create_room_data.txt"
    json_string = file_util.read_to_end(json_file_name)
    json_object = json.loads(json_string)
    scenario = Scenario.parse(json_object["data"]["scenario"])
    pass

