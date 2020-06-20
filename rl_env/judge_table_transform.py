#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/5/21 14:23
# @Author : ZM
# @File : judget_table_transform.py
# @Desc : 

import random
from collections import defaultdict
import rl_env.judge_table_data as judge_table


def attack_value_to_column(value):
    if 1 <= value <= 2:
        col = 0
    elif 3 <= value <= 5:
        col = 1
    elif 6 <= value <= 8:
        col = 2
    elif 9 <= value <= 14:
        col = 3
    elif 15 <= value <= 20:
        col = 4
    elif 21 <= value <= 27:
        col = 5
    elif 28 <= value <= 35:
        col = 6
    elif 36 <= value <= 45:
        col = 7
    elif 46 <= value <= 57:
        col = 8
    elif 58 <= value <= 71:
        col = 9
    elif 72 <= value <= 89:
        col = 10
    elif value >= 90:
        col = 11
    return col


# class JudgeTableTransform:
#
#     def __init__(self):
#         # 模拟掷骰子次数
#         self.count = 1000
#         # 反舰导弹防御修正值列表
#         self.fanjiandaodan_xiuzheng_defense = [-4, -2, 0, 2, 4]
#         # 反舰导弹攻击修正值列表
#         self.fanjiandaodan_xiuzheng_attack = [-4, -3, -2, -1, 0, 1, 2, 3]
#     #     self.yugong_xiuzheng_defense = [-2, -1, 0, 1, 2, 3, 4, 5]
#     #     self.yugong_xiuzheng_attack = [-5, -4, -3, -2, -1, 0, 1, 2, 3]
#     #
#     self.dandaodaodan_xiuzheng_defense = [-2, -1, 0]
#
#     self.hongzha_xiuzheng_defense = [-7, -5, -4, -3, -2, -1, 0, 2]
#     self.hongzha_xiuzheng_attack = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6]
#
#     self.fanqian_xiuzheng_attack = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
#
#     self.jinju_xiuzheng_defense = [-7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3]
#
#     self.kongduikong_xiuzheng_update = [-4, -2, 0, 2, 4]
#
#     self.yuanjulikongduikong_xiuzheng = [0, 2]


# def main_judge_table_dice(defense_xiuzheng_list, attack_xiuzheng_list, count):
#     """
#     主裁决表转换, 通过多次掷骰子来计算期望，计算时间长且不准确
#     @param defense_xiuzheng_list: 当前攻击方式下防御修正值列表
#     @param attack_xiuzheng_list: 当前攻击方式下攻击修正值列表
#     @param count: 模拟掷骰子次数
#     @return:
#     """
#     table = judge_table.main_judge_table
#     row_num = len(table)
#     col_num = len(table[0])
#     defense_result = defaultdict(list)
#     attack_result = defaultdict(list)
#
#     for defense_xiuzheng in defense_xiuzheng_list:
#         for col in range(col_num):
#             result = 0
#             for i in range(count):
#
#                 # 加上掷骰子的数
#                 num = defense_xiuzheng + random.randint(0, 9)
#                 # 防御栏第9行才是值为0的行，所以需要加上8
#                 num += 8
#                 # 防御栏大于20行的值都取第20行的值
#                 if num > (row_num - 1):
#                     num = (row_num - 1)
#                 result += table[num][col]
#             result = result / count
#             defense_result[defense_xiuzheng].append(result)
#
#     for attack_xiuzheng in attack_xiuzheng_list:
#         for col in range(col_num):
#             result = 0
#             for i in range(count):
#                 num = attack_xiuzheng + random.randint(0, 9)
#                 # 进攻栏第8行才是值为0的行，所以需要加上7
#                 num += 7
#                 # 防御栏大于20行的值都取第20行的值
#                 if num > (row_num - 1):
#                     num = (row_num - 1)
#                 result += table[num][col]
#             result = result / count
#             attack_result[attack_xiuzheng].append(result)
#
#     return defense_result, attack_result


def main_judge_table(defense_xiuzheng_list, attack_xiuzheng_list):
    """
    主裁决表转换， 通过计算在骰子区间的10个数求平均来计算，计算准确且速度快
    @param defense_xiuzheng_list: 当前攻击方式下防御修正值列表
    @param attack_xiuzheng_list: 当前攻击方式下攻击修正值列表
    @return: 转换后的裁决表，以修正值为行的index， 列的index和原始裁决表一样
    """
    table = judge_table.main_judge_table
    row_num = len(table)
    col_num = len(table[0])
    defense_result = defaultdict(list)
    attack_result = defaultdict(list)

    for defense_xiuzheng in defense_xiuzheng_list:
        for col in range(col_num):
            result = 0
            # 防御栏第9行才是值为0的行，所以需要加上8
            start = defense_xiuzheng + 8
            num = start
            # 10 是骰子点数， 将这一列[修正值+0, 修正值+ 9]的值相加求平均
            for i in range(10):
                # 防御栏大于20行的值都取第20行的值
                if num > (row_num - 1):
                    num = (row_num - 1)
                result += table[num][col]
                num += 1
            result = result / 10
            defense_result[defense_xiuzheng].append(result)

    for attack_xiuzheng in attack_xiuzheng_list:
        for col in range(col_num):
            result = 0
            # 进攻栏第8行才是值为0的行，所以需要加上7
            start = attack_xiuzheng + 7
            num = start
            # 10 是骰子点数， 将这一列[修正值+0, 修正值+ 9]的值相加求平均
            for i in range(10):
                # 防御栏大于20行的值都取第20行的值
                if num > (row_num - 1):
                    num = (row_num - 1)
                result += table[num][col]
                num += 1
            result = result / 10
            attack_result[attack_xiuzheng].append(result)
    return defense_result, attack_result

    # def fanjiandaodan_judge_result(self):
    #     result = self.main_judge_table(self.fanjiandaodan_xiuzheng_defense, self.fanjiandaodan_xiuzheng_attack)
    #     print(result)
#
# if __name__ == '__main__':
#
#     a = JudgeTableTransform()
#     a.fanjiandaodan_judge_result()
