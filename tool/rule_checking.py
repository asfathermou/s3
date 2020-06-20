# --coding:utf-8--


# @Author: 逸风
# @Time: 2019-12-24 17:15


class ruleChecking:
    """
    规则检查
    """
    def __init__(self):
        pass

    def taskDeployCheck(self, operator_id, task_id):
        """
        算子部署任务时，检查算子是否符合需要部署的任务类型
        :param operator_id: 算子ID
        :param task_id: 任务ID
        :return:
        """
        pass

    def awacsCommandCheck(self, operator_id, coordinate):
        """
        预警指挥机部署规则检查
        :param operator_id: 算子ID
        :param coordinate:  坐标位置
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
        岛礁登陆检查
        条件：
            实施单位
            实施范围
            限制条件
        :param operator_id:
        :param coordinate:
        :return:
        """

        pass

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


