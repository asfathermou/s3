# --coding:utf-8--

# author:吕石磊 
# create time: 2020/01/06 
import ai.ai_const as const


def if_operator_is_intercepter_fighter(war_operator):
    if war_operator.category_id2 == const.intercepter_fighter_id:
        return True
    else:
        return False


def get_category_id1_by_category_id2(category_id2):
    # return category_id1
    return category_id2 // 100

# category_id1:
# 1：水面单位
# 2：水下单位
# 3：空中单位
# 4：岸基单位
# 5：基地
# 6：编队
# 7：水雷
# 8：守备部队
#

# category_id2:
# 101：航母
# 102：驱逐舰
# 103：登陆舰
# 104：护卫舰
# 105：两栖攻击舰
# 106：轻型护卫舰
# 107：补给舰
# 108：巡逻艇
# 201：核潜艇
# 202：常规潜艇
# 301：预警机
# 302：预指机
# 303：攻击/歼轰机
# 304：轰炸机
# 305：电子战机
# 306：截/歼击机
# 307：侦察机
# 401：岸舰导弹
# 402：弹道导弹
# 403：巡航导弹
# 404：防空导弹
# 501：机场
# 502：港口
# 503:基地
# 601：任务编组
# 602：特混编队
# 701：水雷
# 801：守备部队
