# --coding:utf-8--


# @Author: 逸风
# @Time: 2019-12-20

import requests
import logging
import json
import time


class CSFhttpClient:
    def __init__(self, user, token, ipaddress, room, websocket):
        self._user = user
        self._token = token
        self._ipaddress = ipaddress
        self._room = room
        self._ws = websocket

        self._url = "http://" + self._ipaddress + "/api"
        # self._url = "http://" + self._ipaddress
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='tmp/test.log',
                            filemode='w')

    def http_post_anti_ship_missiles_target_select(self, round_id, attack_formation_id, attack_operator_ids,
                                                   target_formation_id, target_operator_ids):

        """
        反舰导弹目标选择
        :param round_id:    数值，回合id
        :param attack_formation_id: 数值，发起反舰导弹的编队id，非编队发起填-1
        :param attack_operator_ids: 列表，发起的operator_id列表
        :param target_formation_id: 数值，被攻击方的编队id
        :param target_operator_ids: 列表，被攻击方的operator_id列表
        :return:
        """
        data = {
            "room_id": self._room.room_id,
            "camp_id": self._room.camp_id,
            "round_id": round_id,
            "attack_formation_id": attack_formation_id,
            "attack_operator_ids": json.dumps(attack_operator_ids),
            "target_formation_id": target_formation_id,
            "target_operator_ids": json.dumps(target_operator_ids)
        }

        result = self._http_post(
            url="/ai/attack/anti_ship_missiles_target_select",
            data=data
        )

        if result is not None:
            if result['code'] == 1:
                return result['data']
            else:
                return result['code']
        else:
            return -2

    def http_pot_formation_finished(self, section_id, room_id, camp_id):
        """
        编队调整完成通知接口
        :param section_id:
        :param room_id:
        :param camp_id:
        :return:
        """
        if camp_id == 1:
            time.sleep(3)
        result = self._http_post(
            url="/ai/actionplan/formation_finished",
            data={"section_id": section_id, "room_id": room_id, "camp_id": camp_id}
        )

        if result is not None:
            if result['code'] == 1:
                return 0
            else:
                return result['code']
        else:
            return -1

    def http_post_ruling_finished(self, section_id):
        """
        裁决完成通知接口
        :param section_id:
        :param room_id:
        :param camp_id:
        :return:
        """
        if self._room.camp_id == 1:
            time.sleep(3)
        result = self._http_post(
            url="/ai/actionplan/ruling_finished",
            data={"section_id": section_id, "room_id": self._room.room_id, "camp_id": self._room.camp_id}
        )

        if result is not None:
            if result['code'] == 1:
                return 0
            else:
                return result['code']
        else:
            return -1

    def http_post_login(self, username, password):
        """
        登录授权
        :param username:
        :param password:
        :return:
        """
        login_data = {'account': username, 'password': password}

        result = self._http_post(
            url="/ai/user/login",
            data=login_data
        )

        if result is not None:
            if result['code'] == 1 :
                userInfo = result['data']['userinfo']
                self._user.user_id = userInfo['user_id']
                self._user.username = userInfo['username']
                self._user.nickname = userInfo['nickname']
                self._user.group_id = userInfo['group_id']
                self._user.group_name = userInfo['group_name']

                self._token.token = userInfo['token']
                self._token.expiretime = userInfo['expiretime']
                self._token.expires_in = userInfo['expires_in']

                json_data = {"type": "userInit", "user_id": self._user.user_id}
                self._ws.send_message(json.dumps(json_data))
                # 将登陆后的用户新发送给引擎
                return 0
            else:
                return result['code']
        else:
            return -2

    def  http_get_scenario_info(self):
        """
        获取想定信息
        :param scenario_id: 想定ID
        :param room_id: 推演室ID
        :return:
        """
        result = self._http_post(
            url="/ai/scenario/scenario_info",
            data={'scenario_id': self._room.scenario_id, 'room_id': self._room.room_id, 'type': 0, 'camp_id': self._room.camp_id}
        )

        if result is not None:
            if result['code'] == 1:
                scenario_json = result['data'] #json.loads(scenario_json_string)

                return scenario_json
            else:
                return result['code']
        else:
            return -2

    def http_post_battle_state(self, room_id, user_id):
        """
        战斗状态（待用）
        :param room_id:
        :param user_id:
        :return:
        """
        pass

    def http_post_join_room(self):
        """
        加入推演室
        :param room_id: 推演室ID
        :param seat_id: 席位ID
        :param camp_id: 阵营ID
        :return:
        """
        data = {"room_id": self._room.room_id, "type": self._room.camp_id, "camp_id": self._room.camp_id, "seat": self._room.seat_id, "user_id": self._user.user_id}
        result = self._http_post(
            url="/ai/room/join",
            data=data
        )
        if result['code'] == 1:
            json_data = {"type": "join_camp", "user_id": self._user.user_id, "room_id": self._room.room_id, "camp_id": self._room.camp_id}
            self._ws.send_message(json.dumps(json_data))
            return 0
        else:
            return result['code']

    def http_get_exit_room(self, room_id):
        """
        退出推演室
        :param room_id: 推演室ID
        :return:
        """
        result = self._http_get(
            url="/ai/room/exit_room",
            data={"room_id": room_id}
        )

        if result is not None:
            if result['code'] == 1:

                return 0
            else:
                return result['code']
        else:
            return -3

    def http_get_exit_seat(self, room_id, camp_id, seat_id):
        """
        退出席位
        :param room_id: 推演室ID
        :param camp_id: 阵营ID
        :param seat_id: 席位ID
        :return:
        """
        result = self._http_get(
            url="/ai/room/exit_seat",
            data={"room_id": room_id, "camp_id": camp_id, "seat_id": seat_id}
        )

        if result is not None:
            if result['code'] == 1:

                return 0
            else:
                return result['code']
        else:
            return -2

    def http_get_change_presenter(self, room_id, camp_id, country_id):
        """
        推演方变更
        :param room_id: 推演室ID
        :param camp_id: 阵营ID
        :param country_id: 国家ID
        :return:
        """
        result = self._http_post(
            url="/ai/room/change_deduction",
            data={"room_id": room_id, "camp_id": camp_id, "country_id": country_id}
        )

        if result is not None:
            if result['code'] == 1:

                return 0
            else:
                return result['code']
        else:
            return -2


    def http_post_send_troops(self, operator_ids=[]):
        """
        派兵时节，设置不参与本次推演的算子
        :param room_id: 推演室ID
        :param operator_ids: 不参与本次推演的算子列表
        :return:
        """
        result = self._http_post(
            url="/ai/preparationstage/sending_soldiers",
            data={"room_id": self._room.room_id, "camp_id": self._room.camp_id, "data": json.dumps(operator_ids)}
        )

        if result is not None:
            if result['code'] == 1:

                return 0
            else:
                return result['code']
        else:
            return -2

    def http_post_adjusting_initial_position(self, operator_position_dict=None):
        """
        兵力初始位置调整
        :param room_id: 推演室ID
        :param camp_id: 阵营ID
        :param operator_position_dict: 被调整的算子及位置字典
        :return:
        """
        data = {}
        data['room_id'] = self._room.room_id
        data['camp_id'] = self._room.camp_id
        data['data'] = json.dumps(operator_position_dict)

        result = self._http_post(
            url="/ai/preparationstage/operator_position",
            data=data
        )

        if result is not None:
            if result['code'] == 1:
                return 0
            else:
                return result['code']
        else:
            return -2

    def http_post_information_support_finish(self, room_id, camp_id):
        if camp_id == 1:
            time.sleep(3)
        result = self._http_post(
            url="/ai/intelligence/information_support_finish",
            data={"room_id": room_id, "camp_id": camp_id}
        )
        if result is not None:
            if result['code'] == 1:
                return 0
            else:
                return result['code']
        else:
            return -1

    def http_get_aviation_task_initialization(self):
        """
        航空任务初始化数据
        :param room_id:
        :param camp_id:
        :param scenario_id:
        :return:
        """

        result = self._http_post(
            url="/ai/aviation/aviation_info",
            data={"room_id": self._room.room_id, "camp": self._room.camp_id, "scenario_id": self._room.scenario_id}
        )

        if result is not None:
            if result['code'] == 1:
                return result['data']
            else:
                return result['code']
        else:
            return -1

    def http_post_aviation_mission_deployment(self, aviation_mission_deployment_data_dict):
        """
        航空任务部署
        :param aviation_mission_deployment_data_dict: 航空任务部署数据字典
        :return:
        """
        if self._room.camp_id == 1:
            time.sleep(3)
        data = {}
        data['room_id'] = self._room.room_id
        data['camp_id'] = self._room.camp_id
        data['operators'] = aviation_mission_deployment_data_dict
        result = self._http_post(
            url="/ai/aviation/aviation_setting",
            data={"data": json.dumps(data)}
        )

        if result is not None:
            if result['code'] == 1:
                return 0
            else:
                return result['code']
        else:
            return -4

    def http_post_aviation_volley_expulsion(self, scenario_id, camp_id, seat_id, room_id, type, action_type, section_id, is_long_air, is_return, is_expel,
                                  operator_ids):
        """
        航空作战阶段-截击驱逐时节接口
        :param operator_id: 算子ID列表
        :param type: 类型:106:截击时节;107:驱逐时节
        :param action_type: 动作类型：1:远距离攻击;2=返航;3=驱逐
        :param section_id: 时节ID
        :param is_long_air: 动作类型：1:远距离攻击;2=返航;3=驱逐
        :param is_return: 是否返航：0:否;1:是
        :param is_expel: 是否驱逐：0:否;1:是
        :return:
        """
        data = {}
        data['scenario_id'] = scenario_id
        data['camp'] = camp_id
        data['seat'] = seat_id
        data['room_id'] = room_id
        data['type'] = type
        data['action_type'] = action_type
        data['section_id'] = section_id
        data['is_long_air'] = is_long_air
        data['is_return'] = is_return
        data['is_expel'] = is_expel
        data['operator_id'] = ",".join(operator_ids) #将列表转换为字符串，用逗号隔开

        if self._room.camp_id == 1:
            time.sleep(3)

        result = self._http_post(
            url="/ai/aviation/aviation_volley_expel",
            data=data
        )

        if result is not None:
            if result['code'] == 1:
                return 0
            else:
                return result['code']
        else:
            return -2

    def http_post_aircraft_bray(self, room_id, camp_id, operator_dict):
        """
        飞机布雷接口
        :param room_id: 推演室ID
        :param camp_id: 阵营ID
        :param operator_dict: 算子字典数据{"operator_id": 230301,"position ": "1,1"}
        :return:
        """
        data = {}
        data['room_id'] = room_id
        data['camp_id'] = camp_id
        data['operators'] = operator_dict
        if camp_id == 1:
            time.sleep(3)

        result = self._http_post(
            url="/ai/aviation/aircraft_bray",
            data={"data": json.dumps(data)}
        )

        if result is not None:
            if result['code'] == 1:
                return 0
            else:
                return result['code']
        else:
            return -4

    def http_post_awacs_deployment(self, room_id, camp_id, awacs_deployment_data_dict):
        """
        预警指挥机部署接口
        :param room_id: 推演室ID
        :param camp_id: 阵营ID
        :param awacs_deployment_data_dict: 预警指挥机部署数据字典
        :return:
        """
        data = {}
        data['room_id'] = room_id
        data['camp_id'] = camp_id
        data['operators'] = awacs_deployment_data_dict
        if camp_id == 1:
            time.sleep(3)
        result = self._http_post(
            url="/ai/aviation/awacs_deployment",
            data={"data": json.dumps(data)}
        )

        if result is not None:
            if result['code'] == 1:
                return 0
            else:
                return result['code']
        else:
            return -4

    def http_post_air_patrol(self, room_id, camp_id, air_patrol_data_dict):
        """
        战斗空中巡逻接口
        :param room_id: 推演室ID
        :param camp_id: 阵营ID
        :param air_patrol_data_dict: 战斗空中巡逻接口数据字典
        :return:
        """
        data = {}
        data['room_id'] = room_id
        data['camp_id'] = camp_id
        data['operators'] = air_patrol_data_dict
        if camp_id == 1:
            time.sleep(3)
        result = self._http_post(
            url="/ai/aviation/air_patrol",
            data={"data": json.dumps(data)}
        )

        if result is not None:
            if result['code'] == 1:
                return 0
            else:
                return result['code']
        else:
            return -4

    def http_post_shore_unit_action_plan(self, room_id, camp_id, action_plan_data_dict):
        """
        岸基单位行动计划接口
        :param action_plan_data_dict: 岸基单位行动计划数据字典
        :return:
        """
        if camp_id == 1:
            time.sleep(3)
        result = self._http_post(
            url="/ai/actionplan/dark_base_missile",
            data={
                "room_id": room_id,
                "camp_id": camp_id,
                "data": json.dumps(action_plan_data_dict)
            }
        )

        if result is not None:
            if result['code'] == 1:
                return 0
            else:
                return result['code']
        else:
            return -2

    def http_post_operational_orders_issued(self, room_id, camp_id, rounds, zone_id, command_data_dict):
        """
        作战命令下达接口
        :param command_data_dict: 下达的命令数据字典
        :return:
        """
        data = {}
        data['room_id'] = room_id
        data['camp_id'] = camp_id
        data['rounds'] = rounds
        data['zone_id'] = zone_id
        data['data'] = json.dumps(command_data_dict)

        result = self._http_post(
            url="/ai/combatcommand/command",
            data=data
        )

        if result is not None:
            if result['code'] == 1:
                return 0
            else:
                return result['code']
        else:
            return -2

    def http_post_create_formation(self, formation_dict):
        """
        组件编队
        :param type:
        :param user_id:
        :param room_id:
        :param scenario_id:
        :param camp_id:
        :param country_id:
        :param rounds:
        :param seat_id:
        :param category_id:
        :param operator_ids:
        :param position:
        :param move:
        :return:
        """
        # data = {"type": type, "user_id": user_id, "room_id": room_id, "scenario_id": scenario_id, "camp_id": camp_id, "country_id": country_id, "rounds": rounds, "seat_id": seat_id, "category_id": category_id, "operator_ids": operator_ids, "position": position, "move": move}
        result = self._http_post(
            url="/ai/actionplan/formation",
            data=formation_dict
        )

        if result is not None:
            if result['code'] == 1:
                return 0
            else:
                return result['code']
        else:
            return -4

    def http_post_adjust_formation(self, adjust_formation_dict):
        """
        编队调整
        :param type:
        :param user_id:
        :param room_id:
        :param scenario_id:
        :param camp_id:
        :param adjust_formation_dict:
        :return:
        """
        # deleted_formation_ids = adjust_formation_dict['deleted_formation_ids']
        # changed_formations = adjust_formation_dict['changed_formations']
        #
        # data = {"type": type, "user_id": user_id, "room_id": room_id, "scenario_id": scenario_id, "camp_id": camp_id, "deleted_formation_ids": deleted_formation_ids, "changed_formations": changed_formations}
        result = self._http_post(
            url="/ai/actionplan/formation",
            data={"data": json.dumps(adjust_formation_dict)}
        )
        if result is not None:
            if result['code'] == 1:
                return 0
            else:
                return result['code']
        else:
            return -4

    def http_post_preset_formation_order(self, presetFormatioOrderDict):
        """
        预设编队顺序接口
        :param presetFormatioOrderDict: 调整信息字典
        :return:
        """
        result = self._http_post(
            url="/ai/actionplan/updateFormationOrder",
            data=presetFormatioOrderDict
        )
        if result is not None:
            if result['code'] == 1:
                return 0
            else:
                return result['code']
        else:
            return -4

    def http_post_transfer_command(self, transferFommandDict):
        """
        移交指挥权接口
        :param transferFommandDict: 移交算子信息字典
        :return:
        """
        result = self._http_post(
            url="/ai/actionplan/transfer_formation",
            data=transferFommandDict
        )

        if result is not None:
            if result['code'] == 1:
                return 0
            else:
                return result['code']
        else:
            return -2

    def http_post_disbanded_formations(self, disbandedFormationsDict):
        """
        解散编队
        :param disbandedFormationsDict: 被解散的编队信息字典
        :return:
        """
        result = self._http_post(
            url="/ai/actionplan/disband_formation",
            data=disbandedFormationsDict
        )

        if result is not None:
            if result['code'] == 1:
                return 0
            else:
                return result['code']
        else:
            return -1

    def http_post_submarine_voyage_mode(self, submarineVoyageModeDict):
        """
        潜艇航行模式宣告时节接口
        :param submarineVoyageModeDict: 潜艇航行数据字典
        :return:
        """
        data = {
            "room_id":submarineVoyageModeDict['room_id'],
            'camp_id': submarineVoyageModeDict['camp_id'],
            'operators': json.dumps(submarineVoyageModeDict['operators'])
        }

        if self._room.camp_id == 1:
            time.sleep(3)
        result = self._http_post(
            url="/ai/actionplan/submarine_voyage",
            data=data
        )

        if result is not None:
            if result['code'] == 1:
                return 0
            else:
                return result['code']
        else:
            return -2

    def http_post_change_presenter(self, room_id, camp_id, country_id):
        """
        推演方变更接口
        :param room_id: 推演室ID
        :param camp_id: 阵营ID
        :param country_id: 国家ID
        :return:
        """
        data = {"room_id": room_id, "camp_id": camp_id, "country_id": country_id}
        result = self._http_post(
            url="/ai/room/change_deduction",
            data=data
        )

        if result is not None:
            if result['code'] == 1:
                return 0
            else:
                return result['code']
        else:
            return -2

    def http_post_maneuvering_attack(self, maneuvering_attack_list):
        """
        作战筹划阶段-各种机动攻击数据接口
        鱼攻、反舰导弹、巡航导弹、弹道导弹、轰炸、反潜、近距等战斗类型攻击数据接口
        :param maneuvering_attack_dict:
        :return:
        """
        if self._room.camp_id == 1:
            time.sleep(3)
        print("接收到的数据")
        print(maneuvering_attack_list)
        if len(maneuvering_attack_list) > 0:
            maneuvering_attack_list = json.dumps(maneuvering_attack_list)
        else:
            maneuvering_attack_list = ""
        data = {
            "room_id": self._room.room_id,
            "camp_id": self._room.camp_id,
            "MargedActionData": maneuvering_attack_list
        }

        print("阵营" + str(self._room.camp_id) + ": 发送")
        print(data)
        result = self._http_post(
            url="/ai/attack/anti_ship_missile",
            data=data
        )

        if result is not None:
            if result['code'] == 1:
                return 0
            else:
                return result['code']
        else:
            return -3

    def http_post_aircraft_return(self, operator_id, position, section_id, return_type):
        """
        飞机返回数据接口
        :param operator_id:
        :param position:
        :param section_id:
        :param return_type:
        :return:
        """
        data = {"operator_id": operator_id, "position": position, "section_id": section_id, "return_type": return_type}

        result = self._http_post(
            url="/ai/service/airplane_return",
            data=data
        )

        if result is not None:
            if result['code'] == 1:
                return 0
            else:
                return result['code']
        else:
            return -2

    def http_post_user_to_engine(self, user_id, username):
        """
        将已登录用户发送给引擎
        :param user_id: 用户ID
        :param username: 用户名
        :return:
        """
        data = {"user_id": user_id, "username": username}
        result = self._http_post_engine(
            url="/ai_login",
            data=data
        )

        if result == "true":
            return 0
        else:
            return -1

    def http_post_awacs_command_check(self, operator_id, coordinate):
        """

        :param operator_id:
        :param coordinate:
        :return:
        """
        data = {}
        data['room_id'] = self._room.room_id
        data['camp_id'] = self._room.camp_id
        data['operator_id'] = operator_id
        data['position'] = coordinate

        result = self._http_post_engine(
            url="/ai/aviation/check",
            data=data
        )

        if result == "true":
            return 0
        else:
            return -1

    def http_post_attack_finished(self, section_id):
        """
        作战筹划完成接口
        :param section_id:
        :param room_id:
        :param camp_id:
        :return:
        """
        if self._room.camp_id == 1:
            time.sleep(3)
        result = self._http_post(
            url="/ai/attack/attack_finished",
            data={"section_id": section_id,"room_id": self._room.room_id, "camp_id": self._room.camp_id}
        )
        if result is not None:
            if result['code'] == 1:
                return 0
            else:
                return result['code']
        else:
            return -1

    def http_post_airplane_return(self, operator_id, position, section_id, return_type):
        """
        飞机返航完成接口
        :param operator_id: 算子ID
        :param position: 坐标
        :param section_id: 时节ID
        :param return_type: 返航类型：0=手动，1=自动
        :return:
        """
        if self._room.camp_id == 1:
            time.sleep(3)

        result = self._http_post(
            url="/ai/actionplan/airplane_return",
            data={
                "section_id": section_id,
                "room_id": self._room.room_id,
                "camp_id": self._room.camp_id,
                "operator_id": operator_id,
                "zone_id": 1,
                "position": position,
                "return_type": return_type
            }
        )
        if result is not None:
            if result['code'] == 1:
                return 0
            else:
                return result['code']
        else:
            return -1

    def http_post_airplane_return_finished(self, section_id):
        """
        飞机返航完成接口
        :param section_id:
        :param room_id:
        :param camp_id:
        :return:
        """
        if self._room.camp_id == 1:
            time.sleep(3)
        result = self._http_post(
            url="/ai/actionplan/airplane_return_finished",
            data={"section_id": section_id,"room_id": self._room.room_id, "camp_id": self._room.camp_id}
        )
        if result is not None:
            if result['code'] == 1:
                return 0
            else:
                return result['code']
        else:
            return -1

    def http_post_get_map_distance(self, cols, rows, start_position, end_position):
        """
        获取两个地图坐标之间的相差几步
        :param start_position 起始点坐标
        :param end_position 终点坐标
        :return: 返回步数
        """
        result = self._http_post(
            url="/ai/aistart/getMapDistance",
            data={"cols": cols, "rows": rows, "start_position": start_position, "end_position": end_position}
        )

        if result is not None:
            if result['code'] == 1:
                return result['data']
            else:
                return result['code']
        else:
            return -1

    def http_post_get_move_path(self, cols, rows, start_position, end_position):
        """
        算子到目标位置的最短机动路线
        :param start_position 起始点坐标
        :param end_position 终点坐标
        :return: 返回步数
        """
        result = self._http_post(
            url="/ai/aistart/getMovePath",
            data={"cols": cols, "rows": rows, "start_position": start_position, "end_position": end_position}
        )

        if result is not None:
            if result['code'] == 1:
                return result['data']
            else:
                return result['code']
        else:
            return -1

    def http_post_satellite_reconnaissance(self, statellite_position):
        """
        卫星侦察时节
        :param statellite_position 卫星侦察坐标
        :return: 0：发送侦察成功;-1参数错误; -2:发送侦察失败
        """
        result = self._http_post(
            url="/ai/actionplan/satellite_reconnaissance",
            data={"start_position": statellite_position, "room_id": self._room.room_id, "camp_id": self._room.camp_id, "scenario_id": self._room.scenario_id}
        )

        if result is not None:
            if result['code'] == 1:
                return result['code']
            else:
                return result['code']
        else:
            return -1

    def _http_post(self, url, data=None, headers=None, files=None):
        """
        封装post请求，return响应码和响应内容
        :param url: 接口地址
        :param data: 接口数据
        :param headers: 接口headers
        :param files: 文件类型数据
        :return:
        """
        try:
            if self._token.token is not None:
                headers = {"token": self._token.token}
            logging.info("请求的地址：%s" % url)
            logging.info("请求的headers：%s" % headers)
            r = requests.post(self._url+url, data=data, headers=headers, files=files)
            logging.info("请求的内容：%s" % data)
            status_code = r.status_code  # 获取返回的状态码
            logging.info("获取返回的状态码:%d" % status_code)
            response_json = r.json()  # 响应内容，json类型转化成python数据类型
            logging.info("响应内容：%s" % response_json)
            # return status_code, response_json  # 返回响应码，响应内容
            return response_json  # 返回响应码，响应内容
        except BaseException as e:
            logging.error("请求失败！", exc_info=1)

    def _http_post_json(self, url, data=None, headers=None, files=None):
        """
        封装post json请求，return响应码和响应内容
        :param url: 接口地址
        :param data: 接口数据
        :param headers: 接口headers
        :param files: 文件类型数据
        :return:
        """
        try:
            data = json.dumps(data).encode('utf-8')  # python数据类型转化为json数据类型
            if self._token.token is not None:
                headers = {"token": self._token.token}
            logging.info("请求的地址：%s" % url)
            logging.info("请求的headers：%s" % headers)
            r = requests.post(self._url + url, data=data, headers=headers, files=files)
            logging.info("请求的内容：%s" % data)
            status_code = r.status_code  # 获取返回的状态码
            logging.info("获取返回的状态码:%d" % status_code)
            response_json = r.json()  # 响应内容，json类型转化成python数据类型
            logging.info("响应内容：%s" % response_json)
            # return status_code, response_json  # 返回响应码，响应内容
            return response_json  # 返回响应码，响应内容
        except BaseException as e:
            logging.error("请求失败！", exc_info=1)
        pass

    def _http_get(self, url, data=None, headers=None):
        """
        封装gett请求，return响应码和响应内容
        :param url: 接口地址
        :param data: 接口数据
        :param headers: 接口headers
        :return:
        """
        try:
            if self._token.token is not None:
                headers = {"token": self._token.token}
            logging.info("请求的headers：%s" % headers)
            r = requests.get(self._url+url, data, headers=headers)
            logging.info("请求的内容：%s" % data)
            status_code = r.status_code  # 获取返回的状态码
            logging.info("获取返回的状态码:%d" % status_code)
            response_json = r.json()  # 响应内容，json类型转化成python数据类型
            logging.info("响应内容：%s" % response_json)
            return response_json
        except BaseException as e:
            logging.error("请求失败！", exc_info=1)

    def _http_post_engine(self, url, data=None, headers=None, files=None):
        """
        封装post请求，return响应码和响应内容
        :param url: 接口地址
        :param data: 接口数据
        :param headers: 接口headers
        :param files: 文件类型数据
        :return:
        """
        try:
            if self._token.token is not None:
                headers = {"token": self._token.token}
            logging.info("请求的地址：%s" % url)
            logging.info("请求的headers：%s" % headers)
            r = requests.post(self._engine_url+url, data=data, headers=headers, files=files)
            logging.info("请求的内容：%s" % data)
            status_code = r.status_code  # 获取返回的状态码
            logging.info("获取返回的状态码:%d" % status_code)
            response_json = r.json()  # 响应内容，json类型转化成python数据类型
            logging.info("响应内容：%s" % response_json)
            # return status_code, response_json  # 返回响应码，响应内容
            return response_json  # 返回响应码，响应内容
        except BaseException as e:
            logging.error("请求失败！", exc_info=1)

if __name__ == "__main__":
    pass


