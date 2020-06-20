# --coding:utf-8--


# @Author: 逸风
# @Time: 2019-12-18


from seat.seat import Seat


class OperatorSeat(Seat):
    """
    算子指挥员的席位
    """
    def __init__(self, http_client, user, room):
        super(OperatorSeat).__init__()
        self._user = user
        self._room = room
        self._http_client = http_client

    def antiShipMissilesTargetSelect(self, round_id, attack_formation_id, attack_operator_ids, target_formation_id,
                                     target_operator_ids):
        """
        反舰导弹目标选择接口
        :param round_id:    数值，回合id
        :param attack_formation_id: 数值，发起反舰导弹的编队id，非编队发起填-1
        :param attack_operator_ids: 列表，发起的operator_id列表
        :param target_formation_id: 数值，被攻击方的编队id
        :param target_operator_ids: 列表，被攻击方编队内的的所有operator_id的列表
        :return:
        """
        result = self._http_client.http_post_anti_ship_missiles_target_select(round_id, attack_formation_id,
                                                                              attack_operator_ids, target_formation_id,
                                                                              target_operator_ids)

        return result

    def createFormation(self, position, move, operator_ids):
        """
        创建编队接口
        :param position: 坐标位置
        :param move: 机动值
        :param operator_ids: 算子列表
        :return:
        """
        #以下数据是又SDK维护并输出#
        room_id = self._room.room_id
        formation_dict = {}
        formation_dict['room_id'] = room_id
        formation_dict['scenario_id'] = self._room.scenario_id
        formation_dict['type'] = 301
        formation_dict['country_id'] = 1
        formation_dict['rounds'] = 1
        formation_dict['seat'] = 101
        formation_dict['category_id'] = 601
        formation_dict['camp'] = self._room.camp_id
        formation_dict['operator_ids'] = ",".join(operator_ids)
        formation_dict['position'] = position
        formation_dict['move'] = move

        result = self._http_client.http_post_create_formation(formation_dict)

        return result

    def adjustFormation(self, adjust_formation_dicts):
        """
        调整编队接口
        :param adjust_formation_dict: 调整编队的算子字典
        :return:
        """
        # adjustFormationDict = {"type": 302, "user_id": 59, "room_id": 1444, "scenario_id": 1, "camp": 2,
        #                        "deleted_formation_ids": "", "changed_formations": [
        #                        {"operator_id": 260201, "country_id": 2, "rounds": 1, "seat": 201, "is_find": 0,
        #                        "operator_ids": "210201,210401"}]}

        adjust_formation_dict = {}
        adjust_formation_dict['type'] = 302
        adjust_formation_dict['room_id'] = self._room.room_id
        adjust_formation_dict['scenario_id'] = self._room.scenario_id
        adjust_formation_dict['camp'] = self._room.camp_id
        adjust_formation_dict['deleted_formation_ids'] = ",".join(adjust_formation_dicts['deleted_formation_ids'])
        adjust_formation_dict['changed_formations'] = adjust_formation_dicts['changed_formations']

        for changed_formations in adjust_formation_dicts['changed_formations']:
            changed_formations['operator_ids'] = ",".join(changed_formations['operator_ids'])


        result = self._http_client.http_post_adjust_formation(adjust_formation_dict)

        return result

    def presetFormatioOrder(self, operator_id, order_asuw=None, order_fish_attact=None):
        """
        预设编队顺序接口
        :param operator_id:
        :param order_asuw:
        :param order_bomb:
        :param order_fish_attact:
        :return:
        """

        presetFormatioOrderDict = {}
        presetFormatioOrderDict['type'] = 305
        presetFormatioOrderDict['room_id'] = self._room.room_id
        presetFormatioOrderDict['scenario_id'] = self._room.scenario_id
        presetFormatioOrderDict['camp'] = self._room.camp_id
        presetFormatioOrderDict['operator_id'] = operator_id
        presetFormatioOrderDict['order_asuw'] = ",".join(order_asuw)
        presetFormatioOrderDict['order_fish_attact'] = ",".join(order_fish_attact)

        result = self._http_client.http_post_preset_formation_order(presetFormatioOrderDict)

        return result

    def transferFommand(self, operator_id, receive_seat_id):
        """
        移交指挥权接口
        :param operator_id: 算子ID
        :param receive_seat_id: 接收指挥权的席位ID
        :param room_id: 推演室ID
        :param camp_id: 阵营ID
        :return:
        """

        transferFommandDict = {}
        transferFommandDict['id'] = operator_id
        transferFommandDict['seat'] = receive_seat_id
        transferFommandDict['room_id'] = self._room.room_id
        transferFommandDict['camp_id'] = self._room.camp_id

        result = self._http_client.http_post_transfer_command(transferFommandDict)

        return result


    def disbandedFormations(self, operator_id):
        """
        解散编队接口
        :param operator_id: 编队ID
        :param room_id: 推演室ID
        :return:
        """

        disbandedFormationsDict = {}
        disbandedFormationsDict['operator_id'] = operator_id
        disbandedFormationsDict['room_id'] = self._room.room_id
        result = self._http_client.http_post_disbanded_formations(disbandedFormationsDict)

        return result

    def formationFinished(self, section_id):
        """
        编队调整完成
        :param section_id: 时节ID
        :return:
        """
        result = self._http_client.http_pot_formation_finished(section_id, self._room.room_id, self._room.camp_id)

        return result

    def submarineVoyageMode(self, operatorList):
        """
        潜艇航行模式宣告时节接口
        :param room_id: 推演室ID
        :param camp_id: 阵营ID
        :param rounds: 算子ID
        :param operator_id: 算子ID
        :param type: 航行模式:1：正常航行;2=高速航行;3=深潜模式
        :return:
        """
        params = {}
        params['room_id'] = self._room.room_id
        params['camp_id'] = self._room.camp_id
        if operatorList is not None:
            for operator in operatorList:
                operator['room_id'] = self._room.room_id
                operator['camp_id'] = self._room.camp_id
                operator['rounds'] = 1

            params['operators'] = operatorList
        else:
            params['operators'] = []
        result = self._http_client.http_post_submarine_voyage_mode(params)

        return result

    def maneuveringAttack(self, maneuvering_attack_dict):
        """
        作战筹划阶段-各种机动攻击数据接口
        鱼攻、反舰导弹、巡航导弹、弹道导弹、轰炸、反潜、近距等战斗类型攻击数据接口
        :param submarine_voyage_data_dict: 攻击算子数据字典
        :return:
        """
        send_list = []
        if maneuvering_attack_dict is not None:
            for send_dict in maneuvering_attack_dict:
                send_dict['room_id'] = self._room.room_id
                send_dict['scenario_id'] = self._room.scenario_id
                send_dict['country_id'] = 2
                # send_dict['operator_id'] = operator_id
                send_dict['camp'] = self._room.camp_id
                # send_dict['seat'] = 101
                # send_dict['act_order'] = act_order
                send_dict['rounds'] = 1
                # send_dict['is_formation'] = is_formation
                send_dict['act_content']['room_id'] = self._room.room_id
                send_dict['act_content']['camp'] = self._room.camp_id
                # send_dict['act_content']['seat'] = 201
                # send_dict['act_content'] = maneuvering_attack_dict['act_content']

                send_list.append(send_dict)

        result = self._http_client.http_post_maneuvering_attack(send_list)

        return result

    def attack_finished(self, section_id):
        """
        作战筹划完成接口
        :param section_id:
        :return:
        """
        result = self._http_client.http_post_attack_finished(section_id)

        return result

    def aircraftReturn(self, operator_id, position, section_id, return_type):
        """
        调整阶段-飞机返航接口
        :param operator_id: 算子ID
        :param position: 返航位置坐标
        :param section_id: 时节ID
        :param return_type: 返航类型
        :return:
        """
        result = self._http_client.http_post_aircraft_return(operator_id, position, section_id, return_type)

        return result



