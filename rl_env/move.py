#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/5/12 17:16
# @Author : ZM
# @File : move.py
# @Desc :


#from entities.hexagon.graph import Graph
import numpy as np


class Move:
    def __init__(self, sdk):
        self._graph = None
        self._sdk = sdk

    def set_env(self, graph):
        self._graph = graph

    def move_not_see_enemy(self, camp_id, operator_information_original):
        # 测试阶段：当看不见对方船的时候，随机选一个最近的对方的船作为终点，产生最短路径，然后根据机动值确定终点。
        # 实际阶段：当看不见对方船的时候，根据初始想定数据里敌方的区域防空力，区域防空性质，近距防空值，分值等计算防御力最弱的船，产生最短路径, 输入参数也要换，应该换成实时的算子信息，不是初始的算子信息
        camp_id = str(camp_id)
        df = operator_information_original
        df1 = df.loc[(df['camp_id'] == camp_id) & (df['category_id2'] < 300)]
        df2 = df.loc[(df['camp_id'] != camp_id) & (df['category_id2'] < 300)]
        min_distance = 10000
        min_id1 = 0
        min_id2 = 0
        for i1, row1 in df1.iterrows():
            for i2, row2 in df2.iterrows():
                distance = self._graph.get_two_hexagon_distance(df1.at[i1, 'position'], df2.at[i2, 'position'])
                if distance < min_distance:
                    min_distance = distance
                    min_id1 = i1
                    min_id2 = i2
        print(min_id1, min_id2, min_distance)
        move_path = self._graph.get_path(df1.at[min_id1, 'position'], df2.at[min_id2, 'position'])
        p1_path_list = []
        p2_path_list = []
        a = int(len(move_path) / 2)
        for i in range(a):
            p1_path_list.append('{},{}'.format(move_path[i].row, move_path[i].col))
            p2_path_list.append(
                '{},{}'.format(move_path[len(move_path) - i - 1].row, move_path[len(move_path) - i - 1].col))

        print(min_id1, min_id2, min_distance)
        return min_id1, min_id2, min_distance

    def move_to_mid_point(self, df_formation, camp_id):
        camp_id = str(camp_id)
        df = df_formation
        # df_boat = df.loc[(df['category_id2'] < 300)]
        # x_list = []
        # y_list = []
        # for i in df_boat.index:
        #     x_list.append(df_boat.at[i, 'position'][0])
        #     y_list.append(df_boat.at[i, 'position'][1])
        # x_list = list(set(x_list))
        # y_list = list(set(y_list))
        # x_list_mean = int(np.mean(x_list))
        # y_list_mean = int(np.mean(y_list))
        # self.create_path(camp_id, operator_information_original, [x_list_mean, y_list_mean])
        self.create_path(camp_id, df_formation, [10, 10])
        # return x_list_mean, y_list_mean

    def create_path(self, camp_id, df_formation, target_position):
        camp_id = str(camp_id)

        if camp_id == '1' or camp_id == '2':
        # df = operator_list
        # df1 = df.loc[(df['camp_id'] == camp_id) & (df['category_id2'] < 300)]
        # plan_list = []
        # for i1, row1 in df1.iterrows():
        #     move_path = self._graph.get_path(df1.at[i1, 'position'], target_position)
        #     # 去掉当前起点位置
        #     move_path = move_path[1:]
        #     p1_path_list = []
        #     p2_path_list = []
        #     for j in range(len(move_path)):
        #         p1_path_list.append('{},{}'.format(move_path[j].row, move_path[j].col))
        #
        #     act_content = {"operator_id": str(df1.at[i1, 'operator_id']), "camp": camp_id,
        #                    "seat": int(df1.at[i1, 'seat_id']),
        #                    "act_order": "1",
        #                    "act_list": [{"act_id": 1, "type": 405, "routes": p1_path_list,
        #                                  "fp_operator_id": ""}],
        #                    "attack_order": "1", "attack_list": []}
        #     print(act_content)
        #
        #     plan = {"type": 502, "operator_id": int(df1.at[i1, 'operator_id']), "seat": int(df1.at[i1, 'seat_id']), "act_order": "1",
        #             "is_formation": int(df1.at[i1, 'is_formation']), "act_content": act_content}
        #    # print(type(df1.at[i1, 'operator_id']))
        #     plan_list.append(plan)
            plan_list_1 = []
            plan_list_2 = []
            for i in df_formation.index:
                is_formation = df_formation.at[i, 'is_formation']
                if is_formation == 1:
                    start_position = [df_formation.at[i, 'x_position'], df_formation.at[i, 'y_position']]
                    move_path = self._graph.get_path(start_position, target_position)
                    move_path = move_path[1:]
                    path_list = []
                    for j in range(len(move_path)):
                        path_list.append('{},{}'.format(move_path[j].row, move_path[j].col))
                    operator_id = df_formation.at[i, 'operator_id']
                    seat_id = df_formation.at[i, 'seat_id']
                    is_formation = df_formation.at[i, 'is_formation']
                    camp_id = df_formation.at[i, 'camp_id']
                    formation_id = i


                    act_content = {"operator_id": operator_id, "camp": camp_id, "seat": seat_id,
                                   "act_order": "1",
                                   "act_list": [{"act_id": 1, "type": 405, "routes": path_list,
                                                 "fp_operator_id": ""}],
                                   "attack_order": "1", "attack_list": []}
                    plan = {"type": 502, "operator_id": formation_id, "seat": seat_id,
                            "act_order": "1",
                            "is_formation": is_formation, "act_content": act_content}
                    if camp_id == '1':
                        plan_list_1.append(plan)
                    if camp_id == '2':
                        plan_list_2.append(plan)




            # for operator in operator_list:
            #     if operator["formation_id"] != 0:
            #         formation_id = operator['formation_id']
            #         move_path = self._graph.get_path(operator["position"][0], target_position)
            #         move_path = move_path[1:]
            #         p1_path_list = []
            #         for j in range(len(move_path)):
            #             p1_path_list.append('{},{}'.format(move_path[j].row, move_path[j].col))
            #             operator_id = ''
            #         for i in operator["src_id"]:
            #             operator_id += str(i)
            #             operator_id += ','
            #         operator_id = operator_id[:-1]
            #
            #         act_content = {"operator_id": operator_id, "camp": camp_id, "seat": operator['seat_id'][0],
            #                        "act_order": "1",
            #                        "act_list": [{"act_id": 1, "type": 405, "routes": p1_path_list,
            #                                      "fp_operator_id": ""}],
            #                        "attack_order": "1", "attack_list": []}
            #         plan = {"type": 502, "operator_id": formation_id, "seat": operator['seat_id'][0],
            #                 "act_order": "1",
            #                 "is_formation": 1, "act_content": act_content}
            #         if operator['camp_id'][0] == '1':
            #             plan_list_1.append(plan)
            #         if operator['camp_id'][0] == '2':
            #             plan_list_2.append(plan)

        if camp_id == '1':
            plan_list = plan_list_1
        if camp_id == '2':
            plan_list = plan_list_2
        # maneuvering_attack = self._sdk.operator_seat.maneuveringAttack(plan_list)

        print(plan_list)

    def no_move(self):
        """
        不做任何机动和攻击，只是在这个环节发送一个指令给引擎，避免进行不下去
        """
        plan_list = []
        maneuvering_attack = self._sdk.operator_seat.maneuveringAttack(plan_list)
