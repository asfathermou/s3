# --coding:utf-8--

from routine_check import RoutineCheck


class Configure:
    def __init__(self, args=None):
        self.ip = None
        self.room_id = None
        self.scenario_id = None
        self.username = None  # lyu1, lyu2 # username和password在ai中填写
        self.password = None   # lyu , lyu
        self.camp_id = None
        self.seat_id = None
        self.run_model = "not_competition_edition"  # 是否是比赛版
        self.parse_args(args)

    def parse_args(self, args):
        # 启动参数说明：
        # python demo_ai.py ip ai_id room_id camp_id scenario_id seat_id
        # scenario_id:目前提供4个想定，该值取值范围1~4;camp_id:阵营ID，红方为1，蓝方为2;seat_id:'101,10001'; '201,10001'
        # 启动示例（先修改start_game.py中的ip）：
        # python demo_ai.py 10.11.6.45 0 1 1 44 101,10001
        # python demo_ai_2.py 10.11.6.45 0 1 2 44 201,10001
        # python start_game.py
        self.ip = args[1]
        self.ai_id = args[2]  # 非比赛版，该参数随意填写
        self.room_id = int(args[3])
        self.camp_id = int(args[4])
        self.scenario_id = int(args[5])
        self.seat_id = args[6]
        if self.run_model == 'competition_edition':
            self.routine_check = RoutineCheck(self.ai_id, self.room_id, self.camp_id, self.scenario_id, self.seat_id)
