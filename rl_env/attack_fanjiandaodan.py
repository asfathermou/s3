#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/5/8 15:13
# @Author : ZM
# @File : attack_fanjiandaodan.py
# @Desc :

from collections import Counter
import copy
import itertools
import numpy as np
import pandas as pd
import math
import rl_env.judge_table_transform as judge_table
import rl_env.judge_table_data as judge_data
import rl_env.cal_map as cal_map_static


class AttackFanjiandaodan:
    """
    反舰导弹攻击
    """

    def __init__(self, scenario, camp_id, sdk):
        # 纪录每一个单算子的属性值，属性值实时更新
        self.df_operator = None
        # 纪录按编队进行编组的属性值，只有部分属性是更新有用的，使用时参考update_operator.create_df_formation()中更新的属性值
        self.df_formation = None
        self.cal_map = None
        self.round = None
        self.graph = None
        self.scenario = scenario
        self.camp_id = camp_id
        self.sdk = sdk
        self.xianzhishuiyu_list = []
        self.land_list = []
        self.our_yujing_list = []
        # 反舰导弹防御修正值列表
        self.fanjiandaodan_xiuzheng_defense = [-4, -2, 0, 2, 4]
        # 反舰导弹攻击修正值列表
        self.fanjiandaodan_xiuzheng_attack = [-4, -3, -2, -1, 0, 1, 2, 3]
        # 反舰导弹掷骰子转期望裁决表
        self.fanjiandaodan_defense_table, self.fanjiandaodan_attack_table = judge_table.main_judge_table(
            self.fanjiandaodan_xiuzheng_defense, self.fanjiandaodan_xiuzheng_attack)

    def set_env(self, scenario, update_operator_property, df_formation, camp_id, cal_map, round, graph):
        self.scenario = scenario
        self.df_operator = update_operator_property
        self.df_formation = df_formation
        self.camp_id = str(camp_id)
        self.cal_map = cal_map
        self.round = round
        self.graph = graph

    def terrain_position_list(self):
        """
        计算在想定中，哪些坐标属于哪种地形
        地形： 1:深海;2:浅海;3:陆地;4:海岸;5:岛屿;6:限制水域
        地形字段: terrain ，str类型 ‘3’
        坐标字段：coordinate， str类型 ‘1,3’
        """

        for cell in self.scenario.war_map.cells:
            if cell.terrain == '6':
                self.xianzhishuiyu_list.append(cell.coordinate)
            if cell.terrain == '3':
                self.land_list.append(cell.coordinate)

    def cal_defenser_attribute(self):
        """
        计算反舰导弹攻击中防御方算子的各种属性
        @return:
        """
        # 计算限制水域等坐标
        self.terrain_position_list()
        df_shuimian_our = self.df_operator.loc[
            (100 < self.df_operator['category_id2']) & (self.df_operator['category_id2'] < 200) & (
                    self.df_operator['camp_id'] == self.camp_id)]
        df_shuimian_enemy = self.df_operator.loc[
            (100 < self.df_operator['category_id2']) & (self.df_operator['category_id2'] < 200) & (
                    self.df_operator['camp_id'] != self.camp_id)]
        # df_shuimian_enemy = self.df_operator.loc[(100 < self.df_operator['category_id2']) & (self.df_operator['category_id2'] < 200)]

        # 2. a. 合计目标六角格防御方所有单位区域防空力（ 对水面舰艇的近距战斗跳过该步骤）
        # 近距战斗待添加
        for i in df_shuimian_enemy.index:
            luehai_quyufangkongli = 0
            no_luehai_quyufangkongli = 0
            gaosu_jinjufangkongli = 0
            no_gaosu_jinjufangkongli = 0
            fangyu_xiuzheng = 0
            gongji_xiuzheng = 0

            position_str = '{},{}'.format(df_shuimian_enemy.at[i, 'x_position'], df_shuimian_enemy.at[i, 'y_position'])
            # 2.a(1) 如果目标在限制水域六角格， 区域防空力为 0
            if position_str in self.xianzhishuiyu_list:
                self.df_operator.at[i, 'luehai_quyufangkongli'] = 0
                self.df_operator.at[i, 'no_luehai_quyufangkongli'] = 0

            # 2.a(2) 如果该攻击是【 掠海】 攻击， 区域防空力=防御方（ 拥有宙斯盾的单位区域防空力之和）乘以 2 加上（ 不拥有宙斯盾单位的区域防空力之和） ；
            # 2.a(3) 如果该攻击不是【 掠海】 攻击， 区域防空力=防御方（ 拥有宙斯盾的单位区域防空力之和） 乘以 3 加上（ 不拥有宙斯盾单位的区域防空力之和） 乘以 2；
            # 0：普通  # 1：宙斯盾  # 2：反导能力  # 3：宙斯盾+反导  # 只对type1=1生效
            df_same_position = df_shuimian_enemy.loc[
                (df_shuimian_enemy['x_position'] == df_shuimian_enemy.at[i, 'x_position']) & (
                        df_shuimian_enemy['y_position'] == df_shuimian_enemy.at[i, 'y_position'])]
            for j in df_same_position.index:
                if df_same_position.at[j, 'rad_nature'] == 1 or df_same_position.at[j, 'rad_nature'] == 3:
                    luehai_quyufangkongli += df_same_position.at[j, 'regional_air_defense'] * 2
                    no_luehai_quyufangkongli += df_same_position.at[j, 'regional_air_defense'] * 3
                else:
                    luehai_quyufangkongli += df_same_position.at[j, 'regional_air_defense']
                    no_luehai_quyufangkongli += df_same_position.at[j, 'regional_air_defense'] * 2
            self.df_operator.at[i, 'luehai_quyufangkongli'] = luehai_quyufangkongli
            self.df_operator.at[i, 'no_luehai_quyufangkongli'] = no_luehai_quyufangkongli

            # 2.a(4) 如果攻击距离大于等于 2 格， 需加上途经六角格防御方水面单位区域防空力 ????
            # 待添加

            # 2.b 合计目标单位近距防空力
            # 2.b(1) 如果目标为编队， 加上目标下方单位近距防空值；???? （ 同一单位的近距防空力在同一次战斗中只可以使用一次， 所以当编队
            # 中目标下方单位也成为被攻击目标时， 不可以重复合计该单位的近距防空力） 待添加
            no_gaosu_jinjufangkongli = df_shuimian_enemy.at[i, 'close_air_defense']
            # 2.b(2) 如果目标在己方港口， 加上港口近距防空值；游戏比赛的时候没有港口，暂不需要
            # 2.b(3) 如果是【 高速】 攻击， 以上两个近距防空值都要减半（ 但减半后值至少为 1， 尾数舍去）；区域防空力+近距防空力， 得出最终值
            gaosu_jinjufangkongli = int(no_gaosu_jinjufangkongli / 2) if int(no_gaosu_jinjufangkongli / 2) >= 1 else 1
            self.df_operator.at[i, 'no_gaosu_jinjufangkongli'] = no_gaosu_jinjufangkongli
            self.df_operator.at[i, 'gaosu_jinjufangkongli'] = gaosu_jinjufangkongli

            # 3. 计算防御修正值
            # 掷骰子并进行以下修正：
            # 3.a 目标属于特混编队 [+2]
            # 3.b 目标既不属于特混编队又不属于任务任务编组 [-2]
            # 水面单位的数量为 2-3 个的编队被视为任务编组， 水面单位的数量为大于等于 4 个的编队被视为特混编队
            formation_id = df_shuimian_enemy.at[i, 'formation_id']
            if formation_id == -1:
                # 单算子
                fangyu_xiuzheng += -2
            else:
                formation_member_num = df_shuimian_enemy['formation_id'].value_counts()[formation_id]

                # formation_member_num = df_shuimian_enemy['formation_id'].value_counts[formation_id]
                if formation_member_num >= 4:
                    fangyu_xiuzheng += 2
            # 3.c 防御方所在六角格有其战斗空中巡逻且包含预警机或预警指挥机[+2] , 预警范围需要实时计算， 待添加
            if df_shuimian_enemy.at[i, 'position'] in self.our_yujing_list:
                #  if 有战斗空中巡逻机：
                # 待添加
                fangyu_xiuzheng += 2
            # 3.d 攻击方至少有一个电子战机单位参战时 [-2]. 现在游戏暂时不用考虑，现在飞机不能编队，所以不会有电子战机参战

            self.df_operator.at[i, 'fangyu_xiuzheng'] = fangyu_xiuzheng

            # 4. 根据第2步防空力和第3步点数， 对照战斗结果裁决表[防御栏]得出防御战斗结果值；

            # 5. 攻击修正值计算：
            # 5.a 攻击方是否使用战术支援 用一个[+1]， 最多用 3 个
            # 待添加
            # 5.b 目标在港口或限制水域六角格 [-3]
            if position_str in self.xianzhishuiyu_list:
                gongji_xiuzheng += -3
            # 5.c 目标六角格内存在防御方宙斯盾舰时 [-1]
            flag_rad_nature = 0
            for k in df_same_position.index:
                if df_same_position.at[k, 'rad_nature'] == 1 or df_same_position.at[k, 'rad_nature'] == 3:
                    flag_rad_nature = 1
            if flag_rad_nature == 1:
                gongji_xiuzheng += -1
            self.df_operator.at[i, 'gongji_xiuzheng'] = gongji_xiuzheng

    # self.df_operator

    def cal_step_5_result(self, attack_asm_nature, defense_operator_id, jinzhan_attack_flag, in_path_operator_list):
        """
        计算裁决规则第5步的点数
        @param attack_asm_nature: 攻击方的总攻击力
        @param defense_operator_id: 防御方算子id
        @return: 反舰导弹裁决规则第5步的点数
        """
        # asm_nature: 0普通 1高速 2掠海 3高速+掠海
        defense_fangkongli = 0
        k = defense_operator_id
        if attack_asm_nature == 0:
            if jinzhan_attack_flag == 0:
                defense_fangkongli += self.df_operator.at[k, 'no_luehai_quyufangkongli']
                #  如果攻击距离大于等于 2 格，需加上途经六角格防御方水面单位区域防空力， in_path_operator_list 表示沿途六角格的算子id列表
                defense_fangkongli += int(self.df_operator[['no_luehai_quyufangkongli']][self.df_operator.index.isin(in_path_operator_list)].sum())
                defense_fangkongli += self.df_operator.at[k, 'no_gaosu_jinjufangkongli']
            elif jinzhan_attack_flag == 1:
                # 对水面舰艇的近距战斗跳过区域防空力计算步骤
                defense_fangkongli += self.df_operator.at[k, 'no_gaosu_jinjufangkongli']

        elif attack_asm_nature == 1:
            if jinzhan_attack_flag == 0:
                defense_fangkongli += self.df_operator.at[k, 'no_luehai_quyufangkongli']
                defense_fangkongli += int(self.df_operator[['no_luehai_quyufangkongli']][self.df_operator.index.isin(in_path_operator_list)].sum())
                defense_fangkongli += self.df_operator.at[k, 'gaosu_jinjufangkongli']
            elif jinzhan_attack_flag == 1:
                defense_fangkongli += self.df_operator.at[k, 'gaosu_jinjufangkongli']
        elif attack_asm_nature == 2:
            if jinzhan_attack_flag == 0:
                defense_fangkongli += self.df_operator.at[k, 'luehai_quyufangkongli']
                defense_fangkongli += int(self.df_operator[['luehai_quyufangkongli']][self.df_operator.index.isin(in_path_operator_list)].sum())
                defense_fangkongli += self.df_operator.at[k, 'no_gaosu_jinjufangkongli']
            elif jinzhan_attack_flag == 1:
                defense_fangkongli += self.df_operator.at[k, 'no_gaosu_jinjufangkongli']
        elif attack_asm_nature == 3:
            if jinzhan_attack_flag == 0:
                defense_fangkongli += self.df_operator.at[k, 'luehai_quyufangkongli']
                defense_fangkongli += int(self.df_operator[['luehai_quyufangkongli']][self.df_operator.index.isin(in_path_operator_list)].sum())
                defense_fangkongli += self.df_operator.at[k, 'gaosu_jinjufangkongli']
            elif jinzhan_attack_flag == 1:
                defense_fangkongli += self.df_operator.at[k, 'gaosu_jinjufangkongli']
        fangyu_xiuzheng = self.df_operator.at[k, 'fangyu_xiuzheng']
        judge_table_col = judge_table.attack_value_to_column(defense_fangkongli)

        # 4. 根据第2步防空力和第3步点数，对照战斗结果裁决表【防御栏】得出防御战斗结果值
        fangyu_zhandou_jieguozhi = self.fanjiandaodan_defense_table[fangyu_xiuzheng][judge_table_col]

        gongji_xiuzheng = self.df_operator.at[k, 'gongji_xiuzheng']
        # 需要在已知攻击方的情况下对攻击修正进行更新， 待添加

        # 5. 为每个目标投掷一个骰子，点数减去防御战斗结果值，并进行攻击修正，修正后得出最终点数：
        result_5_step = 4.5 - fangyu_zhandou_jieguozhi + gongji_xiuzheng

        # 将防御方编队中单算子第五步的结果值写入df_operator中
        self.df_operator.at[k, 'fanjiandaodan_step_5_result'] = result_5_step

    def fanjiandaodan_68(self, dian5, blood_state, destroy_level, fangyuzhi, score):
        # 计算反舰导弹裁决规则第6到第8步的内容。通过一系列输入得到最小的反舰导弹分配值
        # fenpei_level 0, 1 for half_blood= True,  fenpei_level 0, 1, 2 for half_blood= False
        '''
        input:
            dian5 第五步获得的点数
            blood_state = 0,1,2
            fangyuzhi: currently left fangyuzhi
            destroy_level 0, 1 for half_blood= True,  destroy_level 0, 1, 2 for half_blood= False
            judge_table
            judge_table_1row: hejizhandouli row of judge_table
        return:
            fenpeizhi
        '''
        main_judge_table = np.array(judge_data.main_judge_table)
        judge_table_1row = np.array([1, 3, 6, 9, 15, 21, 28, 36, 46, 58, 72, 90])
        if destroy_level == 0:
            return (0, 0)  # 如预期损毁等级为0,则不必分配反舰导弹值
        if blood_state == 2:  # 如已损毁,则不必分配反舰导弹值
            return (0, 0)
        # 需要进行插值计算，待添加
        judge_table_row_num = min(max(int(dian5), -7), 12) + 7  # 通过骰子点数得到裁决表的行信息
        judge_table_row = main_judge_table[judge_table_row_num]  # 定位当前行,并单独取出
        if blood_state == 1:
            fenpei_index = np.min(np.where(judge_table_row >= fangyuzhi * 0.5)[0])
            return judge_table_1row[int(fenpei_index)], (int(score[1]) - int(score[2]))
        else:
            if destroy_level == 2:
                fenpei_index = np.min(np.where(judge_table_row >= fangyuzhi)[0])
                return judge_table_1row[int(fenpei_index)], (int(score[0]) - int(score[2]))
            else:  # destroy_level == 1
                fenpei_index = np.min(np.where(judge_table_row >= fangyuzhi * 0.5)[0])
                return judge_table_1row[int(fenpei_index)], (int(score[1]) - int(score[2]))

    def assign_attack(self, asm_attack, target_id_list):
        """
        计算当防御方是编队时，给防御方的每个算子每个分配多少攻击力。防御方是单算子时，是长度为1的编队
        @param asm_attack: 攻击方的总攻击力
        @param target_id_list: 防御方算子id
        """
        enemy_formation_member_num = len(target_id_list)
        best_result = [0] * enemy_formation_member_num
        best_fenpeizhi = [0] * enemy_formation_member_num

        # 计算在确定攻击方和确定防御方的情况下，怎么分配攻击力可以使得分最高
        # 根据防御方编队中的算子数量生成组合集合， 每个单算子都可以被攻击成3个状态，0,1,2； 如果有n个单算子，就有3的n次方个组合
        for it in itertools.product('012', repeat=enemy_formation_member_num):
            result = [0] * enemy_formation_member_num
            fenpeizhi = [0] * enemy_formation_member_num
            for member in target_id_list:
                member_index = target_id_list.index(member)
                result_5_step = self.df_operator.at[member, 'fanjiandaodan_step_5_result']
                state = self.df_operator.at[member, 'state_fanjian_assume']
                destroy_level = int(it[member_index])
                fangyuzhi = self.df_operator.at[member, 'defense']
                score = self.df_operator.at[member, 'score']
                fenpeizhi[member_index], result[member_index] = self.fanjiandaodan_68(result_5_step,
                                                                                      state,
                                                                                      destroy_level,
                                                                                      fangyuzhi,
                                                                                      score)

            if sum(result) > sum(best_result) and sum(fenpeizhi) <= asm_attack:
                best_result = result
                best_fenpeizhi = fenpeizhi
                # 获取最优结果的攻击df的index（算子id或者编队id）
                # best_attack_id = i
                # best_defense_id = j
                best_it = it
                # best_select_target_id_list = target_id_list

        return best_result, best_fenpeizhi, best_it

    def cal_fanjiandaodan(self):
        """
        计算在当前态势下，在所有攻击方和所有可见的防御方的数据下，攻击方和防御方怎么配对，以及防御方如果是编队，攻击力如何分配
        """
        df_our_attack = copy.deepcopy(self.df_formation.loc[(self.df_formation['camp_id'] == self.camp_id)])
        df_enemy_shuimian = copy.deepcopy(self.df_formation.loc[
            (self.df_formation['category_id2'].isin([101, 102, 103, 104, 108, 109, 888])) & (
                    self.df_formation['camp_id'] != self.camp_id)])
        while df_our_attack.shape[0] > 0 and df_enemy_shuimian.shape[0] > 0:
            drop_attack_list, best_result, best_pair, best_select_target_id_list, best_fenpeizhi, best_destory_state = self.cal_fanjiandaodan_inner(
                df_our_attack, df_enemy_shuimian)

            # 计算出一对最好的攻击方和防御方对，将攻击方从攻击列表中删除，将防御方的状态进行更新
            if best_pair is not None:
                df_our_attack = df_our_attack.drop(index=best_pair[0])
                for i in range(len(best_select_target_id_list)):
                    self.df_operator.at[best_select_target_id_list[i], 'state_fanjian_assume'] = int(best_destory_state[i])
                #df_enemy_shuimian = df_enemy_shuimian.drop(index=best_pair[1])
                print(best_result, best_pair, best_select_target_id_list, best_fenpeizhi)
                # 纪录下攻击方，防御方，攻击力分配，等待拼装给攻击接口， 待添加

            if drop_attack_list:
                df_our_attack = df_our_attack.drop(drop_attack_list)

    def cal_fanjiandaodan_inner(self, df_our_attack, df_enemy_shuimian):
        """
        计算在当前态势下，我方算子和能看到的敌方算子，选择某个攻击方和某个防御方，进行反舰导弹攻击可以得到最大的得分收益

        """
        best_result_out = -1000
        best_fenpeizhi_out = None
        best_pair_out = None
        best_select_target_id_list_out = None
        best_it_out = None
        drop_attack_list = []

        # 遍历目前可以选的攻击方
        for i in df_our_attack.index:
            x_position = df_our_attack.at[i, 'x_position']
            y_position = df_our_attack.at[i, 'y_position']
            asm_range = df_our_attack.at[i, 'asm_range']
            attack_asm_nature = df_our_attack.at[i, 'asm_nature']
            # 如果攻击范围是0，则无法攻击
            if asm_range == 0:
                attack_position_list = []
                drop_attack_list.append(i)
                continue
            # 如果攻击范围不是0， 则计算这个攻击方的攻击范围坐标list
            else:
                attack_position_list = []
                attack_map = self.cal_map.get_radius(x_position, y_position, asm_range)
                attack_position = attack_map.nonzero()
                for z in range(len(attack_position[0])):
                    attack_position_list.append([attack_position[0][z], attack_position[1][z]])
                attack_operator_id = df_our_attack.at[i, 'operator_id']
                attack_formation_id = df_our_attack.at[i, 'formation_id']
                # 如果攻击方是编队，需要计算攻击方列表，用于引擎掷骰子使用
                if attack_formation_id != -1:
                    attack_operator_list = []
                    for item in attack_operator_id.split(','):
                        attack_operator_list.append(int(item))

                # 防御方遍历：遍历敌方的水面算子，包括单算子和编队
                for j in df_enemy_shuimian.index:
                    # 是否能进行攻击， 0 否，1 是
                    can_attack_flag = 0
                    # 是否是近战攻击， 0 否， 1 是
                    jinzhan_attack_flag = 0
                    # 防御方是否是编队
                    is_defenser_formation = 0
                    # 途径六角格防御方水面单位列表
                    in_path_operator_list = []
                    single_operator_id_list = []
                    defense_position = [df_enemy_shuimian.at[j, 'x_position'], df_enemy_shuimian.at[j, 'y_position']]
                    # 如果防御方在攻击方的攻击范围之内，则进行下面计算
                    if defense_position in attack_position_list:
                        can_attack_flag = 1
                        # 如果是相邻格， 视为对水面舰艇的近距战斗
                        distance = cal_map_static.rect_distance([x_position, y_position], defense_position)
                        if distance == 1:
                            jinzhan_attack_flag = 1
                        # 如果攻击距离大于等于 2 格，需加上途经六角格防御方水面单位区域防空力
                        elif distance >= 2:
                            path = self.graph.get_path([x_position, y_position], defense_position)
                            # 路径去掉起点和终点
                            path = path[1:-1]
                            path_list = []
                            for path_point in range(len(path)):
                                path_list.append('{},{}'.format(path[path_point].row, path[path_point].col))
                            # 提取敌方在途径六角格水面算子列表
                            in_path_operator_list = self.df_operator.loc[(self.df_operator['category_id2'].isin([101, 102, 103, 104, 108, 109, 888])) & (self.df_operator['camp_id'] != self.camp_id) & (self.df_operator['position_str'].isin(path_list))].index.tolist()

                        # 如果防御方是单算子
                        if int(df_enemy_shuimian.at[j, 'category_id2']) in ([101, 102, 103, 104, 108, 109]):
                            is_defenser_formation = 0
                            single_operator_id_list.append(j)
                            # 计算第5步的点数
                            self.cal_step_5_result(attack_asm_nature, single_operator_id_list[0], jinzhan_attack_flag, in_path_operator_list)

                        # 如果防御方是编队，则通过接口获得是攻击编队的上半部分还是下半部分
                        elif df_enemy_shuimian.at[j, 'category_id2'] == 888:
                            is_defenser_formation = 1
                            defense_operator_id = df_enemy_shuimian.at[j, 'operator_id']
                            defense_operator_list = []
                            for item in defense_operator_id.split(','):
                                defense_operator_list.append(int(item))
                            defense_formation_id = j
                            # 为编队中的每一个单算子计算第5步的结果
                            for k in defense_operator_list:
                                self.cal_step_5_result(attack_asm_nature, k, jinzhan_attack_flag, in_path_operator_list)

                            # 掷骰子 选择上半部分或者下半部分的算子id。
                            # 需要进行两种部分都计算，然后加权, 待添加
                            # 分别计算编队的上部分和下部分是被攻击对象的结果，将两个结果相加作为总的结果，选择总的结果最好的防御方
                            mid_index = math.ceil(len(defense_operator_list) / 2)
                            defense_list_1 = defense_operator_list[: mid_index]
                            defense_list_2 = defense_operator_list[mid_index:]
                            #select_result = self.sdk.operator_seat.antiShipMissilesTargetSelect(self.round, attack_formation_id, attack_operator_list,defense_formation_id, defense_operator_list)
                            #select_target_id_list = select_result['select_target_ids']

                        if can_attack_flag == 1:
                            # 如果是近距战斗，在第1步中用近距战斗力替代反舰导弹力，选择不使用反舰导弹弹药的单位，攻击值为：近距战斗力减去反舰导弹力；
                            if jinzhan_attack_flag == 1:
                                asm_attack = df_our_attack.at[i, 'close_combat']
                            else:
                                asm_attack = df_our_attack.at[i, 'asm_attack']
                            # 如果是编队，则分别计算上半部分和下半部分的结果，求和再除以2
                            if is_defenser_formation == 1:
                                best_result_list1, best_fenpeizhi1, best_it1 = self.assign_attack(asm_attack, defense_list_1)
                                best_result_list2, best_fenpeizhi2, best_it2 = self.assign_attack(asm_attack, defense_list_2)
                                # best_result1[-1:-1] = best_result2
                                best_result = (sum(best_result_list1) + sum(best_result_list2)) / 2
                            else:
                                best_result_list, best_fenpeizhi, best_it = self.assign_attack(asm_attack, single_operator_id_list)
                                best_result = sum(best_result_list)

                            # enemy_formation_member_num = len(select_target_id_list)
                            # best_result = [0] * enemy_formation_member_num
                            # best_fenpeizhi = [0] * enemy_formation_member_num
                            #
                            # # 计算在确定攻击方和确定防御方的情况下，怎么分配攻击力可以使得分最高
                            # # 根据防御方编队中的算子数量生成组合集合， 每个单算子都可以被攻击成3个状态，0,1,2； 如果有n个单算子，就有3的n次方个组合
                            # for it in itertools.product('012', repeat=enemy_formation_member_num):
                            #     result = [0] * enemy_formation_member_num
                            #     fenpeizhi = [0] * enemy_formation_member_num
                            #     for member in select_target_id_list:
                            #         member_index = select_target_id_list.index(member)
                            #         result_5_step = self.df_operator.at[member, 'fanjiandaodan_step_5_result']
                            #         state = self.df_operator.at[member, 'state']
                            #         destroy_level = int(it[member_index])
                            #         fangyuzhi = self.df_operator.at[member, 'defense']
                            #         score = self.df_operator.at[member, 'score']
                            #         fenpeizhi[member_index], result[member_index] = self.fanjiandaodan_68(result_5_step,
                            #                                                                               state,
                            #                                                                               destroy_level,
                            #                                                                               fangyuzhi,
                            #                                                                               score)
                            #     if sum(result) > sum(best_result) and sum(fenpeizhi) <= asm_attack:
                            #         best_result = result
                            #         best_fenpeizhi = fenpeizhi
                            #         # 获取最优结果的攻击df的index（算子id或者编队id）
                            #         best_attack_id = i
                            #         best_defense_id = j
                            #         best_it = it
                            #         best_select_target_id_list = select_target_id_list

                        print("编队中攻击力分配遍历完毕")
                        # 如果这个攻击方和防御方组合的得分比最好成绩好，则把他们记为最好成绩
                        if best_result > best_result_out:
                            best_pair_out = (i, j)
                            if is_defenser_formation == 0:
                                best_fenpeizhi_out = best_fenpeizhi
                                best_result_out = best_result
                                best_select_target_id_list_out = single_operator_id_list
                            else:
                                select_result = self.sdk.operator_seat.antiShipMissilesTargetSelect(self.round,
                                            attack_formation_id, attack_operator_list, defense_formation_id, defense_operator_list)
                                select_target_id_list = select_result['select_target_ids']
                                best_result_out_list, best_fenpeizhi_out, best_it = self.assign_attack(asm_attack,
                                                                                                  select_target_id_list)
                                best_result_out = sum(best_result_out_list)
                                best_select_target_id_list_out = select_target_id_list
                            best_it_out = best_it
                print("防御方遍历完毕")
                # 如果这个攻击方不能攻击任何防御方，则把它从攻击列表中去掉
                if can_attack_flag == 0:
                    drop_attack_list.append(i)

        print('攻击方遍历完毕')
        return drop_attack_list, best_result_out, best_pair_out, best_select_target_id_list_out, best_fenpeizhi_out, best_it_out
