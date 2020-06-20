# --coding:utf-8--


# @Author: 逸风
# @Time: 2020-01-05 15:34

# 规则检查

import const

class RuleChecksUtil:
    def __init__(self, scenario_info=None):

        self._scenario_info = scenario_info

    def taskDeployCheck(self, operator_id, task_id):
        """
        航空任务部署，检查算子是否符合要部署是任务类型
        :param operatorID:  算子ID
        :param taskID: 任务类型:101=截机任务,102=布雷任务,103=侦查任务,104=预警指挥任务,105=战术支援任务
        :return:
        """
        operators = self._scenario_info.operators
        for operator in operators:
            if operator.operator_id == operator_id:
                """ 判断算子是否是空中单位 """
                category_id1 = str(operator.category_id2)[:1]
                if category_id1 == '3':
                    """ 判断算子是否允许执行相应的任务 """
                    if str(operator.category_id2) in const.plan_type[str(task_id)]:
                        """ 反潜战斗力为0的空中算子，不可对潜艇实施侦察 """
                        for attributes in operator.attributes:
                            if attributes.attribute_name == 'antisubmarine':
                                antisubmarine = ','.join(attributes.attribute_value.split(',')[:1])
                                if int(antisubmarine) > 0:
                                    return 0
                                else:
                                    return -3
                    else:
                        return -3
                else:
                    return -3

    def awacsCommandCheck(self, operator_id, coordinate):
        """
        预警指挥机部署
        :param operatorID:  算子ID
        :param coordinate:  部署坐标
        :return:
        """
        pass

    def maneuveringCheck(self, operator_id, coordinate):
        """
        机动检查
        条件：
            水面单位
            水下单位
            空中单位
            岸基单位
        :param operator_id: 算子ID
        :param coordinate:  坐标位置
        :return:
        """
        pass



    def attackCheck(self, operator_id, target_ids, attack_type):
        """
        攻击检查
        条件：
            发动单位
            目标单位
            目标单位
            限制条件
        :param operator_id:
        :param target_ids:
        :param attack_type:
        :return:
        """
        pass

    def reefsLandingCheck(self, operator_id, coordinate):
        """
        岛礁登陆检查,天气为暴雨的格子不能登陆
        条件：
            实施单位
            实施范围
            限制条件
        :param operator_id:
        :param coordinate:
        :return:
        """
        # 获取地图数据
        maps = self._scenario_info.war_map[0]
        for smaps in maps.cells:
            if smaps.coordinate == coordinate:
                if smaps.weather == 3:
                    return -2
                else:
                    return 0

    def brayCheck(self, operator_id, coordinate):
        """
        布雷检查
        :param operator_id:
        :param coordinate:
        :return:
        """
        pass

if __name__ == "__main__":
    pass


