# --coding:utf-8--


# @Author: 逸风
# @Time: 2019-12-22 18:03



from utils.string_util import to_int_array, to_int


class WarOperator:
    def __init__(self):
        self.id = -1
        self.operator_name = ""
        self.operator_id = -1
        self.category_id2 = -1
        self.country_id = -1
        self.is_find = -1
        self.seat_id = -1
        self.position = ""
        self.army_image = ""
        self.model_image = ""
        self.score = -1
        self.category_ch_name = ""
        self.category_en_name = ""
        self.attributes = []
        self.is_ground_building = -1
        self.is_formation = -1

        # self.type2 = -1
        # self.state = 0
        # self.formation_id = -1
        # self.is_blos = False  # 远距离攻击能力

        # self._camp_id = -1  # init by country_id

    def set_state(self, new_state):
        pass

    def get_camp_id(self):
        return self._camp_id

    def set_camp_id(self, camp_id):
        self._camp_id = camp_id

    @staticmethod
    def parse(war_operator_json_object):
        war_operator = WarOperator()
        war_operator.__dict__ = war_operator_json_object

        # war_operator.is_ground_building
        # war_operator.is_formation
        # "members": ["110201", "110202"]
        if 'members' in war_operator.__dict__:
            war_operator.members = [int(i) for i in war_operator.members]

        war_operator.position = [int(i) for i in war_operator.position.split(",")]
        war_operator.is_find = to_int(war_operator.is_find)
        war_operator.score = [int(i) for i in war_operator.score.split(",")]
        war_operator.state = to_int(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "state"))
        war_operator.move = to_int_array(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "move"))
        war_operator.defense = to_int_array(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "defense"))
        war_operator.asm_attack = to_int_array(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "asm_attack"))
        war_operator.scout_range = to_int(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "scout_range"))
        war_operator.adjustable_range = to_int(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "adjustable_range"))
        war_operator.warning_range = to_int_array(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "warning_range"))
        war_operator.landing = to_int_array(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "landing"))
        war_operator.defense = to_int_array(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "defense"))
        war_operator.asm_nature = to_int(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "asm_nature"))
        war_operator.asm_range = to_int_array(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "asm_range"))
        war_operator.asm_num = to_int(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "asm_num"))
        war_operator.combat_capability = to_int(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "combat_capability"))
        war_operator.is_batch = to_int(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "is_batch"))
        war_operator.bomb = to_int_array(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "bomb"))
        war_operator.is_blos = to_int(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "is_blos"))
        war_operator.blos_range = to_int(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "blos_range"))
        war_operator.wait_round = to_int(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "wait_round"))
        war_operator.retention_round = to_int(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "retention_round"))
        war_operator.is_anti_missile = to_int(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "is_anti_missile"))
        war_operator.antisubmarine = to_int_array(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "antisubmarine"))
        war_operator.antisubmarine_nature = to_int(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "antisubmarine_nature"))
        war_operator.antisubmarine_num = to_int(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "antisubmarine_num"))
        war_operator.torpedo_attack = to_int_array(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "torpedo_attack"))
        war_operator.torpedo_num = to_int(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "torpedo_num"))
        war_operator.to_air = to_int_array(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "to_air"))
        war_operator.close_combat = to_int_array(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "close_combat"))
        war_operator.regional_air_defense = to_int_array(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "regional_air_defense"))
        war_operator.rad_nature = to_int(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "rad_nature"))
        war_operator.close_air_defense = to_int_array(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "close_air_defense"))
        war_operator.cm_attack = to_int_array(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "cm_attack"))
        war_operator.cm_num = to_int(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "cm_num"))
        war_operator.is_helicopter = to_int(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "is_helicopter"))
        war_operator.platform_type = WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "platform_type")
        war_operator.nato_code = WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "nato_code")
        war_operator.torpedo_supply = to_int(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "torpedo_supply"))
        war_operator.is_rad_supply = to_int(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "is_rad_supply"))
        war_operator.is_antisubmarine_supply = to_int(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "is_antisubmarine_supply"))
        war_operator.asm_supply = to_int(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "asm_supply"))
        war_operator.cm_supply = to_int(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "cm_supply"))
        war_operator.cm_range = to_int_array(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "cm_range"))
        war_operator.ba_attack = to_int_array(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "ba_attack"))
        war_operator.ba_num = to_int(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "ba_num"))
        war_operator.ba_range = to_int_array(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "ba_range"))
        war_operator.hasm_num = to_int(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "hasm_num"))
        war_operator.is_hasm_supply = to_int(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "is_hasm_supply"))
        war_operator.shell_num = to_int(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "shell_num"))
        war_operator.shell_supply = to_int(WarOperator.fetch_attribute_value_by_name(war_operator.attributes, "shell_supply"))

        #operator.attributes = [Attributes.parse(operators_json_object) for operators_json_object in operators_json_object['attributes']]
        return war_operator


    @staticmethod
    def fetch_attribute_value_by_name(attributes, name):
        attribute_list = [a for a in attributes if a["attribute_name"] == name]
        if not attribute_list:
            return None
        return attribute_list[0]["attribute_value"]