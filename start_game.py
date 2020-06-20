# --coding:utf-8--

import requests
import logging

logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            # filename='tmp/test.log',
                            # filemode='w'
                            )
def post_start_game_message(room_id):
    try:
        # ip = '10.11.6.45'
        # ip = '10.0.112.216'
        # ip = '172.20.10.2'
        ip = '192.168.0.103'
        r = requests.get("http://" + ip + '/api/ai/a_i_service/start', {"room_id": room_id})
        status_code = r.status_code  # 获取返回的状态码
        logging.info("获取返回的状态码:%d" % status_code)
        response_json = r.json()  # 响应内容，json类型转化成python数据类型
        logging.info("响应内容：%s" % response_json)
        # return response_json
    except BaseException as e:
        print("请求失败！")


if __name__ == "__main__":
    room_id = 1
    post_start_game_message(room_id)
