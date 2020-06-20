# -- coding:utf-8 --
# Author:      逸风
# Create Time: 2020/3/20 12:16 上午 
# File:        logger.py.

from utils.color_printer import color_print


class Logger:
    def __init__(self, ai_name):
        self._ai_name = ai_name

    def print(self, round, message):
        if self._ai_name == "ai_1":
            color_print("\t".join([self._ai_name, str(round), message]), "red")
        elif self._ai_name == "ai_2":
            color_print("\t".join([self._ai_name, str(round), message]), "blue")
        else:
            color_print("\t".join([self._ai_name, str(round), message]), "green")
