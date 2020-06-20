from collections import Counter
import copy
import itertools
import numpy as np
import math
import rl_env.judge_table_transform as judge_table
import rl_env.judge_table_data as judge_data
from entities.hexagon.graph import Graph


class AttackHongzha:
    """
    空袭战斗
    """
    def __init__(self, scenario, camp_id, sdk):
        # 纪录每一个单算子的属性值，属性值实时更新
        self.df_operator = None
        # 纪录按编队进行编组的属性值，只有部分属性是更新有用的，使用时参考update_operator.create_df_formation()中更新的属性值
        self.df_formation = None
        self.cal_map = None
        self.round = None
        self.scenario = scenario
        self.camp_id = camp_id
        self.sdk = sdk
        self.graph = Graph(max_row=100, max_col=100)
        # 限制区域
        self.xianzhishuiyu_list = []
        # 岸基
        self.base_land_list = []

        ####################################
        #
        # 轰炸防御修正值列表
        self.hongzha_xiuzheng_defense = [-4, -2, 0, 2, 4]
        # 轰炸攻击修正值列表
        self.hongzha_xiuzheng_attack = [-4, -3, -2, -1, 0, 1, 2, 3]
        # 轰炸掷骰子转期望裁决表
        self.hongzha_defense_table, self.hongzha_attack_table = judge_table.main_judge_table(
            self.hongzha_xiuzheng_defense, self.hongzha_xiuzheng_attack)
        ####################################

    def set_env(self, scenario, update_operator_property, df_formation, camp_id, cal_map, round):
        self.scenario = scenario
        self.df_operator = update_operator_property
        self.df_formation = df_formation
        self.camp_id = str(camp_id)
        self.cal_map = cal_map
        self.round = round

    def terrain_position_list(self):
        # """
        # 计算在想定中，哪些坐标属于哪种地形
        # 地形： 1:深海;2:浅海;3:陆地;4:海岸;5:岛屿;6:限制水域
        # 地形字段: terrain ，str类型 ‘3’
        # 坐标字段：coordinate， str类型 ‘1,3’
        # """
        #
        for cell in self.scenario.war_map.cells:
            if cell.terrain == '6':
                self.xianzhishuiyu_list.append(cell.coordinate)

    def cal_defenser_attribute(self):
        """
        计算轰炸攻击中防御方算子的各种属性
        @return:
        """
        # 找出有友方空中单位和敌军水面 岸基单位
        df_kongzhong = self.df_operator.loc[
            (300 < self.df_operator['category_id2']) & (self.df_operator['category_id2'] < 400) & (
                    self.df_operator['camp_id'] == self.camp_id)]

        df_shuimian_target = self.df_operator.loc[
            (100 < self.df_operator['category_id2']) & (self.df_operator['category_id2'] < 200) & (
                    self.df_operator['camp_id'] != self.camp_id)]

        df_land_target=self.df_operator.loc[
            (500 < self.df_operator['category_id2']) & (self.df_operator['category_id2'] < 600) & (
                    self.df_operator['camp_id'] == self.camp_id)]

        self.terrain_position_list()
        # ==限制条件==
        # 1.实施轰炸的空中单位，必须能够进入目标所位于的六角格。
        # 2.攻击同时拥有港口和机场的六角格时，必须选其一。

        # a．合计位于该六角格内所有单位的区域防空力
        for i in df_shuimian_target.index:
            fangyu_xiuzheng = 0
            gongji_xiuzheng = 0
            quyufangkongli = 0

            df_same_position = df_shuimian_target.loc[
                (df_shuimian_target['x_position'] == df_shuimian_target.at[i, 'x_position']) & (
                        df_shuimian_target['y_position'] == df_shuimian_target.at[i, 'y_position'])]
            for j in df_same_position.index:
                # 合计区域防空力
                quyufangkongli += df_shuimian_target.at[j, 'regional_air_defense']

            # 目标为水面舰艇单位位于限制水域六角格内时，不可使用区域防空力；
            position_str = '{},{}'.format(df_shuimian_target.at[i, 'x_position'],
                                          df_shuimian_target.at[i, 'y_position'])
            if position_str in self.xianzhishuiyu_list:
                quyufangkongli = 0

            # 目标为基地时，在同一格内的水面舰艇的区域防空力不可被计算；但位于防御范围内的
            # 岸基防空导弹的区域防空力需计算在内。

            # 计算防御修正值
            # 目标属于特混编队 【+2】
            # 目标既不属于特混编队又不属于任务编组 【-2】
            if self.df_operator.at[i, 'category_id2'] == 602:
                fangyu_xiuzheng += 2
            if self.df_operator.at[i, 'category_id2'] != 602 and self.df_operator.at[i, 'category_id2'] != 601:
                fangyu_xiuzheng -= 2

            #     攻击方至少有一个电子战机单位参战时 【-2】
            for k in df_kongzhong.index:
                if self.df_operator.at[k, 'category_id2'] == 305:
                    gongji_xiuzheng -= 2
                    break
            #
            #
            # 攻击方是隐形攻击【-3】
            # yinxin = -3
            # for k in df_kongzhong.index:
            #     if self.df_operator.at[k, 'combat_capability'] != 2:
            #         yinxin = 0
            #         break

            self.df_operator.at[i, 'fangyu_xiuzheng'] = fangyu_xiuzheng
            self.df_operator.at[i, 'gongji_xiuzheng'] = gongji_xiuzheng
            self.df_operator.at[i, 'quyufangkongli'] = quyufangkongli

    def target_defence_cal(self, target_list):
        result = 0
        for i in range(len(target_list)):
            result += self.df_operator.at[target_list[i], 'close_air_defense']
        return result


    def path_region_defence(self, df_shuimian_target, form_position, defence_position):
        # b．合计途经己方水面舰艇区域防空力
        # 实施轰炸战斗的空中单位途经六角格内的己方水面舰艇区域防空力将被累加。途径六角
        # 格相邻格存在拥有宙斯盾能力的己方水面舰艇时，该单位的区域防空力也将被累加。
        ##？？##############################
        # 目标点坐标
        # defences_position = [int(position_str.split(",")[0]), int(position_str.split(",")[1])]

        # 获取路径上的点坐标
        x_position = form_position[0]
        y_position = form_position[1]
        path = self.graph.get_path([x_position, y_position], defence_position)
        path = path[1:-1]
        path_list = []
        for path_point in range(len(path)):
            path_list.append('{}.{}'.format(path[path_point].row, path[path_point].col))

        quyufangkongli = 0
        for path_item in path_list:
            for eve in df_shuimian_target.index:
                eve_x = df_shuimian_target.at[eve, 'x_position']
                eve_y = df_shuimian_target.at[eve, 'y_position']
                path_item_x = int(path_item.split(".")[0])
                path_item_y = int(path_item.split(".")[1])

                # 两坐标相等  加上己方水面舰艇的区域防空力
                if eve_x == path_item_x and eve_y == path_item_y:
                    quyufangkongli += df_shuimian_target.at[eve, 'regional_air_defense']

                # 遍历相邻格子内部拥有宙斯盾的己方水面舰艇
                if (math.fabs(eve_x - path_item_x) + math.fabs(eve_y - path_item_y)) <= 2 and (
                        df_shuimian_target.at[eve, 'rad_nature'] == 1 or df_shuimian_target.at[eve, 'rad_nature'] == 3):
                    quyufangkongli += df_shuimian_target.at[eve, 'regional_air_defense']
        return int(quyufangkongli)

    def cal_hongzha(self):
        """
        计算在当前态势下，在所有攻击方和所有可见的防御方的数据下，攻击方和防御方怎么配对，以及防御方如果是编队，攻击力如何分配
        """
        hongzha_prepare_list = []

        # 我方空中单位
        df_our_attack = self.df_formation.loc[(self.df_formation['camp_id'] == self.camp_id) & (self.df_formation['category_id2'] == 306)]

        # 敌方水面单位和基地单位
        df_enemy_shuimian = self.df_formation.loc[
            (self.df_formation['category_id2'].isin([101, 102, 103, 104, 108, 109, 501, 888])) & (
                    self.df_formation['camp_id'] != self.camp_id)]

        while df_our_attack.shape[0] > 0 and df_enemy_shuimian.shape[0] > 0:
            drop_attack_list, best_result, best_pair, best_select_target_id_list, best_fenpeizhi, best_destory_state = self.cal_hongzha_inner(
                df_our_attack, df_enemy_shuimian)

            # 计算出一对最好的攻击方和防御方对，就将他们从攻击方和防御方列表中删掉
            if best_pair is not None:
                df_our_attack = df_our_attack.drop(index=best_pair[0])
                df_enemy_shuimian = df_enemy_shuimian.drop(index=best_pair[1])
                print(best_result, best_pair, best_select_target_id_list, best_fenpeizhi)
                every_plan = [best_result, best_pair, best_select_target_id_list, best_fenpeizhi]
                hongzha_prepare_list.append(every_plan)
                # 纪录下攻击方，防御方，攻击力分配，等待拼装给攻击接口， 待添加
            else:
                break
            # if drop_attack_list:
            #     df_our_attack = df_our_attack.drop(drop_attack_list)

    def hongzha_68(self, dian3, blood_state, destroy_level, fangyuzhi, score):
        # 通过一系列输入得到最小的轰炸力分配值
        # fenpei_level 0, 1 for half_blood= True,  fenpei_level 0, 1, 2 for half_blood= False
        '''
        input:
            dian3 第三步获得的点数
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
            return (0, 0)  # 如预期损毁等级为0,则不必分配轰炸值
        if blood_state == 1:
            return (-1, 0)

        judge_table_row_num = min(max(int(dian3), -7), 12) + 7  # 通过骰子点数得到裁决表的行信息
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

    def cal_step_3_result(self, defense_operator_id, path_defence, target_defence):
        """
        计算裁决规则第3步的点数
        @param attack_bomb: 攻击方的总攻击力
        @param defense_operator_id: 防御方算子id
        @return: 轰炸战斗裁决规则第3步的点数

        4.根据第2步中防御方防空值和第3步中点数，对照战斗结果裁决表【防御栏】，得出防御战斗结果值。
        """
        k = defense_operator_id
        defense_quyufangkongli = self.df_operator.at[k, 'quyufangkongli'] + path_defence + target_defence

        fangyu_xiuzheng = self.df_operator.at[k, 'fangyu_xiuzheng']

        judge_table_col = judge_table.attack_value_to_column(defense_quyufangkongli)

        # 4. 根据第2步防空力和第3步点数，对照战斗结果裁决表【防御栏】得出防御战斗结果值
        fangyu_zhandou_jieguozhi = self.hongzha_defense_table[fangyu_xiuzheng][judge_table_col]

        gongji_xiuzheng = self.df_operator.at[k, 'gongji_xiuzheng']

        # 根据防御战斗结果值确定攻击方飞机损伤点数（系统随机选择受伤单位）：
        # 对照【轰炸战斗时攻击方损伤表】
        feijisunshangzhi = 0
        if self.df_operator.at[k, 'rad_nature'] != 1:
            if 0 <= fangyu_zhandou_jieguozhi <= 3:
                feijisunshangzhi = 0
            elif 4 <= fangyu_zhandou_jieguozhi <= 6:
                feijisunshangzhi = 0.5
            elif 7 <= fangyu_zhandou_jieguozhi <= 11:
                feijisunshangzhi = 1
        else:
            if 0 <= fangyu_zhandou_jieguozhi <= 1:
                feijisunshangzhi = 0
            elif 2 <= fangyu_zhandou_jieguozhi <= 3:
                feijisunshangzhi = 0.5
            elif 4 <= fangyu_zhandou_jieguozhi <= 6:
                feijisunshangzhi = 1
            elif 7 <= fangyu_zhandou_jieguozhi <= 11:
                feijisunshangzhi = 1.5
        # 飞机受到损伤后，攻击力下降，按比例自动重新分配轰炸力，但不能改变目标
        step_7_xiuzheng = 0
        # 7.掷骰子，从掷出的点数中减去防御战斗结果值，并进行以下修正：
        # ▪ 攻击方是否使用战术支援，用一个【+1】，最多用 3 个
        # ▪ 目标在港口或限制水域六角格 【+3】
        # ▪ 目标为导弹艇（巡逻艇）【-2】
        # ▪ 夜间的轰炸战斗，不具备夜间战斗能力的单位的轰炸力达到总轰炸力一半以上时
        # 【-2】
        # ▪ 目标六角格内存在防御方宙斯盾舰时 【-1】
        # 待添加！！！！！！！！！！！！！！！！！！！！！！！！！！！！
        result_3_step = 4.5 - fangyu_zhandou_jieguozhi + gongji_xiuzheng

        # 将防御方编队中单算子第三步的结果值写入df_operator中
        self.df_operator.at[k, 'hongzha_step_3_result'] = result_3_step

    def cal_hongzha_inner(self, df_our_attack, df_enemy_shuimian):
        """
        计算在当前态势下，我方算子和敌方算子处于同一位置时，计算出轰炸的最大得分收益
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
            our_position = [x_position, y_position]

            # 防御方遍历：遍历敌方的水面算子，包括单算子和编队
            for j in df_enemy_shuimian.index:
                can_attack_flag = 0
                select_target_id_list = []
                #
                form_position = [df_our_attack.at[i, 'x_position'],
                                 df_our_attack.at[i, 'y_position']]
                defence_position = [df_enemy_shuimian.at[j, 'x_position'],
                                    df_enemy_shuimian.at[j, 'y_position']]

                #
                # 如果防御方在攻击方同一个格子，则进行下面计算
                can_attack_flag = 1
                # 如果防御方是单算子
                if int(df_enemy_shuimian.at[j, 'category_id2']) in ([101, 102, 103, 104, 108, 109]):
                    select_target_id_list.append(j)

                    # 计算第5步的点数
                    self.cal_step_3_result(select_target_id_list[0], self.path_region_defence(
                                df_enemy_shuimian, form_position, defence_position),
                                           self.target_defence_cal(select_target_id_list))

                # 如果防御方是编队
                elif df_enemy_shuimian.at[j, 'category_id2'] == 888:
                    defense_operator_id = df_enemy_shuimian.at[j, 'operator_id']
                    defense_operator_list = []
                    for item in defense_operator_id.split(','):
                        defense_operator_list.append(int(item))

                        select_target_id_list.append(int(item))
                    # 为编队中的每一个单算子计算第5步的结果
                    for k in defense_operator_list:
                        self.cal_step_3_result(k, self.path_region_defence(
                            df_enemy_shuimian, form_position, defence_position),
                                               self.target_defence_cal(select_target_id_list))

                if can_attack_flag == 1:
                    # 防御方算子列表
                    enemy_formation_member_num = len(select_target_id_list)
                    best_result = [0] * enemy_formation_member_num
                    best_fenpeizhi = [0] * enemy_formation_member_num
                    best_it = -1
                    best_select_target_id_list = []
                    asm_attack = df_our_attack.at[i, 'bomb']
                    # 计算在确定攻击方和确定防御方的情况下，怎么分配攻击力可以使得分最高
                    # 根据防御方编队中的算子数量生成组合集合， 每个单算子都可以被攻击成3个状态，0,1,2； 如果有n个单算子，就有3的n次方个组合
                    for it in itertools.product('012', repeat=enemy_formation_member_num):
                        result = [0] * enemy_formation_member_num
                        fenpeizhi = [0] * enemy_formation_member_num

                        for member in select_target_id_list:
                            member_index = select_target_id_list.index(member)
                            result_3_step = self.df_operator.at[member, 'hongzha_step_3_result']
                            state = self.df_operator.at[member, 'state']
                            destroy_level = int(it[member_index])
                            fangyuzhi = self.df_operator.at[member, 'defense']
                            score = self.df_operator.at[member, 'score']
                            fenpeizhi[member_index], result[member_index] = self.hongzha_68(result_3_step,
                                                                                                  state,
                                                                                                  destroy_level,
                                                                                                  fangyuzhi,
                                                                                                  score)
                        if sum(result) > sum(best_result) and sum(fenpeizhi) <= asm_attack:
                            best_result = result
                            best_fenpeizhi = fenpeizhi
                            # 获取最优结果的攻击df的index（算子id或者编队id）
                            best_attack_id = i
                            best_defense_id = j
                            best_it = it
                            best_select_target_id_list = select_target_id_list

                print("编队中攻击力分配遍历完毕")
                # 如果这个攻击方和防御方组合的得分比最好成绩好，则把他们记为最好成绩
                if sum(best_result) > best_result_out:
                    best_result_out = sum(best_result)
                    best_fenpeizhi_out = best_fenpeizhi
                    best_pair_out = [i, j]
                    best_select_target_id_list_out = best_select_target_id_list
                    best_it_out = best_it
            print("防御方遍历完毕")
            if can_attack_flag == 0:
                drop_attack_list.append(i)

        print('攻击方遍历完毕')
        return drop_attack_list, best_result_out, best_pair_out, best_select_target_id_list_out, best_fenpeizhi_out, best_it_out
