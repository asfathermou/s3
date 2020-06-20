# --coding:utf-8--


# @Author: 逸风
# @Time: 2019-12-22 17:59


class Countries:
    def __init__(self):
        self.id = -1
        self.name = ""
        self.code = ""
        self.camp = -1

    @staticmethod
    def parse(countries_json_object):
        countries = Countries()
        countries.id = int(countries_json_object['id'])
        countries.name = countries_json_object['name']
        countries.camp = int(countries_json_object['camp'])
        countries.code = countries_json_object['code']

        return countries


