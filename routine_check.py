# -*-coding:utf-8-*-


import requests
import json
import time
from threading import Thread


class RoutineCheck(Thread):
    def __init__(self, ai_id, room_id, camp_id, scenario_id, seat_id):
        super(RoutineCheck, self).__init__()
        self.url = "http://tapi.wgengine.bkw100.com/ai/heartbeat/index"
        self.message = self.to_json(ai_id, room_id, camp_id, scenario_id, seat_id)
        self.start()

    def to_json(self, ai_id, room_id, camp_id, scenario_id, seat_id):
        message = {
                "ai":{"id":ai_id},
                "room":{"id":room_id},
                "camp_id":camp_id,
                "scenario_id":scenario_id,
                "seat_id":seat_id
                }
        return {"data":json.dumps(message)}

    def run(self):
        while True:
            time.sleep(1)
            self.ai_connection()

    def ai_connection(self):
        #print(self.message)
        res = requests.post(url=self.url, data=self.message)
        #print(res.content)


