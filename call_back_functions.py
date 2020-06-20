# --coding:utf-8--


# @Author: 逸风
# @Time: 2019-12-18

import json
# def call_backs():
#     call_back_func_1 = None
#     call_back_func_2 = None
#
#     def call_back_1(func1):
#         call_back_func_1 = func1
#
#     def call_back_2(func2):
#         call_back_func_2 = func2
#
#     return call_back_func_1, call_back_func_2

# cb = call_backs
# cb.call_back_1(func1)


class CallBackFuncs:
    def __init__(self):
        self.ai_call_back = None
        self.xxx_call_back_func = None
        self.fetch_room_info_func = None

    def register(self, call_back_func):
        self.ai_call_back = call_back_func

    def fetch_websocket_msg(self, data):
        """
        接收websocket返回信息
        :param resv:
        :return:
        """
        data = "sdk处理加工后的数据，" + data
        self.ai_call_back(data)

    def set_xxx_call_back(self, xxx_func):
        self.xxx_call_back_func = xxx_func

    def get_xxx_call_back(self, params):
        print(params)

        self.xxx_call_back_func(params)

