# --coding:utf-8--

# @Author: 逸风
# @Time: 2019-12-20


import json

from entities.battle_state import BattleState
from entities.scenario import Scenario
from entities.user import User
from entities.token import Token
from csf_http_client import CSFhttpClient
from seat.battle_seat import BattleSeat
from seat.operator_seat import OperatorSeat
from entities.room import Room
from utils.socket_util import WebSocketUtil
from utils.rule_checks_util import RuleChecksUtil


"""
中国海上舰队(Chinese Sea Fleet)接口
"""
class CSFInterface:
    def __init__(self, ip_address, room_id, camp_id, scenario_id, seat_id):
        self._user = User()
        self._token = Token()
        self._room = Room()
        self._ip_address = ip_address
        self._room.room_id = room_id
        self._room.seat_id = seat_id
        self._room.camp_id = camp_id
        self._room.scenario_id = scenario_id
        self._scenario_info = None
        self._call_back_func = None
        self._socket = None
        self._http_client = None
        self.battle_seat = None
        self.operator_seat = None
        self.rule_checks = None

    def register(self, call_back_func):
        """
        注册回调函数
        :param call_back_funcs: call_back_func
        :return:
        """
        self._call_back_func = call_back_func
        self._socket = WebSocketUtil(self._ip_address, self._call_back_func)
        self._http_client = CSFhttpClient(self._user, self._token, self._ip_address, self._room, self._socket)
        self.battle_seat = BattleSeat(self._http_client, self._room)
        self.operator_seat = OperatorSeat(self._http_client, self._user, self._room)

    def login(self, username, password, ip=None, force=0):
        """
        用户登录认证
        :param username: 用户名
        :param password: 密码
        :param ip: 服务器IP地址
        :param force: 是否强制登录；非必须；强制登录时，若已有存在的登录，则强制其下线。0表示不强制登录，1表示强制登录，默认值为0
        :return:
        """

        if username is None:
            # print('请输入用户名')
            return -1
        if password is None:
            # print('请输入密码')
            return -1

        user_result = self._http_client.http_post_login(username, password)

        return user_result

    def fetchUserInfo(self):
        """

        获取用户基本信息
        :return:
        """
        return self._user

    def fetchRoomInfo(self):

        return self._room

    def fetchToken(self):
        """
        获取token
        :return:
        """
        return self._token.token

    def fetchScenario(self):
        """
        获取想定信息
        :param scenario_id:
        :param room_id:
        :return:
        """
        scenario_json_string = self._http_client.http_get_scenario_info()
        # print(scenario_json_string)
        if scenario_json_string == -2:
            return '想定不存在',None
        elif scenario_json_string is not None:
            scenario = Scenario.parse(scenario_json_string)

            self._scenario_info = scenario
            self.rule_checks = RuleChecksUtil(scenario)
            self.battle_seat.set_scenario(scenario)
            return scenario,scenario_json_string
        else:
            return None,None


    def joinRoom(self):
        """
        获取推演室信息
        :param room_id:
        :param user_id:
        :param seat_id:
        :param camp_id:
        :return:
        """

        result = self._http_client.http_post_join_room()

        return result

    def leaveRoom(self, room_id):
        """
        退出推演室
        :param room_id: 推演室ID
        :return:
        """
        result = self._http_client.http_get_exit_room(room_id)

        return result

    def exitSeats(self, room_id, camp_id, seat_id):
        """
        退出席位
        :param room_id: 推演室ID
        :param camp_id: 阵营ID
        :param seat_id: 席位ID
        :return:
        """

        result = self._http_client.http_get_exit_seat(room_id, camp_id, seat_id)

        return result

    def changePresenter(self, room_id, camp_id, country_id):
        """
        推演方变更接口
        :param room_id: 推演室ID
        :param camp_id: 阵营ID
        :param country_id: 国家ID
        :return:
        """
        result = self._http_client.http_post_change_presenter(room_id, camp_id, country_id)

        return result

    def rulingFinished(self, section_id):
        """
        裁决完成接口
        :param section_id:
        :return:
        """
        result = self._http_client.http_post_ruling_finished(section_id)
        return result

    def airplane_return(self, operator_id, position, section_id, return_type):
        """
        飞机返航接口
        :param operator_id: 算子ID
        :param position: 坐标
        :param section_id: 时节ID
        :param return_type: 返航类型：0=手动，1=自动
        :return:
        """
        result = self._http_client.http_post_airplane_return(operator_id, position, section_id, return_type)

        return result

    def http_post_airplane_return_finished(self, section_id):
        """
        飞机返回完成接口
        :param section_id:
        :return:
        """
        result = self._http_client.http_post_airplane_return_finished(section_id)

        return result

    def set_country_camp(self, country_id, camp_id):
        self.battle_seat.country_id = country_id
        self.operator_seat.country_id = country_id
        self.battlscenario_infoe_seat.camp_id = camp_id
        self.operator_seat.camp_id = camp_id

    def fetch_battle_state(self, room_id, user_id):
        battle_state_json_string = self._http_client.http_fetch_battle_state(room_id, user_id)
        battle_state = BattleState.parse(battle_state_json_string)
        return battle_state

    def taskDeployCheck(self, operatorID, taskID):
        """
        为算子分配任务时，需要先检查算是否可以执行相应任务
        :param operatorID: 算子ID
        :param taskID: 任务类型ID
        :return:
        """
        result = self.rule_checks.taskDeployCheck(operatorID, taskID)

        return result

    def awacsCommandCheck(self, operatorID, coordinate):
        """
        检查预警指挥机是否符合部署条件
        :param operatorID:  算子ID
        :param coordinate: 部署坐标
        :return:
        """
        pass

    def reefsLandingCheck(self, operator_id=None, coordinate=None):
        """
        岛礁登陆检查
        :param operator_id:
        :param coordinate:
        :return:
        """
        if (operator_id is None or coordinate is None):
            return -1
        else:
            result = self.rule_checks.reefsLandingCheck(operator_id, coordinate)
            return result

    def getMapDistance(self, start_position, end_position):
        """
        计算两个地图坐标之间的相差几步
        :param start_position 起始点坐标 [1,2]
        :param end_position 终点坐标 [2,3]
        :return: 返回距离
        """
        y1, x1 = start_position
        y2, x2 = end_position
        du = x2 - x1
        dv = (y2 + x2 // 2) - (y1 + x1 // 2)
        return max(abs(du), abs(dv)) if ((du >= 0 and dv >= 0) or (du < 0 and dv < 0)) else abs(du) + abs(dv)

    def getMovePath(self, operator_position, end_position):
        """
        算子到目标位置的最短机动路线
        :param operator_position 算子所在坐标
        :param end_position 终点坐标
        :return: 返回路线坐标
        """
        cols = self._scenario_info.war_map.cols  # 想定地图列数
        rows = self._scenario_info.war_map.rows  # 想定地图行数

        result = self._http_client.http_post_get_move_path(cols, rows, operator_position, end_position)
        return result

    def statelliteReconnaissance(self, statellite_position):
        """
        卫星侦察时节
        :param statellite_position 侦察坐标 字符串，形如 "26,24"
        :return: 0：发送侦察成功;-1参数错误; -2:发送侦察失败
        """
        result = self._http_client.http_post_satellite_reconnaissance(statellite_position)
        return result


if __name__ == "__main__":

    pass


