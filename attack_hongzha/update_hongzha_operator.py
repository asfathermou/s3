# @author xie yusen
# 更新算子信息

import collections
import pandas as pd
import copy
from pandas import Series, DataFrame
from copy import deepcopy
from rl_env.update_operator import UpdateOperator


class UpdateHongzhaOperater:
    pass
    # """
    # 获取想定初始的算子信息，根据当前态势数据对算子信息进行更新
    # """
    # def __init__(self, scenario,):
    #     # 参数
    #     self.operator_information_original = []
    #     self.operator_ids = []
    #     self.operator_state = collections.defaultdict(int)
    #     self.column_name = ["camp_id", "category_ch_name", "category_id2", "operator_id", "operator_name", "state",
    #                         "antisubmarine", "to_air", "is_blos", "blos_range", "asm_attack", "asm_nature", "asm_range",
    #                         "asm_num", "bomb", "warning_range", "retention_round", "move", "defense", "scout_range",
    #                         "score", "regional_air_defense", "close_air_defense", 'position', 'seat_id', 'is_formation',
    #                         'rad_nature']
    #     self.formation_dict_original = {'src_id': {}, 'asm_nature': {}, 'position': {}, 'seat_id': {}, 'camp_id': {},
    #                                     'rad_nature': {}, 'regional_air_defense': {}}
    #     self.formation_dict = deepcopy(self.formation_dict_original)
    #     self.operator_list = []
    #     self.scenario = scenario
    #     self.df_operator = None
    #     self.df_formation = None
    #     pd.set_option('display.max_columns', None)
    #
    # def get_operator_original_information(self, scenario):
    #     """
    #     获取当前想定游戏刚开始时双方算子的信息
    #     @param scenario: 当前想定信息
    #     @return: 游戏开始时双方算子的信息
    #     """
    #
    #     for operator in scenario.operators:
    #         # 获取水面单位（1）、空中单位（3）、基地（503）
    #         if operator.category_id2 in [102,108,103,104] or operator.category_id2 in [307,305,306]:
    #             operator_feature = [operator.camp_id, operator.category_ch_name, operator.category_id2,
    #                                 operator.operator_id, operator.operator_name, operator.state,
    #                                 operator.antisubmarine, operator.to_air, operator.is_blos,
    #                                 operator.blos_range, operator.asm_attack, operator.asm_nature, operator.asm_range,
    #                                 operator.asm_num, operator.bomb, operator.warning_range, operator.retention_round,
    #                                 operator.move, operator.defense, operator.scout_range, operator.score,
    #                                 operator.regional_air_defense, operator.close_air_defense, operator.position,
    #                                 operator.seat_id, operator.is_formation, operator.rad_nature]
    #
    #             # 添加信息
    #             self.operator_information_original.append(operator_feature)
    #             self.operator_ids.append(operator.operator_id)
    #
    #     for operator in self.operator_ids:
    #         self.operator_state[operator] = 0
    #     df_operator_information_original = DataFrame(self.operator_information_original, columns=self.column_name)
    #     df_operator_information_original['x_position'] = -1
    #     df_operator_information_original['y_position'] = -1
    #     df_operator_information_original['formation_id'] = -1
    #     df_operator_information_original['member'] = -1
    #     # df_operator_information_original['luehai_quyufangkongli'] = -1
    #     # df_operator_information_original['no_luehai_quyufangkongli'] = -1
    #     # df_operator_information_original['gaosu_jinjufangkongli'] = -1
    #     # df_operator_information_original['no_gaosu_jinjufangkongli'] = -1
    #     df_operator_information_original['fangyu_xiuzheng'] = -1
    #     df_operator_information_original['gongji_xiuzheng'] = -1
    #     df_operator_information_original['hongzha_step_3_result'] = -1
    #     df_operator_information_original = df_operator_information_original.set_index('operator_id', drop=False)
    #     return df_operator_information_original
    #
    #
    # def update_operator_state(self, battle_state):
    #     """
    #     更新敌我双方算子的情况，还存活哪些，状态怎么样
    #     @param battle_state: 当前想定信息
    #     @return: 算子的状态
    #     """
    #     judgements = battle_state.data['judgements']
    #     if len(judgements) != 0:
    #         for judgement in judgements:
    #             injured_operators = judgement['judgement_data'][0]['injured_operators']
    #             injured_damage = judgement['judgement_data'][0]['injured_damage']
    #             # print("injured_operators:injured_damage:%s,%s" % (str(injured_operators), str(injured_damage)))
    #             for i in range(len(injured_operators)):
    #                 self.operator_state[injured_operators[i]] += injured_damage[i]
    #     return self.operator_state
    #
    # def operator_df_update_state(self, key):
    #     """
    #     根据算子实时的state对算子信息dataframe中state列的内容进行更新
    #     """
    #     return self.operator_state.get(key, 2)
    #
    # def apply_property_value_select(self, df, column_name):
    #     """
    #     根据算子的状态来选择它对应的属性值
    #     @param df: 算子信息的dataframe
    #     @param column_name: 需要更新的属性列的名称
    #     @return: 更新后的算子信息dataframe
    #     """
    #     for i in df.index:
    #         if type(df.at[i, column_name]) == list:
    #             if len(df.at[i, column_name]) == 0:
    #                 df.at[i, column_name] = 0
    #             else:
    #                 df.at[i, column_name] = df.at[i, column_name][df.at[i, 'state']]
    #         else:
    #             df.at[i, column_name] = 0
    #     return df
    #
    # def update_change_property(self, df, battle_state):
    #     """
    #     对df中根据态势信息battle_state发生变化的属性值进行更新
    #     @param battle_state: 态势信息
    #     @param df: 算子信息dataframe
    #     @param column_name: 列名
    #     @return: 算子信息dataframe
    #     """
    #     df['x_position'] = -1
    #     df['y_position'] = -1
    #     df['is_formation'] = -1
    #     df['formation_id'] = -1
    #     for operator in battle_state.our_operators:
    #         if operator.category_id2 in [102, 108, 103, 104] or operator.category_id2 in [307, 305, 306]:
    #             operator_id = operator.operator_id
    #             df.at[operator_id, 'x_position'] = operator.position[0]
    #             df.at[operator_id, 'y_position'] = operator.position[1]
    #             df.at[operator_id, 'is_formation'] = int(operator.is_formation)
    #             df.at[operator_id, 'formation_id'] = int(operator.formation_id) if hasattr(operator, 'formation_id') else -1
    #     for operator in battle_state.enemy_operators:
    #         if operator.category_id2 in [102, 108, 103, 104] or operator.category_id2 in [307, 305, 306]:
    #             operator_id = operator.operator_id
    #             df.at[operator_id, 'x_position'] = operator.position[0]
    #             df.at[operator_id, 'y_position'] = operator.position[1]
    #             df.at[operator_id, 'is_formation'] = int(operator.is_formation)
    #             df.at[operator_id, 'formation_id'] = int(operator.formation_id) if hasattr(operator,
    #                                                                                        'formation_id') else -1
    #     return df

    # def update_operator_property(self, battle_state, df_operator_information_original):
    #     """
    #     根据当前回合和态势更新算子的属性值
    #     @param df_operator_information_original: 想定的初始算子信息
    #     @param battle_state: 当前想定信息
    #     @return: 当前所有单算子的属性
    #     """
    #     # 根据当前态势更新算子状态
    #     operator_state = self.update_operator_state(battle_state)
    #     # 根据算子状态获（正常，受损，损毁: 0, 1, 2）取算子的属性值
    #     self.df_operator = copy.deepcopy(df_operator_information_original)
    #     # 根据算子id和状态的dict对算子信息df中的state列进行更新
    #     self.df_operator['state'] = self.df_operator['operator_id'].map(self.operator_df_update_state)
    #     # 删除掉状态为2的算子行
    #     self.df_operator = self.df_operator.drop(
    #         self.df_operator[self.df_operator['state'] == 2].index)
    #     # 将有多个值的属性根据算子当前状态取对应的值
    #     # [6, 7, 10, 12, 14, 15, 17, 18, 20]
    #     # "antisubmarine", "to_air", "asm_attack", "asm_range", "bomb", "warning_range", "move", "defense", "score"
    #     self.apply_property_value_select(self.df_operator, 'antisubmarine')
    #     self.apply_property_value_select(self.df_operator, 'to_air')
    #     self.apply_property_value_select(self.df_operator, 'asm_attack')
    #     self.apply_property_value_select(self.df_operator, 'asm_range')
    #     self.apply_property_value_select(self.df_operator, 'bomb')
    #     self.apply_property_value_select(self.df_operator, 'warning_range')
    #     self.apply_property_value_select(self.df_operator, 'move')
    #     self.apply_property_value_select(self.df_operator, 'defense')
    #     # self.apply_property_value_select(self.df_operator, 'score')
    #     self.apply_property_value_select(self.df_operator, 'regional_air_defense')
    #     # self.apply_property_value_select(self.df_operator, 'close_air_defense')
    #
    #     self.update_change_property(self.df_operator, battle_state)
    #
    #     # 将算子id作为dataframe的index索引
    #     # self.df_operator = self.df_operator.set_index('operator_id', drop=False)
    #     return self.df_operator


    # def create_df_formation(self):
    #     self.df_formation = copy.deepcopy(self.df_operator)
    #     df = self.df_formation
    #     for i in df.index:
    #         if i in df.index:
    #             if df.at[i, 'is_formation'] == 1:
    #                 # 获取一行算子
    #                 df_temp = df.loc[i, :]
    #
    #                 # 获取和这个算子相同编队是算子df
    #                 df_formation = df.loc[df['formation_id'] == df.at[i, 'formation_id']]
    #
    #                 # 计算编队的机动范围和反舰导弹攻击范围，都是编队中算子的最小值
    #                 # move = df_formation['move'].min()
    #                 # asm_range = df_formation['asm_range'].min()
    #
    #                 # 合计轰炸力
    #                 asm_attack = 0
    #                 for k in df_formation.index:
    #                     if df_formation.at[k, 'asm_num'] != 0:
    #                         asm_attack += df_formation.at[k, 'asm_attack']
    #
    #                 # 在编队中，算子的侦查范围不变，可以理解为编队的侦查范围是算子的侦查范围的最大值
    #                 # scout_range = df_formation['scout_range'].max()
    #                 # 计算编队的反舰导弹性质
    #                 # 如果发动单位中一半以上拥有掠海能力，则该攻击属于掠海攻击
    #                 # 如果发动单位一半以上拥有高速能力，则该攻击为高速攻击
    #                 # asm_nature: 0普通 1高速 2掠海 3高速+掠海
    #                 # dict_asm_nature = df_formation['asm_nature'].value_counts().to_dict()
    #                 # if ((dict_asm_nature.get(2, 0) + dict_asm_nature.get(3, 0)) / df_formation.shape[0] > 0.5) and ((dict_asm_nature.get(1, 0) + dict_asm_nature.get(3, 0)) / df_formation.shape[0] > 0.5):
    #                 #     asm_nature = 3
    #                 # elif ((dict_asm_nature.get(2, 0) + dict_asm_nature.get(3, 0)) / df_formation.shape[0] > 0.5) and ((dict_asm_nature.get(1, 0) + dict_asm_nature.get(3, 0)) / df_formation.shape[0] <= 0.5):
    #                 #     asm_nature = 2
    #                 # elif ((dict_asm_nature.get(2, 0) + dict_asm_nature.get(3, 0)) / df_formation.shape[0] <= 0.5) and ((dict_asm_nature.get(1, 0) + dict_asm_nature.get(3, 0)) / df_formation.shape[0] > 0.5):
    #                 #     asm_nature = 1
    #                 # else:
    #                 #     asm_nature = 0
    #                 # 计算编队的算子id有哪些
    #
    #                 operator_id_list = df_formation['operator_id'].unique()
    #                 member = ''
    #                 for id in operator_id_list:
    #                     member = member + str(id) + ','
    #                 member = member[:-1]
    #
    #                 formation_id = df_temp['formation_id']
    #                 # df_temp['move'] = move
    #                 # df_temp['asm_range'] = asm_range
    #                 # df_temp['asm_nature'] = asm_nature
    #                 df_temp['operator_id'] = member
    #                 df_temp['asm_attack'] = asm_attack
    #                 # df_temp['scout_range'] = scout_range
    #                 # df_temp['category_id2'] = 8882
    #                 # df_temp['category_ch_name'] = '实时编队2'
    #
    #                 # 将这个编队的单算子行从编队的df中删掉
    #                 # df = df[df['formation_id'] != formation_id]
    #                 # 将编队的这一行数据添加到编队的df中
    #                 # df.loc[formation_id] = df_temp
    #     self.df_formation = df
    #     return self.df_formation

