# -- coding:utf-8 --
# Author:      逸风
# Create Time: 2020/3/20 1:46 上午 
# File:        color_printer.py

import datetime

def color_print(str_sentence = None, color = None):
    try:
        if color is not None:
            list_str_colors = ['darkbrown', 'red', 'green', 'yellow', 'blue', 'purple', 'yank', 'white']
            assert  str_sentence is not None and color in list_str_colors
            id_color = 30 + list_str_colors.index(color)
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print('\33[1;35;{}m'.format(id_color) + now + " " + str_sentence + '\033[0m')
        else:
            print(str_sentence)

    except Exception as e:
        print('error in echosentence_color {}'.format(str(e)))
        raise
