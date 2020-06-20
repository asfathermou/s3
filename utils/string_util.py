# --coding:utf-8--

# author:吕石磊 
# create time: 2020/01/07 


def to_int_array(input, separator=','):
    if not input:
        return []
    return [int(i) for i in input.split(separator)]

def to_int(input, default=0):
    if not input:
        return default
    return int(input)

