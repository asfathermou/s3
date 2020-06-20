# --coding:utf-8--


def read_to_end(input_file_name):
    with open(input_file_name, 'r', encoding='utf-8') as input_file:
        return input_file.read().strip()
