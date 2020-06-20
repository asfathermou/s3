# --coding:utf-8--


# @Author: 逸风
# @Time: 2020-01-03 14:49

# 系统常量配置
room_id = 1

# 航空任务类型
interception_task = 101 # 截击任务
bray_task = 102   # 布雷任务
reconnaissance_task = 103   # 侦查任务
awacs_command_task = 104  # 预警指挥任务
tactical_support_task = 105  # 战术支援任务

# 飞机类型
plan_type = {
    '101': ['301', '302', '303'],
    '102': ['304', '307'],
    '103': ['301', '302', '303', '304', '306', '307'],
    '104': ['302'],
    '105': ['301', '305', '307']
}


