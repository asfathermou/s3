# --coding:utf-8--

import sys
import time
import os
sys.path.append("..")
import ai_mj.ai_const as const
from configure import Configure
from utils.logger import Logger
from ai_mj.ai_algorithm_2 import AIAlgorithm
from csf_sdk import CSFInterface
from entities.parsing.complete_battle_state import CompleteBattleState
from rl_env.update_operator import UpdateOperator
from rl_env.update_operator import UpdateOperator
from rl_env.cal_map import Hex
from entities.hexagon.graph import Graph

class DemoAI:
    def __init__(self):
        conf = Configure(sys.argv)
        conf.username = "lyu2"  # 选手自己的用户名
        conf.password = "lyu"  # 选手自己的密码
        # 单机版推演系统，变量初始化：room_id固定为1
        self._sdk = CSFInterface(conf.ip, conf.room_id, conf.camp_id, conf.scenario_id, conf.seat_id)
        self._init_failed = False
        self._scenario = None
        self._camp_id = None
        self._seat_ids = None
        self._war_map = None
        self._logger = Logger("ai_2")
        self._fetch_scenario_finish = False
        self._seat_ids = []
        self._round = 1
        for seat_id in conf.seat_id.split(','):
            self._seat_ids.append(int(seat_id))
        self._camp_id = conf.camp_id

        self._game_started = False

        # 创建AI算法对象
        self._algorithm = AIAlgorithm(self._sdk, self._scenario, conf.camp_id, conf.scenario_id)
        self._algorithm.set_logger(self._logger)
        self._algorithm.set_env(self._seat_ids)

        self.df_operator = None
        self.df_formation = None
        self.operator_information_original = []
        # self.operator_list = []
        self._row = 0
        self._col = 0
        self._update_operator = UpdateOperator(self._scenario)
        self._cal_map = Hex(self._row, self._col)
        self._graph = None

        # 注册回调函数
        self._sdk.register(self._call_back)

        # AI登录
        print(conf.username, conf.password)
        self._login_result = self._sdk.login(conf.username, conf.password)
        print("_login_result:{}".format(self._login_result))
        if self._login_result != 0:
            self._init_failed = True
            self._logger.print(self._round, "AI1 登陆失败")
            return

    def start(self):
        if self._init_failed:
            self._logger.print(self._round, "登录失败，请重试")
            return

        # 加入房间(加入战役指挥员席位,飞机水面编队指挥员席位，岸基潜艇指挥员席位)
        join_room_result = self._sdk.joinRoom()
        self._logger.print(self._round, "join room:{}".format(join_room_result))

        # 获取想定信息
        self._scenario, scenario_json_string = self._sdk.fetchScenario()
        self._row = self._scenario.war_map.rows
        self._col = self._scenario.war_map.cols
        self._cal_map.set_row_col(self._row, self._col)
        self._graph = Graph(max_row=self._row, max_col=self._col)
        self.operator_information_original = self._update_operator.get_operator_original_information(self._scenario)
        self._update_operator.set_env(self._cal_map)


        self._algorithm.set_scenario(self._scenario)
        self._fetch_scenario_finish = True
        self._logger.print(self._round, "_scenario_info:{}".format(self._scenario))

        # 等待开始，开始后回调函数会被调用 _call_back

    def _call_back(self, response):
        if "data" in response and "round" in response["data"]:
            self._round = response["data"]["round"]

        # 根据type值，做不同的处理,详细信息参见/data/websocket返回数据说明.json
        if response["type"] == const.BEGIN_GAME:
            self._logger.print(self._round, "callbackdata: %s" % response)
            if self._game_started:
                return
            self._game_started = True
            # 等待接收想定数据完成
            while not self._fetch_scenario_finish:
                time.sleep(0.1)
            # 设置出动所有兵力
            send_result = self._sdk.battle_seat.sendNotDispatchTroops([])
        elif response["type"] == const.ENGINE:
            # 根据不同时节，做成不同的响应
            self._algorithm.set_round(self._round)
            if response["data"]["time_interval"] != 30403:
                self._logger.print(self._round, "callbackdata: %s " % response)
            battle_state = CompleteBattleState.parse(response, self._scenario, self._camp_id)
            time_section_id = battle_state.get_time_section_id()
            self.df_operator = self._update_operator.update_operator_property(battle_state,
                                                                              self.operator_information_original)
            self._algorithm.set_df_operator(self.df_operator)
            self.df_formation = self._update_operator.create_df_formation()
            self._algorithm.set_df_formation(self.df_formation)

            print("我方算子id， 位置， 状态，编队id:")
            for i in battle_state.our_operators:
                print(i.operator_id, i.position, i.state,
                      i.formation_id if hasattr(i, 'formation_id') else -1)
            print("敌方算子id， 位置， 状态， 编队id:")
            for i in battle_state.enemy_operators:
                print(i.operator_id, i.position, i.state,
                      i.formation_id if hasattr(i, 'formation_id') else -1)
            # print(battle_state.our_operators[0].operator_id, battle_state.our_operators[0].position)
            # print(battle_state.our_operators[1].operator_id, battle_state.our_operators[1].position)
            # print(battle_state.our_operators[2].operator_id, battle_state.our_operators[2].position)
            # print(battle_state.our_operators[3].operator_id, battle_state.our_operators[3].position)

            if time_section_id == 30301:
                # 需要在情报支援环节之后，才能更新对对方的侦察情况
                # self.df_formation = self._update_operator.create_df_formation()
                # self._algorithm.set_df_formation(self.df_formation)
                pass

            # if time_section_id == 70101:
                # 推演结束，获取所有非空的裁决信息
            # judgement_string = self._update_operator.get_judgement_string()
            # self._algorithm.set_judgement_string(judgement_string)

            self._algorithm.make_decision(battle_state)
        else:
            # 可以看到心跳等信息
            self._logger.print(self._round, "callbackdata: %s " % response)

    def _ai_clean(self):
        self._scenario = None
        self._camp_id = None
        self._seat_ids = None
        self._war_map = None
        self._fetch_scenario_finish = False
        self._game_started = False


if __name__ == "__main__":
    demo_ai = DemoAI()
    demo_ai.start()

    # 注 其实room_id camp_id 等这些不用设置，不用填写，只需要读取接受一次即可

    # csfSdk = CSFInterface('127.0.0.1', 1, 1, 1, '101,102')

    # 注册回调函数，需要在登录之前先注册
    # csfSdk.register(testws)

    # 1.1 授权登录
    # rs = csfSdk.login('ztao', 'woaiwojia')

    # 1.7 加入房间
    # joinRoom = csfSdk.joinRoom()

    # 1.4 获取想定
    # scenarion = csfSdk.fetchScenario()
    # 获取想定后，等待开始命令（在回调函数中接收）

