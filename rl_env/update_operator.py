#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/5/11 17:47
# @Author : ZM
# @File : update_operator.py
# @Desc :

import collections
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import math
from collections import Counter
import copy
from copy import deepcopy
import rl_env.cal_map as cal_map_static


class UpdateOperator:
    """
    获取想定初始的算子信息，根据当前态势数据对算子信息进行更新
    """

    def __init__(self, scenario, ):
        self.operator_information_original = []
        self.operator_ids = []
        self.operator_state = collections.defaultdict(int)
        self.used_asm_num = collections.defaultdict(int)
        self.column_name = ["camp_id", "category_ch_name", "category_id2", "operator_id", "operator_name", "state",
                            "antisubmarine", "to_air", "is_blos", "blos_range", "asm_attack", "asm_nature", "asm_range",
                            "asm_num", "bomb", "warning_range", "retention_round", "move", "defense", "scout_range",
                            "score", "regional_air_defense", "close_air_defense", 'position', 'seat_id', 'is_formation',
                            'rad_nature', 'close_combat']
        self.formation_dict_original = {'src_id': {}, 'asm_nature': {}, 'position': {}, 'seat_id': {}, 'camp_id': {},
                                        'rad_nature': {}, 'regional_air_defense': {}}
        self.formation_dict = deepcopy(self.formation_dict_original)
        self.operator_list = []
        self.scenario = scenario
        self.df_operator = None
        self.df_formation = None
        self.cal_map = None
        self.judgement_string = ""
        pd.set_option('display.max_columns', None)


    def set_env(self, cal_map):
        self.cal_map = cal_map

    def get_operator_original_information(self, scenario):
        """
        获取当前想定游戏刚开始时双方算子的信息
        @param scenario: 当前想定信息
        @return: 游戏开始时双方算子的信息
        """

        for operator in scenario.operators:
            # 获取除机场外的所有算子
            if operator.category_id2 != 501:
                operator_feature = [operator.camp_id, operator.category_ch_name, operator.category_id2,
                                    operator.operator_id, operator.operator_name, operator.state,
                                    operator.antisubmarine, operator.to_air, operator.is_blos,
                                    operator.blos_range, operator.asm_attack, operator.asm_nature, operator.asm_range,
                                    operator.asm_num, operator.bomb, operator.warning_range, operator.retention_round,
                                    operator.move, operator.defense, operator.scout_range, operator.score,
                                    operator.regional_air_defense, operator.close_air_defense, operator.position,
                                    operator.seat_id, operator.is_formation, operator.rad_nature, operator.close_combat]

                self.operator_information_original.append(operator_feature)
                self.operator_ids.append(operator.operator_id)
        for operator in self.operator_ids:
            self.operator_state[operator] = 0
            self.used_asm_num[operator] = 0
        df_operator_information_original = DataFrame(self.operator_information_original, columns=self.column_name)
        df_operator_information_original['x_position'] = -1
        df_operator_information_original['y_position'] = -1
        df_operator_information_original['formation_id'] = -1
        # 编队中成员id
        df_operator_information_original['member'] = -1
        # 反舰导弹攻击中掠海区域防空力
        df_operator_information_original['luehai_quyufangkongli'] = -1
        # 反舰导弹攻击中非掠海区域防空力
        df_operator_information_original['no_luehai_quyufangkongli'] = -1
        # 反舰导弹攻击中高速近距防空力
        df_operator_information_original['gaosu_jinjufangkongli'] = -1
        # 反舰导弹攻击中非高速近距防空力
        df_operator_information_original['no_gaosu_jinjufangkongli'] = -1
        # 反舰导弹攻击中防御修正值
        df_operator_information_original['fangyu_xiuzheng'] = -1
        # 反舰导弹攻击中攻击修正值
        df_operator_information_original['gongji_xiuzheng'] = -1
        # 反舰导弹攻击中裁决规则第5步计算的最终点数
        df_operator_information_original['fanjiandaodan_step_5_result'] = 0.0
        df_operator_information_original['position_str'] = ""
        # 反舰导弹攻击中进行攻击方防御方遍历计算最优攻击方案时用于临时记录在假设攻击情况下算子的state状态
        df_operator_information_original['state_fanjian_assume'] = 0
        # 算子在反舰导弹攻击中能攻击的地方算子id列表
        df_operator_information_original['asm_attack_id'] = ""

        # 将算子的id设为df的index
        df_operator_information_original = df_operator_information_original.set_index('operator_id', drop=False)
        return df_operator_information_original

    def update_operator_state(self, battle_state):
        """
        更新敌我双方算子的情况，还存活哪些，状态怎么样
        @param battle_state: 当前想定信息
        @return: 算子的状态
        """
        judgements = battle_state.data['judgements']
        if len(judgements) != 0:
            for judgement in judgements:
                for judge_data in judgement['judgement_data']:
                    injured_operators = judge_data['injured_operators']
                    injured_damage = judge_data['injured_damage']
                    src = judge_data['src']
                    judgement_description = judge_data['judgement_description']
                    print("------injured_operators:injured_damage:%s,%s" % (str(injured_operators), str(injured_damage)))
                    print(judgement_description)
                    if judgement_description != []:
                        self.judgement_string += str(judgement_description)
                    # 如果有裁决信息，算子的损伤加上受损的点数。如果是反舰导弹，攻击方的反舰导弹数减1
                    for i in range(len(injured_operators)):
                        self.operator_state[injured_operators[i]] += injured_damage[i]
                        #如果是反舰导弹攻击，每一个发起攻击的算子的反舰导弹子弹数减1
                        if '反舰导弹' in judgement_description[i]:
                            for j in src:
                                self.used_asm_num[j] += 1
                            # self.df_operator.at[src[i], 'asm_num'] -= 1

        return self.operator_state

    def operator_df_update_state(self, key):
        """
        根据算子实时的state对算子信息dataframe中state列的内容进行更新
        """
        return self.operator_state.get(key, 2)

    def apply_property_value_select(self, df, column_name):
        """
        根据算子的状态来选择它对应的属性值
        @param df: 算子信息的dataframe
        @param column_name: 需要更新的属性列的名称
        @return: 更新后的算子信息dataframe
        """
        for i in df.index:
            if type(df.at[i, column_name]) == list:
                if len(df.at[i, column_name]) == 0:
                    df.at[i, column_name] = 0
                else:
                    df.at[i, column_name] = df.at[i, column_name][df.at[i, 'state']]
            else:
                df.at[i, column_name] = 0
        return df

    def update_change_property(self, df, battle_state):
        """
        对df中根据态势信息battle_state发生变化的属性值进行更新
        @param battle_state: 态势信息
        @param df: 算子信息dataframe
        @param column_name: 列名
        @return: 算子信息dataframe
        """
        df['x_position'] = -1
        df['y_position'] = -1
        df['is_formation'] = -1
        df['formation_id'] = -1
        for operator in battle_state.our_operators:
            if operator.category_id2 != 501:
                operator_id = operator.operator_id
                df.at[operator_id, 'x_position'] = operator.position[0]
                df.at[operator_id, 'y_position'] = operator.position[1]
                df.at[operator_id, 'position'] = [operator.position[0], operator.position[1]]
                df.at[operator_id, 'position_str'] = str(operator.position[0]) + "," + str(operator.position[1])
                df.at[operator_id, 'is_formation'] = int(operator.is_formation)
                df.at[operator_id, 'formation_id'] = int(operator.formation_id) if hasattr(operator,
                                                                                           'formation_id') else -1
        for operator in battle_state.enemy_operators:
            if operator.category_id2 != 501:
                operator_id = operator.operator_id
                df.at[operator_id, 'x_position'] = operator.position[0]
                df.at[operator_id, 'y_position'] = operator.position[1]
                df.at[operator_id, 'position'] = [operator.position[0], operator.position[1]]
                df.at[operator_id, 'position_str'] = str(operator.position[0]) + "," + str(operator.position[1])
                df.at[operator_id, 'is_formation'] = int(operator.is_formation)
                df.at[operator_id, 'formation_id'] = int(operator.formation_id) if hasattr(operator,
                                                                                           'formation_id') else -1
        return df

    def update_operator_property(self, battle_state, df_operator_information_original):
        """
        根据当前回合和态势更新算子的属性值
        @param df_operator_information_original: 想定的初始算子信息
        @param battle_state: 当前想定信息
        @return: 当前所有单算子的属性
        """
        # 根据当前态势更新算子状态
        operator_state = self.update_operator_state(battle_state)
        # 根据算子状态获（正常，受损，损毁: 0, 1, 2）取算子的属性值
        self.df_operator = copy.deepcopy(df_operator_information_original)
        # 根据算子id和状态的dict对算子信息df中的state列进行更新
        self.df_operator['state'] = self.df_operator['operator_id'].map(self.operator_df_update_state)
        self.df_operator['state_fanjian_assume'] = self.df_operator['operator_id'].map(self.operator_df_update_state)
        # 删除掉状态为2的算子行
        self.df_operator = self.df_operator.drop(
            self.df_operator[self.df_operator['state'] == 2].index)
        # 将有多个值的属性根据算子当前状态取对应的值
        # [6, 7, 10, 12, 14, 15, 17, 18, 20]
        # "antisubmarine", "to_air", "asm_attack", "asm_range", "bomb", "warning_range", "move", "defense", "score"
        self.apply_property_value_select(self.df_operator, 'antisubmarine')
        self.apply_property_value_select(self.df_operator, 'to_air')
        self.apply_property_value_select(self.df_operator, 'asm_attack')
        self.apply_property_value_select(self.df_operator, 'asm_range')
        self.apply_property_value_select(self.df_operator, 'bomb')
        self.apply_property_value_select(self.df_operator, 'warning_range')
        self.apply_property_value_select(self.df_operator, 'move')
        self.apply_property_value_select(self.df_operator, 'defense')
        # self.apply_property_value_select(self.df_operator, 'score')
        self.apply_property_value_select(self.df_operator, 'regional_air_defense')
        self.apply_property_value_select(self.df_operator, 'close_air_defense')
        self.apply_property_value_select(self.df_operator, 'close_combat')
        self.update_asm_num(self.df_operator)

        self.update_change_property(self.df_operator, battle_state)

        # 将算子id作为dataframe的index索引
        # self.df_operator = self.df_operator.set_index('operator_id', drop=False)
        return self.df_operator

    def update_asm_num(self, df_operator):
        """
        根据裁决信息已经发起成功的反舰导弹攻击来对攻击方的反舰导弹个数进行更新
        """
        for operator in df_operator.index:
            df_operator.at[operator, 'asm_num'] -= self.used_asm_num[operator]

    def create_df_formation(self):
        """
        如果存在编队，则按编队的方式重新组织敌我算子数据，（因为攻击中是以编队为单位发起攻击），并更新编队的属性值

        """
        self.df_formation = copy.deepcopy(self.df_operator)
        df = self.df_formation
        for i in df.index:
            if i in df.index:
                if df.at[i, 'is_formation'] == 1:
                    # 获取一行算子
                    df_temp = df.loc[i, :]
                    # 获取和这个算子相同编队是算子df
                    df_formation = df.loc[df['formation_id'] == df.at[i, 'formation_id']]
                    # 计算编队的机动范围和反舰导弹攻击范围，都是编队中算子的最小值
                    move = df_formation['move'].min()
                    asm_range = df_formation['asm_range'].min()
                    # 编队的子弹数是所有单算子的子弹数的总和
                    asm_num = df_formation['asm_num'].sum()
                    # 编队的攻击力是所有还有攻击次数的算子的攻击力的和
                    # asm_attack = df_formation['asm_attack'].sum()
                    asm_attack = 0
                    close_combat = 0
                    for k in df_formation.index:
                        if df_formation.at[k, 'asm_num'] != 0:
                            asm_attack += df_formation.at[k, 'asm_attack']
                            close_combat += df_formation.at[k, 'close_combat']
                    # 在编队中，算子的侦查范围不变，可以理解为编队的侦查范围是算子的侦查范围的最大值
                    scout_range = df_formation['scout_range'].max()
                    # 计算编队的反舰导弹性质
                    # 如果发动单位中一半以上拥有掠海能力，则该攻击属于掠海攻击
                    # 如果发动单位一半以上拥有高速能力，则该攻击为高速攻击
                    # asm_nature: 0普通 1高速 2掠海 3高速+掠海
                    dict_asm_nature = df_formation['asm_nature'].value_counts().to_dict()
                    if ((dict_asm_nature.get(2, 0) + dict_asm_nature.get(3, 0)) / df_formation.shape[0] > 0.5) and (
                            (dict_asm_nature.get(1, 0) + dict_asm_nature.get(3, 0)) / df_formation.shape[0] > 0.5):
                        asm_nature = 3
                    elif ((dict_asm_nature.get(2, 0) + dict_asm_nature.get(3, 0)) / df_formation.shape[0] > 0.5) and (
                            (dict_asm_nature.get(1, 0) + dict_asm_nature.get(3, 0)) / df_formation.shape[0] <= 0.5):
                        asm_nature = 2
                    elif ((dict_asm_nature.get(2, 0) + dict_asm_nature.get(3, 0)) / df_formation.shape[0] <= 0.5) and (
                            (dict_asm_nature.get(1, 0) + dict_asm_nature.get(3, 0)) / df_formation.shape[0] > 0.5):
                        asm_nature = 1
                    else:
                        asm_nature = 0
                    # 计算编队的算子id有哪些
                    operator_id_list = df_formation['operator_id'].unique()
                    member = ''
                    for id1 in operator_id_list:
                        member = member + str(id1) + ','
                    member = member[:-1]
                    formation_id = df_temp['formation_id']
                    df_temp['move'] = move
                    df_temp['asm_range'] = asm_range
                    df_temp['asm_nature'] = asm_nature
                    df_temp['operator_id'] = member
                    df_temp['asm_attack'] = asm_attack
                    df_temp['asm_num'] = asm_num
                    df_temp['close_combat'] = close_combat
                    df_temp['scout_range'] = scout_range
                    df_temp['category_id2'] = 888
                    df_temp['category_ch_name'] = '实时编队'

                    # 将这个编队的单算子行从编队的df中删掉
                    df = df[df['formation_id'] != formation_id]
                    # 将编队的这一行数据添加到编队的df中
                    df.loc[formation_id] = df_temp
        self.df_formation = df
        self.cal_attack_ids()
        return self.df_formation

    def cal_attack_ids(self):
        """
        计算算子在反舰导弹攻击中能攻击的地方算子id
        """
        df_formation_target = copy.deepcopy(self.df_formation)
        for operator in self.df_formation.index:
            attack_position_list = []
            attack_id_list = []
            attack_id_str = ''
            row = self.df_formation.at[operator, 'x_position']
            col = self.df_formation.at[operator, 'y_position']
            # 反舰导弹攻击范围
            asm_radius = self.df_formation.at[operator, 'asm_range']
            if row != -1 and col != -1 and asm_radius >= 0:
                attack_map = self.cal_map.get_radius(row, col, asm_radius)
                attack_position = attack_map.nonzero()
                for z in range(len(attack_position[0])):
                    attack_position_list.append([attack_position[0][z], attack_position[1][z]])
            else:
                attack_position_list = []
            for operator_id in df_formation_target.index:
                target_position = [df_formation_target.at[operator_id, 'x_position'], df_formation_target.at[operator_id, 'y_position']]
                target_camp_id = df_formation_target.at[operator_id, 'camp_id']
                target_position_str = df_formation_target.at[operator_id, 'position_str']
                if target_position in attack_position_list and target_camp_id != self.df_formation.at[operator, 'camp_id']:
                    attack_id_list.append(operator_id)
            for i in attack_id_list:
                attack_id_str += '{},'.format(i)
            attack_id_str = attack_id_str[:-1]

            # attack_id_list = ','.join(str(attack_id_list))
            self.df_formation.at[operator, 'asm_attack_id'] = attack_id_str
            # self.df_formation.at[operator, 'see_and_asm_attack_id'] = see_and_attack_str

    def get_judgement_string(self):
        return self.judgement_string



    # def cal_formation_and_operator_property(self, battle_state):
    #     """
    #     对编队的算子进行聚合，并计算编队的属性值，同时计算单算子对应的属性值
    #     @param df_operator: 根据当前态势更新的算子属性值
    #     @param battle_state: 当前的态势数据
    #     @return: 算子信息
    #     """
    #     # self.df_operator = df_operator
    #     self.formation_dict = deepcopy(self.formation_dict_original)
    #     for operator in battle_state.our_operators:
    #         self.get_operator_information(operator, df_operator)
    #     for operator in battle_state.enemy_operators:
    #         self.get_operator_information(operator, df_operator)
    #
    #     formation_dict_1 = copy.deepcopy(self.formation_dict)
    #     self.cal_asm_nature(self.formation_dict)
    #     self.formation_dict_transform(self.formation_dict, self.operator_list)
    #     self.cal_quyufangkongli(battle_state)
    #
    #     print('aa')
    #     return self.operator_list
    #
    # def get_operator_information(self, operator, df_operator):
    #     if operator.category_id2 != 501:
    #         # 如果不是编队，则获取单算子相关属性
    #         if not operator.is_formation:
    #             operator_value = {'formation_id': 0, 'src_id': operator.operator_id, 'asm_nature': operator.asm_nature,
    #                               'position': operator.position, 'seat_id': operator.seat_id,
    #                               'camp_id': operator.camp_id, 'rad_nature': operator.rad_nature,
    #                               'regional_air_defense': df_operator.at[operator.operator_id, 'regional_air_defense']}
    #             self.operator_list.append(operator_value)
    #         # 如果是编队，则把在一个编队中的算子id放到一个list中
    #         if operator.is_formation:
    #             self.formation_dict['src_id'].setdefault(operator.formation_id, []).append(operator.operator_id)
    #             self.formation_dict['asm_nature'].setdefault(operator.formation_id, []).append(operator.asm_nature)
    #             self.formation_dict['position'].setdefault(operator.formation_id, []).append(operator.position)
    #             self.formation_dict['seat_id'].setdefault(operator.formation_id, []).append(operator.seat_id)
    #             self.formation_dict['camp_id'].setdefault(operator.formation_id, []).append(operator.camp_id)
    #             self.formation_dict['rad_nature'].setdefault(operator.formation_id, []).append(operator.rad_nature)
    #             self.formation_dict['regional_air_defense'].setdefault(operator.formation_id, []).append(
    #                 df_operator.at[operator.operator_id, 'regional_air_defense'])
    #
    # def cal_asm_nature(self, formation_dict):
    #     """
    #     计算编队的反舰导弹攻击属性
    #     如果发动单位中一半以上拥有掠海能力，则该攻击属于掠海攻击
    #     如果发动单位一半以上拥有高速能力，则该攻击为高速攻击
    #     asm_nature: 0普通 1高速 2掠海 3高速+掠海
    #     @param formation_dict:
    #     @return: 编队的攻击属性
    #     """
    #     for k, v in formation_dict['asm_nature'].items():
    #         d = dict(Counter(v))
    #         if ((d.get(1, 0) + d.get(3, 0)) / len(v) > 0.5) and ((d.get(2, 0) + d.get(3, 0)) / len(v) > 0.5):
    #             formation_dict['asm_nature'][k] = 3
    #         elif ((d.get(1, 0) + d.get(3, 0)) / len(v) > 0.5) and ((d.get(2, 0) + d.get(3, 0)) / len(v) <= 0.5):
    #             formation_dict['asm_nature'][k] = 1
    #         elif ((d.get(1, 0) + d.get(3, 0)) / len(v) <= 0.5) and ((d.get(2, 0) + d.get(3, 0)) / len(v) > 0.5):
    #             formation_dict['asm_nature'][k] = 2
    #         else:
    #             formation_dict['asm_nature'][k] = 0
    #     return formation_dict
    #
    # def formation_dict_transform(self, formation_dict, operator_list):
    #     """
    #     对编队的格式进行转换
    #      @param formation_dict: 编队dict
    #     @param operator_list: 算子列表
    #     @return: 包含编队信息的算子列表
    #     """
    #     for k, v in formation_dict['asm_nature'].items():
    #         temp_dict = {}
    #         temp_dict['formation_id'] = k
    #         temp_dict['src_id'] = formation_dict['src_id'][k]
    #         temp_dict['asm_nature'] = formation_dict['asm_nature'][k]
    #         temp_dict['position'] = formation_dict['position'][k]
    #         temp_dict['seat_id'] = formation_dict['seat_id'][k]
    #         temp_dict['camp_id'] = formation_dict['camp_id'][k]
    #         temp_dict['rad_nature'] = formation_dict['rad_nature'][k]
    #         temp_dict['regional_air_defense'] = formation_dict['regional_air_defense'][k]
    #         operator_list.append(temp_dict)
    #     return operator_list

    # def cal_quyufangkongli(self, battle_state):
    #     """
    #     计算目标六角格防御方所有单位区域防空力
    #     @param battle_state: 当前态势数据
    #     @param scenario: 当前想定数据
    #     @return:
    #     """
    #     df_shuimian = self.df_operator.loc[(100 < self.df_operator['category_id2']) & (self.df_operator['category_id2'] < 200)]
    #     print("aa")
