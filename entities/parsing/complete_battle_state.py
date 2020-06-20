# --coding:utf-8--


from ai.common_functions import *
from entities.parsing.frame import Frame


# 完整的战斗态势对象
class CompleteBattleState:
    def __init__(self):
        self.frame = None
        self.our_operators = []
        self.enemy_operators = []
        self.our_camp_id = 0
        self.enemy_camp_id = 0

    @staticmethod
    def parse(state_json_object, scenario, our_camp_id):
        """
        解析websocket服务端发过来的态势数据
        :param state_json_object: 态势数据，json对象
        :param scenario: 想定对象
        :param our_camp_id: 我们的阵营ID（红蓝方）
        :return: 解析好的态势对象
        """
        battle_state = CompleteBattleState()
        battle_state.__dict__ = state_json_object
        battle_state.our_camp_id = our_camp_id
        battle_state.enemy_camp_id = 2 if our_camp_id == 1 else 1
        battle_state.our_operators = []
        battle_state.enemy_operators = []

        battle_state.frame = Frame.parse_json(state_json_object["data"])
        for frame_operator_json_object in battle_state.frame.operators:
            war_operator = scenario.update_operator(frame_operator_json_object)
            if war_operator.get_camp_id() == our_camp_id:
                battle_state.our_operators.append(war_operator)
            else:
                battle_state.enemy_operators.append(war_operator)

        return battle_state

    def get_volley_or_expulsion_winner_camp(self):
        """
        获取截击或驱逐的胜方
        :return: 胜方的阵营ID
        """
        winner_camp = self.enemy_camp_id
        try:  # 特定时节才有，其他时节此值为空
            winner_camp = int(self.frame.intercept_expel_winner_camp_ids["1"])
        except Exception as e:
            print(e)
        return winner_camp

    def get_time_section_id(self):
        """
        获得时节ID
        :return: 时节ID
        """
        return self.frame.get_time_section_id()

    def fetch_our_operator_ids_by_category_id1(self, category_id1):
        """
        根据大类选择我们的算子，
        :param category_id1: 大类ID。# category_id1:
        1：水面单位，2：水下单位，3：空中单位，4：岸基单位
        5：基地，6：编队，7：水雷，8：守备部队
        :return: 我方算子中属于大类的集合
        """
        operator_ids = []
        for war_operator in self.our_operators:
            operator_category_id1 = get_category_id1_by_category_id2(war_operator.category_id2)
            if operator_category_id1 == category_id1:
                operator_ids.append(war_operator.operator_id)
        return operator_ids

    def fetch_our_operator_ids_by_category_id2(self, category_id2):
        """
        根据小类选择我们的算子
        :param category_id2: 小类ID。
        101：航母，102：驱逐舰，103：登陆舰，104：护卫舰，105：两栖攻击舰
        106：轻型护卫舰，107：补给舰，108：巡逻艇，201：核潜艇，202：常规潜艇
        301：预警机，302：预指机，303：攻击/歼轰机，304：轰炸机
        305：电子战机，306：截/歼击机，307：侦察机
        401：岸舰导弹，402：弹道导弹，403：巡航导弹，404：防空导弹
        501：机场，502：港口，503:基地，601：任务编组，602：特混编队，701：水雷，801：守备部队
        :return: 我方算子中属于小类的集合
        """
        operator_ids = []
        for war_operator in self.our_operators:
            if war_operator.category_id2 == category_id2:
                operator_ids.append(war_operator.operator_id)
        return operator_ids

    def fetch_enemy_operator_ids_by_category_id1(self, category_id1):
        """
        根据大类选择敌方的算子
        :param category_id1: 大类ID
        :return: 敌方算子中属于大类的集合
        """
        operator_ids = []
        for war_operator in self.enemy_operators:
            operator_category_id1 = get_category_id1_by_category_id2(war_operator.category_id2)
            if operator_category_id1 == category_id1:
                operator_ids.append(war_operator.operator_id)
        return operator_ids

    def fetch_enemy_operator_ids_by_category_id2(self, category_id2):
        """
        根据小类选择敌方的算子
        :param category_id2: 小类ID
        :return: 敌方算子中属于小类的集合
        """
        operator_ids = []
        for war_operator in self.enemy_operators:
            if war_operator.category_id2 == category_id2:
                operator_ids.append(war_operator.operator_id)
        return operator_ids

    def fetch_our_operator_by_id(self, operator_id):
        """
        根据ID选择我方算子
        :param operator_id:目标算子的ID
        :return: 算子ID=operator_id的我方算子
        """
        for war_operator in self.our_operators:
            if war_operator.operator_id == operator_id:
                return war_operator
        return None

    def fetch_enemy_operator_by_id(self, operator_id):
        """
        根据ID选择敌方算子
        :param operator_id:目标算子的ID
        :return: 算子ID=operator_id的敌方算子
        """
        for war_operator in self.enemy_operators:
            if war_operator.operator_id == operator_id:
                return war_operator
        return None

    def fetch_operator_by_id(self, operator_id):
        """
        根据ID选择算子
        :param operator_id: 目标算子的ID
        :return: ID=operator_id的算子
        """
        for war_operator in self.our_operators:
            if war_operator.operator_id == operator_id:
                return war_operator
        for war_operator in self.enemy_operators:
            if war_operator.operator_id == operator_id:
                return war_operator
        return None

