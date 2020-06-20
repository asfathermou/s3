# --coding:utf-8--


# @Author: 逸风
# @Time: 2019-12-18


from seat.seat import Seat

class BattleSeat(Seat):
    """
    战役指挥员的席位
    """
    def __init__(self, http_client, room):
        super(BattleSeat).__init__()
        self._room = room
        self._http_client = http_client
        self._scenario = None

    def set_scenario(self, scenario):
        """
        获取想定信息
        :param scenario: 想定信息
        :return:
        """
        self._scenario = scenario
        print(self._scenario)


    def sendNotDispatchTroops(self, not_dispatch_operator_ids=[]):
        """
        派兵时节接口
        将不出动的兵力算子发送给服务端，
        将不出动的算子从想定中移除
        :param remove_troops_dict: 不出动的算子字典
        :return:
        """
        result = self._http_client.http_post_send_troops(not_dispatch_operator_ids)

        return result

    def adjustingInitialPosition(self, operator_position_dict=None):
        """
        兵力初始位置调整接口
        :param operator_position_dict:  被调整的算子及位置字典
        :return:
        """
        result = self._http_client.http_post_adjusting_initial_position(operator_position_dict)

        return result

    def intelligence_support(self):
        """
        情报支援完成接口
        :return:
        """
        result = self._http_client.http_post_information_support_finish(self._room.room_id, self._room.camp_id)

        return result

    def aviationTaskInitialization(self):
        """
        航空作战阶段-获取航空任务部署初始化数据接口
        :return:
        """
        result = self._http_client.http_get_aviation_task_initialization()

        return result

    def aviationMissionDeployment(self, aviation_mission_deployment_data_list):
        """
        航空作战阶段-航空任务部署时节接口
        :param aviation_mission_deployment_data_dict: 航空任务部署数据字典
        :return:
        """
        # aviationMissionDict = [
        #     {"operator_id": 130403, "room_id": 145, "type": 201, "camp": 1, "seat": 101, "zone_id": 1,
        #      "rounds": 2, "flag": 701, "position": "8,13"},
        #     {"scenario_id": 1, "operator_id": 130404, "room_id": 145, "type": 201, "camp": 1, "seat": 101, "zone_id": 1,
        #      "rounds": 2, "flag": 701, "position": "8,13"}
        # ]
        # TODO 过滤is_find=0的算子
        for aviation_operator in aviation_mission_deployment_data_list:
            operator_info = self._get_operator(aviation_operator['operator_id'])
            # print(operator_info)
            aviation_operator['room_id'] = self._room.room_id
            aviation_operator['scenario_id'] = self._room.scenario_id
            aviation_operator['camp'] = operator_info["camp_id"]
            aviation_operator['seat'] = operator_info['seat']
            aviation_operator['position'] = operator_info['position']
            if str(aviation_operator['operator_id'])[1:4] == '701':
                aviation_operator['flag'] = 701
            else:
                aviation_operator['flag'] = 0
            aviation_operator['zone_id'] = 1
            aviation_operator['rounds'] = 1
        result = self._http_client.http_post_aviation_mission_deployment(aviation_mission_deployment_data_list)

        return result

    def _get_operator(self, operator_id):

        # operator = (operator_id for operator_id in self._scenario['scenario'])
        # print(operator_id)
        operator_info = {}
        for operator in self._scenario.operators:
            if operator.operator_id == operator_id:
                operator_info['camp_id'] = operator.get_camp_id()
                operator_info['seat'] = int(operator.seat_id)
                operator_info['is_find'] = int(operator.is_find)
                operator_info['position'] = ",".join([str(operator.position[0]), str(operator.position[1])])
        return operator_info


    def aviationVolleyExpulsion(self, attack_type, action_type, section_id, is_long_air, is_return, is_expel,
                                  operator_ids):
        """
        航空作战阶段-截击驱逐时节接口
        :param operator_ids: 算子ID列表
        :param attack_type: 类型:106:截击时节;107:驱逐时节
        :param action_type: 动作类型：1:远距离攻击;2=返航;3=驱逐
        :param section_id: 时节ID
        :param is_long_air: 动作类型：1:远距离攻击;2=返航;3=驱逐
        :param is_return: 是否返航：0:否;1:是
        :param is_expel: 是否驱逐：0:否;1:是
        :return:
        """
        #一下参数从SDK中自动获取
        scenario_id = self._room.scenario_id
        camp_id = self._room.camp_id
        seat_id = 10001
        room_id = self._room.room_id

        result = self._http_client.http_post_aviation_volley_expulsion(scenario_id, camp_id, seat_id, room_id, attack_type, action_type, section_id, is_long_air, is_return, is_expel, operator_ids)

        return result

    def aircraftBray(self, operator_dict):
        """
        飞机布雷接口
        :param room_id: 推演室ID
        :param camp_id: 阵营ID
        :param operator_dict: 算子字典数据{"operator_id": 230301,"position ": "1,1"}
        :return:
        """
        # 循环添加type和flag
        room_id = self._room.room_id
        camp_id = self._room.camp_id
        scenario_id = self._room.scenario_id
        # 循环添加type和flag
        # operatorDict = [{"operator_id": 130403, "position": "8,13"}, {"operator_id": 130404, "position": "8,13"}]
        for operator in operator_dict:
            operator['scenario_id'] = scenario_id
            operator['room_id'] = room_id
            operator['type'] = 201
            operator['camp'] = camp_id
            operator['seat'] = self._room.seat_id.split(',')[0] #self._room.seat_id
            operator['zone_id'] = 1
            operator['rounds'] = 2
            operator['flag'] = 701

        result = self._http_client.http_post_aircraft_bray(room_id, camp_id, operator_dict)

        return result

    def awacsDeployment(self, awacs_deployment_data_dict):
        """
        预警指挥机部署接口
        :param awacs_deployment_data_dict: 预警指挥机部署数据字典
        :return:
        """
        room_id = self._room.room_id
        camp_id = self._room.camp_id
        scenario_id = self._room.scenario_id
        # 循环添加type和flag
        # operatorDict = [{"operator_id": 130403, "position": "8,13"},{"operator_id": 130404, "position": "8,13"}]
        for operator in awacs_deployment_data_dict:
            operator['scenario_id'] = scenario_id
            operator['room_id'] = room_id
            operator['type'] = 202
            operator['camp'] = camp_id
            operator['seat'] = operator['seat_id']  #部署的席位ID，需要将席位ID传过来#self._room.seat_id
            operator['zone_id'] = 1
            operator['rounds'] = 2
            operator['flag'] = 701

        result = self._http_client.http_post_awacs_deployment(room_id, camp_id, awacs_deployment_data_dict)

        return result

    def airPatrol(self, air_patrol_data_dict):
        """
        战斗空中巡逻接口
        :param air_patrol_data_dict: 战斗空中巡逻接口数据字典
        :return:
        """
        room_id = self._room.room_id
        camp_id = self._room.camp_id
        scenario_id = self._room.scenario_id
        # operatorDict = [{"operator_id": 130403, "position": "8,13"},{"operator_id": 130404, "position": "8,13"}]
        for operator in air_patrol_data_dict:
            operator['scenario_id'] = scenario_id
            operator['room_id'] = room_id
            operator['type'] = 203
            operator['camp'] = camp_id
            operator['seat'] = operator['seat_id']
            operator['zone_id'] = 1
            operator['rounds'] = 2
            operator['flag'] = 701

        result = self._http_client.http_post_air_patrol(room_id, camp_id, air_patrol_data_dict)

        return result

    def shoreUnitActionPlan(self, action_plan_data_dict):
        """
        岸基单位行动计划接口
        :param action_plan_data_dict: 岸基单位行动计划数据字典
        :return:
        """
        # action_plan_data_dict = [{"operator_id": 240301,"type": 1,"target_id": 140202},{"operator_id": 240201,"type": 1,"target_id": 150101}]
        for operator in action_plan_data_dict:
            operator['room_id'] = self._room.room_id
            operator['camp_id'] = self._room.camp_id
            operator['rounds'] = 2

        result = self._http_client.http_post_shore_unit_action_plan(self._room.room_id, self._room.camp_id, action_plan_data_dict)

        return result

    def operationalOrdersIssued(self, command_data_dict):
        """
        作战命令下达接口
        :param command_data_dict: 下达的命令数据字典
        :return:
        """
        # command_data_dicts = {"seat": ['101', '102'], "main_target": ['230402', '230602'], "threaten_target": ['230301', '230302', '230601', '230602', '230701']}
        room_id = self._room.room_id
        camp_id = self._room.camp_id
        rounds = 1
        zone_id = 1
        if command_data_dict:
            command_data_dict['room_id'] = room_id
            command_data_dict['camp_id'] = camp_id
            command_data_dict['rounds'] = rounds
            command_data_dict['zone_id'] = zone_id
            command_data_dict['seat'] = ",".join(command_data_dict['seat'])
            command_data_dict['main_target'] = ",".join(command_data_dict['main_target'])
            command_data_dict['threaten_target'] = ",".join(command_data_dict['threaten_target'])


        result = self._http_client.http_post_operational_orders_issued(room_id, camp_id, rounds, zone_id, command_data_dict)

        return result


if __name__ == "__main__":
    pass


