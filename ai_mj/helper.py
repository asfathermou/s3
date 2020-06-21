# -*-coding:utf-8-*-
import numpy

class Helper:
    def __init__(self):
        self.camp_operator_ids = {"1": {"kongjing": 130201, "yun8zhen": 130701, "yun8dian": 130501,
                                        "jian1": 133601, "jian2": 133602, "jian3": 133603, "jian4": 133604,
                                        "su1": 130601, "su2": 130602, "su3": 130603, "su4": 130604},
                                  "2": {"jilong1": 210201, "jilong2": 210202, "chenggong1": 210401,
                                        "chenggong2": 210402, "e2t": 230201, "f1": 230601, "f2": 230602, "f3": 230603,
                                        "f4": 230604, "f5": 230605, "f6": 230606, "f7": 230607, "f8": 230608}}
        self.zhencha_renwu_ids = []
        self.zhanshuzhiyuan_renwu_ids = []
        self.jieji_renwu_ids = []
        self.bulei_renwu_ids = []
        self.yujingzhihui_renwu_ids = []

        self.jieji_winner_camp = -1
        self.quzhu_winner_camp = -1

    def fetch_operator(self, df_operator, camp_id, name):
        operator = self.camp_operator_ids[str(camp_id)][name]
        if operator not in df_operator.index.tolist():
            return None
        temp = dict(df_operator.loc[operator])
        res = {}
        for key, val in temp.items():
            if type(val) is numpy.int64:
                val = int(val)
            res[key] = val
        return res

    def fetch_formations(self, df_formation, camp_id):
        formations = []
        for i in df_formation.index:
            _camp_id = df_formation.at[i, "camp_id"]
            category_id2 = df_formation.at[i, "category_id2"]
            if _camp_id == str(camp_id) and int(category_id2) == 888:
                temp = dict(df_formation.loc[i])
                res = {}
                for key, val in temp.items():
                    if type(val) is numpy.int64:
                        val = int(val)
                    res[key] = val
                formations.append(res)
        return formations
