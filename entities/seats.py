# --coding:utf-8--


# @Author: 逸风
# @Time: 2019-12-22 18:01


class Seats:
    def __init__(self):
        self.id = -1
        self.country_id = -1
        self.seat_id = -1
        self.seat_name = ""


    @staticmethod
    def parse(seats_json_object):
        seats = Seats()
        seats.id = seats_json_object['id']
        seats.country_id = seats_json_object['country_id']
        seats.seat_id = seats_json_object['seat_id']
        seats.seat_name = seats_json_object['seat_name']

        return seats


