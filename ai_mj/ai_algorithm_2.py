# --coding:utf-8--

import ai_mj.ai_const as const
import random
import sys
import time
from utils_shen.tools import get_reach_range
from random import randint, sample
from ai_mj.helper import Helper
helper = Helper()
from rl_env import cal_map
from collections import defaultdict
"""
    AI算法类： AI 开发者要实现的主体
"""
class AIAlgorithm:

    def __init__(self, sdk, scenario, camp_id, scenario_id):
        self._sdk = sdk
        self._scenario = scenario
        self._scenario_id = scenario_id
        self._camp_id = camp_id
        self._enemy_camp_id = 1 if self._camp_id == 2 else 2
        self._seat_id = None
        self._round = None
        self.df_operator = None
        self.df_formation = None
        self._logger = None
        self._plan_string = ""
        self.judgement_string = ""


        # 变量初始化
        self.zhencha_renwu_ids = []
        self.zhanshuzhiyuan_renwu_ids = []
        self.jieji_renwu_ids = []
        self.bulei_renwu_ids = []
        self.yujingzhihui_renwu_ids = []

        self.jieji_winner_camp = -1
        self.quzhu_winner_camp = -1

        self.yujingzhihuiji_deploy_list = []
        self._volley_close_air_to_air_counter = 0
        self._expulsion_close_air_to_air_counter = 0


        # 不同时节ID到相应的处理函数映射表
        self._decision_map = {
            # 1 分派兵力
            10501: self._send_troops,

            # 2 调整初始位置========================================================
            10502: self._adjust_initial_positions,

            # 情报支援
            20101: self._information_support,

            #  航空任务部署
            30301: self._deploy_aviation_task,

            # 截机远距离确认
            30401: self._volley_remote_air_to_air,

            # 截机近战前，是否返航确认
            30402: self._volley_close_air_to_air,

            # 截机，主要是任务飞机的位置改变
            30403: self._volley,

            # 是否驱逐确认
            30404: self._confirm_expulsion,

            # 驱逐远距离确认
            30501: self._expulsion_remote_air_to_air,

            # 驱逐，主要是任务飞机的位置改变
            30503: self._expulsion,

            # 驱逐近战前，是否返航确认
            30502: self._expulsion_close_air_to_air,

            #  飞机布雷
            30601: self._bray,

            # 飞机侦察
            30702: self._airplane_investigate,

            #  预警指挥机部署
            30801: self._deploy_awacs,

            #  部署战斗空中巡逻
            30901: self._air_patrol,

            # 扫雷
            31001: self._sweep_mine,

            #  岸基单位行动设置
            40101: self._plan_shore_units,

            #  作战命令下达
            40201: self._issure_operation_orders,

            #  调整编队==============================================
            41301: self._adjust_formation,

            #  设置潜艇航行模式
            41401: self._set_submarine_mode,

            # 攻击,机动设置===============================================
            41501: self._set_attack_and_move,

            # 行动裁决
            51401: self._attack_and_move,

            # 岸基单位裁决
            40102: self._shore_units_attack,

            # 裁决完毕
            51402: self._judge_finish,

            # 手动飞机返航
            61601: self._airplane_manual_return,

            # 推演结束
            70101: self._game_over
        }

    def set_round(self, round):
        self._round = round

    def set_logger(self, logger):
        self._logger = logger

    def set_scenario(self, scenario):
        self._scenario = scenario
        self._row = self._scenario.war_map.rows
        self._col = self._scenario.war_map.cols

    def set_env(self, seat_id):
        self._seat_id = seat_id

    def set_df_operator(self, df_operator):
        self.df_operator = df_operator

    def set_df_formation(self, df_formation):
        self.df_formation = df_formation

    def set_judgement_string(self, judgement_string):
        self.judgement_string = judgement_string

    def make_decision(self, battle_state):
        time_section_id = battle_state.get_time_section_id()
        if time_section_id in self._decision_map:
            self._decision_map[time_section_id](battle_state)

    def _send_troops(self, battle_state):
        """
        分派兵力
        :param battle_state: 当前战斗态势
        """
        self._logger.print(self._round, "分派兵力")
        # 填写我方不出动单位的列表，[{"operator_id":120201,"position":"7,9"}]，
        # 在此时节，调用一次下方接口
        self._sdk.battle_seat.sendNotDispatchTroops([])



    def _information_support(self, battle_state):
        """
        情报支援
        :param battle_state: 当前战斗态势
        """
        self._logger.print(self._round, "AI 发送 情报支援完成")
        # 在此时节，调用一次下方接口
        result = self._sdk.battle_seat.intelligence_support()

    def _deploy_aviation_task(self, battle_state):
        """
        航空任务部署
        :param battle_state: 当前战斗态势
        """
        self.zhencha_renwu_ids = []
        self.zhanshuzhiyuan_renwu_ids = []
        self.jieji_renwu_ids = []
        self.bulei_renwu_ids = []
        self.yujingzhihui_renwu_ids = []

        if self._round == 1:
            e2t_info = helper.fetch_operator(self.df_operator, self._camp_id, "e2t")
            if e2t_info is None:
                # E2T预警机已毁
                pass
            else:
                if e2t_info["x_position"] == 22 and e2t_info["y_position"] == 25:
                    # E2T预警机已部署在2225
                    pass
                else:
                    #  按无损-有损顺序从蓝方F16C-1、2、3、4中选两架空中算子F16C-a和F16C-b，其余全部出动
                    f1_info = helper.fetch_operator(self.df_operator, self._camp_id, "f1")
                    f2_info = helper.fetch_operator(self.df_operator, self._camp_id, "f2")
                    f3_info = helper.fetch_operator(self.df_operator, self._camp_id, "f3")
                    f4_info = helper.fetch_operator(self.df_operator, self._camp_id, "f4")
                    order = []
                    if f1_info is not None:
                        order.append((f1_info["operator_id"], f1_info["state"]))
                    if f2_info is not None:
                        order.append((f2_info["operator_id"], f1_info["state"]))
                    if f3_info is not None:
                        order.append((f3_info["operator_id"], f1_info["state"]))
                    if f4_info is not None:
                        order.append((f4_info["operator_id"], f1_info["state"]))
                    order.sort(key=lambda x: x[1])
                    order = [i[0] for i in order]
                    if len(order) > 2:
                        self.jieji_renwu_ids.extend(order[2:])
                    # self.zhencha_renwu_ids.append(e2t_info["operator_id"])
                    self.yujingzhihui_renwu_ids.append(e2t_info["operator_id"])
                    f5_info = helper.fetch_operator(self.df_operator, self._camp_id, "f5")
                    f6_info = helper.fetch_operator(self.df_operator, self._camp_id, "f6")
                    f7_info = helper.fetch_operator(self.df_operator, self._camp_id, "f7")
                    f8_info = helper.fetch_operator(self.df_operator, self._camp_id, "f8")
                    if f5_info is not None:
                        self.jieji_renwu_ids.append(f5_info["operator_id"])
                    if f6_info is not None:
                        self.jieji_renwu_ids.append(f6_info["operator_id"])
                    if f7_info is not None:
                        self.jieji_renwu_ids.append(f7_info["operator_id"])
                    if f8_info is not None:
                        self.jieji_renwu_ids.append(f8_info["operator_id"])
        aviation_mission_list = []
        # 类型：101:截击任务;102:布雷任务;103:侦察任务;104:预警指挥任务;105:战术支援任务
        for operator_id in self.zhencha_renwu_ids:
            deploy_dict = {"operator_id": operator_id, "type": 103}  # 103:侦察任务
            aviation_mission_list.append(deploy_dict)
        for operator_id in self.zhanshuzhiyuan_renwu_ids:
            deploy_dict = {"operator_id": operator_id, "type": 105}  # 105:战术支援任务
            aviation_mission_list.append(deploy_dict)
        for operator_id in self.jieji_renwu_ids:
            deploy_dict = {"operator_id": operator_id, "type": 101}  # 101:截击任务
            aviation_mission_list.append(deploy_dict)
        for operator_id in self.bulei_renwu_ids:
            deploy_dict = {"operator_id": operator_id, "type": 102}  # 102:布雷任务
            aviation_mission_list.append(deploy_dict)
        for operator_id in self.yujingzhihui_renwu_ids:
            deploy_dict = {"operator_id": operator_id, "type": 104}  # 104:预警指挥任务
            aviation_mission_list.append(deploy_dict)

        self._logger.print(self._round, "ai 发送 航空任务部署")
        self._logger.print(self._round, str(aviation_mission_list))
        # 在此时节，调用一次下方接口
        res = self._sdk.battle_seat.aviationMissionDeployment(aviation_mission_list)
        print(res)

    def _volley_remote_air_to_air(self, battle_state):
        """
        截机远距离确认
        :param battle_state: 当前战斗态势
        """
        have_remote_air_to_air_ability_jieji_ids = []
        for jieji_id in self.jieji_renwu_ids:
            war_operator = battle_state.fetch_our_operator_by_id(jieji_id)
            if war_operator:  # 算子是否还存在（可能已阵亡）
                if war_operator.is_blos:
                    have_remote_air_to_air_ability_jieji_ids.append(jieji_id)

        operator_id_strs = []  # ['230301', '230302']
        attack_type = 106  # 106:截击时节;107:驱逐时节
        action_type = 1  # 1:远距离攻击;2=返航;3=驱逐
        section_id = 30401  # 30401：截击时节远距离确认; 30501:驱逐时远距离确认; 30402:截击时的返航确认; 30502:驱逐时的返航确认
        is_long_air = 0  # 是否实施远距离空战：0:否;1:是
        is_return = 0  # 是否返航：0:否;1:是
        is_expel = 0  # 是否驱逐：0:否;1:是

        for id in self.jieji_renwu_ids:  # 添加相关任务ids
            operator_id_strs.append(str(id))
        if have_remote_air_to_air_ability_jieji_ids:
            # 确认进行远距离攻击
            is_long_air = 1  # 是否实施远距离空战：0:否;1:是
        else:
            # 不进行远距离攻击
            is_long_air = 0  # 是否实施远距离空战：0:否;1:是

        self._logger.print(self._round, "是否远距离攻击： %s " % is_long_air)
        self._logger.print(self._round, str(operator_id_strs))
        self._logger.print(self._round, "ai 发送 截击远距离确认")
        # 在此时节，调用一次下方接口
        aviationVolleyExpulsion = self._sdk.battle_seat.aviationVolleyExpulsion(attack_type, action_type, section_id,
                                                                                is_long_air, is_return, is_expel,
                                                                                operator_id_strs)

    def _volley_close_air_to_air(self, battle_state):
        """
        截机近战前，是否返航确认
        :param battle_state: 当前战斗态势
        """
        self._volley_close_air_to_air_counter += 1
        # 每回合，该时节会收到两次，只需在第二次发送 确认即可

        if self._volley_close_air_to_air_counter == 2:  # 第一次收到不做回应，第二次收到处理
            self._volley_close_air_to_air_counter = 0

            operator_id_strs = []  # ['230301', '230302']
            attack_type = 106  # 106:截击时节;107:驱逐时节
            action_type = 2  # 1:远距离攻击;2=返航;3=驱逐
            section_id = 30402  # 30401：截击时节远距离确认; 30501:驱逐时远距离确认; 30402:截击时的返航确认; 30502:驱逐时的返航确认
            is_long_air = 0  # 是否实施远距离空战：0:否;1:是
            is_return = 0  # 是否返航：0:否;1:是
            is_expel = 0  # 是否驱逐：0:否;1:是

            is_return = 0
            for id in self.jieji_renwu_ids:  # 添加相关任务ids
                operator_id_strs.append(str(id))

            self._logger.print(self._round, "ai 发送 截击，是否返航")
            # 在每回合，第二次进入此时节时，调用一次下方接口
            aviationVolleyExpulsion = self._sdk.battle_seat.aviationVolleyExpulsion(attack_type, action_type, section_id,
                                                                                    is_long_air, is_return, is_expel,
                                                                                    operator_id_strs)

    def _volley(self, battle_state):
        """
        截机，主要是任务飞机的位置改变
        :param battle_state: 当前战斗态势
        """
        # 在此时节，不需向接口做任何回应
        pass

    def _confirm_expulsion(self, battle_state):
        """
        是否驱逐确认
        :param battle_state: 当前战斗态势
        """
        self.jieji_winner_camp = battle_state.get_volley_or_expulsion_winner_camp()

        operator_id_strs = []  # ['230301', '230302']
        attack_type = 106  # 106:截击时节;107:驱逐时节
        action_type = 3  # 1:远距离攻击;2=返航;3=驱逐
        section_id = 30404  # 30401：截击时节远距离确认; 30501:驱逐时远距离确认; 30402:截击时的返航确认; 30502:驱逐时的返航确认; 30404:截击后，询问是否驱逐
        is_long_air = 0  # 是否实施远距离空战：0:否;1:是
        is_return = 0  # 是否返航：0:否;1:是
        is_expel = 0  # 是否驱逐：0:否;1:是

        self._logger.print(self._round, "ai 发送 是否驱逐")
        quzhu_ids = self.zhencha_renwu_ids + self.zhanshuzhiyuan_renwu_ids + self.bulei_renwu_ids + self.yujingzhihui_renwu_ids
        for id in quzhu_ids:
            operator_id_strs.append(str(id))

        if self._camp_id == self.jieji_winner_camp:  # 我方是截击胜方
            # 发送驱逐
            is_expel = 1
        else:  # 我方不是截击胜方（可能是负方，或者双方都未取得截击胜利）
            # 发送不驱逐
            is_expel = 0

        # 在此时节，调用一次下方接口
        aviationVolleyExpulsion = self._sdk.battle_seat.aviationVolleyExpulsion(attack_type, action_type,
                                                                                section_id,
                                                                                is_long_air, is_return, is_expel,
                                                                                operator_id_strs)

    def _expulsion_remote_air_to_air(self, battle_state):
        """
        驱逐远距离确认
        :param battle_state: 当前战斗态势
        """
        have_remote_air_to_air_ability_quzhu_ids = []
        quzhu_ids = self.zhencha_renwu_ids + self.zhanshuzhiyuan_renwu_ids + self.bulei_renwu_ids + self.yujingzhihui_renwu_ids

        operator_id_strs = []  # ['230301', '230302']
        attack_type = 107  # 106:截击时节;107:驱逐时节
        action_type = 1  # 1:远距离攻击;2=返航;3=驱逐
        section_id = 30501  # 30401：截击时节远距离确认; 30501:驱逐时远距离确认; 30402:截击时的返航确认; 30502:驱逐时的返航确认; 30404:截击后，询问是否驱逐
        is_long_air = 0  # 是否实施远距离空战：0:否;1:是
        is_return = 0  # 是否返航：0:否;1:是
        is_expel = 0  # 是否驱逐：0:否;1:是

        for quzhu_id in quzhu_ids:
            operator_id_strs.append(str(quzhu_id))
            war_operator = battle_state.fetch_our_operator_by_id(quzhu_id)
            if war_operator:
                have_remote_air_to_air_ability_quzhu_ids.append(quzhu_id)
        if have_remote_air_to_air_ability_quzhu_ids:
            # 确认进行远距离攻击
            is_long_air = 1
        else:
            # 不进行远距离攻击
            is_long_air = 0

        self._logger.print(self._round, "ai 发送 驱逐远距离确认")
        # 在此时节，调用一次下方接口
        aviationVolleyExpulsion = self._sdk.battle_seat.aviationVolleyExpulsion(attack_type, action_type,
                                                                                section_id,
                                                                                is_long_air, is_return, is_expel,
                                                                                operator_id_strs)

    def _expulsion(self, battle_state):
        """
        驱逐，主要是任务飞机的位置改变
        :param battle_state: 当前战斗态势
        """
        # 在此时节，不需向服务器做任何响应
        pass

    def _expulsion_close_air_to_air(self, battle_state):
        """
        驱逐近战前，是否返航确认
        :param battle_state: 当前战斗态势
        """
        self._expulsion_close_air_to_air_counter += 1

        if self._expulsion_close_air_to_air_counter == 2:  # 每回合，该时节会收到两次，只需在第二次发送 确认即可
            self._expulsion_close_air_to_air_counter = 0

            quzhu_ids = self.zhencha_renwu_ids + self.zhanshuzhiyuan_renwu_ids + self.bulei_renwu_ids + self.yujingzhihui_renwu_ids

            operator_id_strs = []  # ['230301', '230302']
            attack_type = 107  # 106:截击时节;107:驱逐时节
            action_type = 2  # 1:远距离攻击;2=返航;3=驱逐
            section_id = 30502  # 30401：截击时节远距离确认; 30501:驱逐时远距离确认; 30402:截击时的返航确认; 30502:驱逐时的返航确认; 30404:截击后，询问是否驱逐
            is_long_air = 0  # 是否实施远距离空战：0:否;1:是
            is_return = 0  # 是否返航：0:否;1:是
            is_expel = 0  # 是否驱逐：0:否;1:是

            is_return = 0
            for quzhu_id in quzhu_ids:
                operator_id_strs.append(str(quzhu_id))

            self._logger.print(self._round, "ai 发送 驱逐是否返航")
            # 在每回合，第二次进入此时节时，调用一次下方接口
            aviationVolleyExpulsion = self._sdk.battle_seat.aviationVolleyExpulsion(attack_type, action_type,
                                                                                    section_id,
                                                                                    is_long_air, is_return, is_expel,
                                                                                    operator_id_strs)

    def _bray(self, battle_state):  # 飞机布雷
        self.quzhu_winner_camp = battle_state.get_volley_or_expulsion_winner_camp()
        # 在此时节，无论能否布雷，都要调用一次接口 _sdk.battle_seat.aircraftBray，如果不能布雷或不想布雷则填空列表，如果能布雷则按照规则填写
        deploy_list = []
        aircraftBray = self._sdk.battle_seat.aircraftBray(deploy_list)

    def _airplane_investigate(self, battle_state):  # 飞机侦察
        # 在此时节，调用一次接口 _sdk.battle_seat.awacsDeployment(已在_deploy_awacs中调用)
        if (self.jieji_winner_camp == self._enemy_camp_id) and (self.quzhu_winner_camp == self._enemy_camp_id):
            # 截击被打败，驱逐也被打败，则不能执行后面的相关航空任务
            # 不会侦察到新的敌方单位
            self._deploy_awacs(battle_state)
        else:
            # 有可能会侦察到新的敌方单位
            self._deploy_awacs(battle_state)

    def _deploy_awacs(self, battle_state):
        """
        预警指挥机部署
        :param battle_state: 当前战斗态势
        """
        self.yujingzhihuiji_deploy_list = []

        if (self.jieji_winner_camp == self._enemy_camp_id) and (self.quzhu_winner_camp == self._enemy_camp_id):
            # 截击被打败，驱逐也被打败，则不能执行后面的相关航空任务
            # 不能部署
            pass
        else:
            # 可以部署
            e2t_info = helper.fetch_operator(self.df_operator, self._camp_id, "e2t")
            if e2t_info is None:
                pass
            else:
                deploy_data = {"operator_id": e2t_info["operator_id"], "seat_id": 10001, "position": "22,25"}
                self.yujingzhihuiji_deploy_list.append(deploy_data)
        self._logger.print(self._round, "ai 发送 预警指挥机部署")
        res = self._sdk.battle_seat.awacsDeployment(self.yujingzhihuiji_deploy_list)
        print(res)

    def _air_patrol(self, battle_state):
        """
        部署战斗空中巡逻
        :param battle_state: 当前战斗态势
        """
        deploy_list = []
        # operatorDict = {"operator_id": 130403, "seat_id":101, "position": "8,13", "target_id":182301}
        # deploy_list.append(operatorDict)
        e2t_info = helper.fetch_operator(self.df_operator, self._camp_id, "e2t")
        if e2t_info is None:
            pass
        else:
            if e2t_info["x_position"] == 22 and e2t_info["y_position"] == 25:
                f1_info = helper.fetch_operator(self.df_operator, self._camp_id, "f1")
                f2_info = helper.fetch_operator(self.df_operator, self._camp_id, "f2")
                f3_info = helper.fetch_operator(self.df_operator, self._camp_id, "f3")
                f4_info = helper.fetch_operator(self.df_operator, self._camp_id, "f4")
                order = []
                if f1_info is not None:
                    order.append((f1_info["operator_id"], f1_info["state"]))
                if f2_info is not None:
                    order.append((f2_info["operator_id"], f1_info["state"]))
                if f3_info is not None:
                    order.append((f3_info["operator_id"], f1_info["state"]))
                if f4_info is not None:
                    order.append((f4_info["operator_id"], f1_info["state"]))
                order.sort(key=lambda x: x[1])
                order = [i[0] for i in order]
                if len(order) <= 2:
                    for i in order:
                        deploy_data = {"operator_id": i, "seat_id": 101, "position": "22,25"}
                        deploy_list.append(deploy_data)
                else:
                    for i in order[:2]:
                        deploy_data = {"operator_id": i, "seat_id": 101, "position": "25,34"}
                        deploy_list.append(deploy_data)
                    for i in order[:2]:
                        deploy_data = {"operator_id": i, "seat_id": 101, "position": "22,25"}
                        deploy_list.append(deploy_data)
                f5_info = helper.fetch_operator(self.df_operator, self._camp_id, "f5")
                f6_info = helper.fetch_operator(self.df_operator, self._camp_id, "f6")
                f7_info = helper.fetch_operator(self.df_operator, self._camp_id, "f7")
                f8_info = helper.fetch_operator(self.df_operator, self._camp_id, "f8")
                order = []
                if f5_info is not None:
                    order.append((f5_info["operator_id"], f5_info["state"]))
                if f6_info is not None:
                    order.append((f6_info["operator_id"], f6_info["state"]))
                if f7_info is not None:
                    order.append((f7_info["operator_id"], f7_info["state"]))
                if f8_info is not None:
                    order.append((f8_info["operator_id"], f8_info["state"]))
                order.sort(key=lambda x: x[1])
                order = [i[0] for i in order]
                if len(order) <= 2:
                    for i in order:
                        deploy_data = {"operator_id": i, "seat_id": 101,  "position": "22,25"}
                        deploy_list.append(deploy_data)
                else:
                    for i in order[:2]:
                        deploy_data = {"operator_id": i, "seat_id": 101, "position": "28,34"}
                        deploy_list.append(deploy_data)
                    for i in order[:2]:
                        deploy_data = {"operator_id": i, "seat_id": 101, "position": "22,25"}
                        deploy_list.append(deploy_data)
        self._logger.print(self._round, "ai 发送 战斗空中巡逻")
        # 在此时节，调用一次下方接口
        res = self._sdk.battle_seat.airPatrol(deploy_list)
        print(res)

    def _sweep_mine(self, battle_state):
        """
        扫雷时节
        :param battle_state: 当前战斗态势
        """
        # 在此时节，直接转入岸基单位行动设置
        self._plan_shore_units(battle_state)
        pass

    def _plan_shore_units(self, battle_state):
        """
        岸基单位行动设置
        :param battle_state: 当前战斗态势
        """
        action_plan_list = []
        self._logger.print(self._round, "AI 发送 岸基单位行动设置")
        # 在此时节，调用一次下方接口
        shoreUnitActionPlan = self._sdk.battle_seat.shoreUnitActionPlan(action_plan_list)

    def _issure_operation_orders(self, battle_state):
        """
        作战命令下达
        :param battle_state: 当前战斗态势
        """
        # commandDict = {"seat": ['101', '102'], "main_target": ['230402', '230602'], "threaten_target": ['230301', '230302', '230601', '230602', '230701']}
        commandDict = {}
        self._logger.print(self._round, "ai 发送 作战命令下达")
        # 在此时节，调用一次下方接口
        operationalOrdersIssued = self._sdk.battle_seat.operationalOrdersIssued(commandDict)

        self._adjust_formation(battle_state)

    def _set_submarine_mode(self, battle_state):
        """
        设置潜艇航行模式
        :param battle_state: 当前战斗态势
        """
        self._logger.print(self._round, "ai 发送 潜艇航行模式设置")
        set_list = []
        # 在此时节，调用一次下方接口
        submarineVoyageMode = self._sdk.operator_seat.submarineVoyageMode(set_list)


    def _adjust_formation(self, battle_state):
        """
        调整编队
        :param battle_state: 当前战斗态势
        """
        # if self._test == 2:
        #     if self._round == 1:
        #         position = '07,06'
        #         move = 4
        #         operator_ids = ['210801', '210802', '210803', '210804']
        #
        #         self._sdk.operator_seat.createFormation(position, move, operator_ids)
        #
        # self._logger.print(self._round, "AI 发送 调整编队")
        # 创建编队
        # operatorIds = ['140202','140201']
        # position = '1,3'
        # move = 27  # 取几个算子最小值
        # createFormation = self._sdk.operator_seat.createFormation(position, move, operatorIds)

        # 编队调整
        # adjustFormationDict = {"deleted_formation_ids":[],"changed_formations":[{"operator_id":160107,"country_id":1,"rounds":1,"seat":101,"is_find":0,"operator_ids":["140201","140202"]}]}
        # adjustFormation = self._sdk.operator_seat.adjustFormation(adjustFormationDict)

        # 调整编队顺序
        # operatorID = 160119
        # orderAsuw = ['140202','140201']
        # orderFishAttact = ['140201','140202']
        # presetFormatioOrder = self._sdk.operator_seat.presetFormatioOrder(operatorID, orderAsuw, orderFishAttact)
        jilong1_info = helper.fetch_operator(self.df_operator, self._camp_id, "jilong1")
        jilong2_info = helper.fetch_operator(self.df_operator, self._camp_id, "jilong2")
        chenggong1_info = helper.fetch_operator(self.df_operator, self._camp_id, "chenggong1")
        chenggong2_info = helper.fetch_operator(self.df_operator, self._camp_id, "chenggong2")
        formation_dict = defaultdict(list)
        if jilong1_info is not None:
            position = f"{jilong1_info['x_position']},{jilong1_info['y_position']}"
            formation_dict[position].append((jilong1_info["operator_id"], jilong1_info["move"]))
        if jilong2_info is not None:
            position = f"{jilong2_info['x_position']},{jilong2_info['y_position']}"
            formation_dict[position].append((jilong2_info["operator_id"], jilong2_info["move"]))
        if chenggong1_info is not None:
            position = f"{chenggong1_info['x_position']},{chenggong1_info['y_position']}"
            formation_dict[position].append((chenggong1_info["operator_id"], chenggong1_info["move"]))
        if chenggong2_info is not None:
            position = f"{chenggong2_info['x_position']},{chenggong2_info['y_position']}"
            formation_dict[position].append((chenggong2_info["operator_id"], chenggong2_info["move"]))
        for key, val in formation_dict.items():
            if len(val) >= 2:
                min_move = 0
                operator_ids = []
                for operator_id, move in val:
                    min_move = min(min_move, move)
                    operator_ids.append(str(operator_id))
                self._sdk.operator_seat.createFormation(key, min_move, operator_ids)
        self._logger.print(self._round, "AI 发送 调整编队完成")
        section_id = 41301  # 此时节填写41301
        # 在此时节，做完调整编队后(上面编队调整的接口可以调用多次)，调用一次下方编队调整完成的接口
        res = self._sdk.operator_seat.formationFinished(section_id)
        print(res)

    def _adjust_initial_positions(self, battle_state):
        """
        调整初始位置
        :param battle_state:  当前战斗态势  当前战斗态势
        """
        adjust_list = []
        # if self._test == 3:
        #     # 获取我方算子信息
        #     df_our_formation = self.df_formation.loc[(self.df_formation['camp_id'] == str(self._camp_id))]
        #     x_position_float_list = df_our_formation['x_position'].values.tolist()
        #     y_position_float_list = df_our_formation['y_position'].values.tolist()
        #     move_list = df_our_formation['move'].values.tolist()
        #     index_list = df_our_formation.index.tolist()
        #     self._row = self._scenario.war_map.rows
        #     self._col = self._scenario.war_map.cols
        #
        #     assert x_position_float_list.__len__() == y_position_float_list.__len__() == move_list.__len__() == index_list.__len__()
        #     for j in range(index_list.__len__()):
        #         y = y_position_float_list[j]
        #         x = x_position_float_list[j]
        #         m = move_list[j]
        #         i = index_list[j]
        #         random_list = get_reach_range(x, y, m, self._row, self._col)
        #         position = random.choice(random_list)
        #         # adjust_list.append({'operator_id': i, 'position': str(position)[1:-1]})
        #         adjust_list.append({'operator_id': i, 'position': '{},{}'.format(position[0], position[1])})
        #
        # else:
        # 蓝方基隆1成功1由1922调整至2024，基隆2成功2由2622调整至2524
        adjust_list.append({'operator_id': 210201, 'position': '20,24'})
        adjust_list.append({'operator_id': 210401, 'position': '20,24'})
        adjust_list.append({'operator_id': 210202, 'position': '25,24'})
        adjust_list.append({'operator_id': 210402, 'position': '25,24'})
        self._logger.print(self._round, "AI 发送 调整算子初始位置")
        print(adjust_list)
        # 在此时节，调用一次下方接口
        res = self._sdk.battle_seat.adjustingInitialPosition(adjust_list)  # 调整初始位置，调整范围 adjustable_range
        print(res)

    def target_id_transform(self, src_id):
        """
        算子可以攻击的目标id列表格式转换成元素为int的list
        @param src_id: 攻击方id
        @return 转换后的list
        """
        target_id_list1 = self.df_formation.at[src_id, 'asm_attack_id'].split(',')
        target_id_list = []

        if target_id_list1 != ['']:
            for i in target_id_list1:
                target_id_list.append(int(i))

        return target_id_list


    def _set_attack_and_move(self, battle_state):
        """
        攻击,机动设置
        :param battle_state: 当前战斗态势
        """

        plan_list = []
        round_id = self._round
        # seat_id = self._seat_id
        seat_id = battle_state.our_operators[0].seat_id
        camp_id = self._camp_id


















        # # 3.17 作战筹划阶段-各种机动攻击数据接口
        # # operatorID = 120201
        # # act_order = '1'
        # # is_formation = 0
        # # maneuveringAttack = self._sdk.operator_seat.maneuveringAttack(operatorID, act_order, is_formation, act_content)
        #
        # # 当反舰导弹发起攻击编队目标时，从引擎获取具体攻击目标中的哪些单位
        # # 示例：
        # # round_id = self._round
        # # attack_formation_id = 160101
        # # attack_operator_ids = [130101, 130102, 130103]
        # # target_formation_id = 260101
        # # target_operator_ids = [230101, 230102, 230103]
        # # select_result = self._sdk.operator_seat.antiShipMissilesTargetSelect(round_id, attack_formation_id,
        # #                                                               attack_operator_ids, target_formation_id,
        # #                                                               target_operator_ids)
        # # 如果返回select_result为以下结构的dict则为获取成功，如果返回其他结果则为获取失败。为加强程序的稳定性，应对获取失败(非以下结构的dict)以及获取超时做处理
        # # 如果获取成功，select_result结构如下
        # # select_result["result"]  # "false"代表获取失败，"true"代表获取到了结果
        # # select_result["rand_num"]  # 随机数的值
        # # select_result["select_target_ids"]  # 攻击目标的operator_id列表
        # # select_result["error_code"] = "None"  # 错误码
        #
        # # # 发送机动，攻击计划
        # plan_list = []
        #
        # our_kongzhong_ids = battle_state.fetch_our_operator_ids_by_category_id1(const.kongzhongdanwei_id)
        # enemy_shuimian_ids = battle_state.fetch_enemy_operator_ids_by_category_id1(const.shuimiandanwei_id)
        # if our_kongzhong_ids:  # 随机选取一个空中单位发起攻击
        #
        #     our_operator_id = random.sample(our_kongzhong_ids, 1)[0]
        #     # 1，反舰导弹攻击(type 502, 目标:水面单位)  判断是否有反舰导弹能力(asm_attack:反舰导弹攻击值，asm_range:反舰导弹射程，asm_num：反舰导弹数量)
        #     our_operator = battle_state.fetch_operator_by_id(our_operator_id)
        #     # 根据state，获取相应属性的值（类似asm_attack这样的属性，是一个数组，具体算子该值取哪个值要根据state进行取值）
        #     if our_operator.asm_attack and (our_operator.state < 2):  # 先判断算子该属性是否有值,且算子不是死亡
        #         asm_attack = our_operator.asm_attack[our_operator.state]
        #         # asm_range 可以判断射程内再射击，如果不在射程内，射击可能不会发生
        #         # asm_num 弹药数量
        #         if asm_attack > 0:
        #             if enemy_shuimian_ids:
        #                 target_id = random.sample(enemy_shuimian_ids, 1)[0]
        #                 target_operator = battle_state.fetch_operator_by_id(target_id)
        #
        #                 is_formation = 0
        #                 # act_content = {"operator_id":"130302","camp": 1,"seat":101,"act_order":"1","act_list":[],"attack_order":"1","attack_list":[{"act_id":1,"type":504,"routes":[],"fp_operator_id":"","src_id":["130302"],"target_id": ["210402"],"aggressivity": "24","ammunition_num": 1,"rounds": 1,"is_suicide_attack": 0,"support_operator_id": "","land_position": "","land_value": 0}]}
        #                 act_content = {"operator_id": str(our_operator_id), "camp": self._camp_id, "seat": our_operator.seat_id,
        #                                "act_order": "1", "act_list": [],
        #                                "attack_order": "1", "attack_list": [{"act_id": 1, "type": 502, "routes": [], "fp_operator_id": "", "src_id":[str(our_operator_id)], "target_id": [str(target_id)], "aggressivity": str(asm_attack), "ammunition_num": 1, "rounds": battle_state.frame.round, "is_suicide_attack": 0, "support_operator_id": "", "land_position": "", "land_value": 0}]}
        #                 # 每个算子最多调用一次该接口，一次可以设置多个动作，act_list 设置机动动作，attack_list 设置攻击动作
        #                 # print("ai 发送 一个作战计划")
        #                 plan = {"type": 502, "operator_id": our_operator_id, "seat": our_operator.seat_id, "act_order": "1", "is_formation": is_formation, "act_content": act_content}
        #                 plan_list.append(plan)
        #                 # maneuveringAttack = self._sdk.operator_seat.maneuveringAttack(our_operator_id, '1', is_formation, act_content)
        #
        # # print("ai 发送 作战筹划完成")
        # # self._sdk.operator_seat.attack_finished(battle_state.get_time_section_id())

        self._logger.print(self._round, "ai 发送 作战筹划 %s " %(plan_list))

        for plan in plan_list:
            plan_string = '{}: attack: {} \n{}: move: {}'.format(plan['operator_id'], plan['act_content']['attack_list'], plan['operator_id'], plan['act_content']['act_list'])
            self._plan_string += plan_string
            print(plan_string)

        # for plan in plan_list:
        #     print("attack:", plan['operator_id'], plan['act_content']['attack_list'])
        #     print("move:", plan['operator_id'], plan['act_content']['act_list'])

        # 在此时节，调用一次下方接口
        # 每个算子可以加plan_list中加一个plan，每个plan可以有多个机动动作、多个攻击动作
        maneuveringAttack = self._sdk.operator_seat.maneuveringAttack(plan_list)

    def _attack_and_move(self, battle_state):
        """
        行动裁决
        可能会有一些态势更新，不需调用sdk和服务器发送交互
        :param battle_state: 当前战斗态势
        """
        # 在此时节，不需要对服务器进行任何响应
        pass

    def _shore_units_attack(self, battle_state):
        """
        岸基单位裁决
        可能会有一些裁决信息，不需调用sdk和服务器发送交互
        :param battle_state: 当前战斗态势
        """
        # 在此时节，不需要对服务器进行任何响应
        pass

    def _judge_finish(self, battle_state):
        """
        裁决完毕
        裁决完成标志，并包含最新的态势
        :param battle_state: 当前战斗态势
        """
        # 通知服务器收到消息
        # 在此时节，调用一次下方接口
        self._sdk.rulingFinished(battle_state.get_time_section_id())
        pass

    def _airplane_manual_return(self, battle_state):
        """
        手动飞机返航
        :param battle_state: 当前战斗态势
        """
        # 对飞机进行返航操作
        # self._sdk.airplane_return(self, operator_id, position, section_id, return_type):
        # 完成接口

        # 在此时节，在完成飞机返航(上面的飞机返航接口可以调用多次)操作后，调用一次下方飞机返航完成接口
        print("飞机手动返航时节")
        self._sdk.http_post_airplane_return_finished(battle_state.get_time_section_id())

        pass

    def _game_over(self, battle_state):
        """
        整个推演结束
        :param battle_state: 当前战斗态势
        """
        # 得分；格式：数组。数组中内容依次代表：红方夺控分，红方歼敌分，红方剩余兵力分；蓝方夺控分，蓝方歼敌分，蓝方剩余兵力分
        # 净胜分 = 我方总分-敌方总分
        scores = battle_state.frame.score
        self._logger.print(self._round, "红方夺控分：{}".format(scores[0]))
        self._logger.print(self._round, "红方歼敌分：{}".format(scores[1]))
        self._logger.print(self._round, "红方剩余兵力分：{}".format(scores[2]))
        self._logger.print(self._round, "红方净胜分：{}".format((scores[0]+scores[1]+scores[2]) - (scores[3]+scores[4]+scores[5])))
        self._logger.print(self._round, "蓝方夺控分：{}".format(scores[3]))
        self._logger.print(self._round, "蓝方歼敌分：{}".format(scores[4]))
        self._logger.print(self._round, "蓝方剩余兵力分：{}".format(scores[5]))
        self._logger.print(self._round, "蓝方净胜分：{}".format((scores[3]+scores[4]+scores[5]) - (scores[0]+scores[1]+scores[2])))
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        self._logger.print(self._round, now + "：本局比赛结束")
        # self._logger.print(self._round, self._plan_string)
        # self._logger.print(self._round, self.judgement_string)
