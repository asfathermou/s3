# --coding:utf-8--


# @Author: 逸风
# @Time: 2020-01-02 20:19
import json
from websocket import create_connection
from threading import Thread


class WebSocketUtil(Thread):
    def __init__(self, ipaddress ,call_back_func):
        super(WebSocketUtil, self).__init__()
        self._ipaddress = ipaddress
        self._call_back = call_back_func
        self._ws = create_connection("ws://"+self._ipaddress+":8283")  # todo： 修改websocket server 地址
        self.start()

    def close(self):
        self._ws.close()
        print("Closed down")

    def send_message(self, message):
        self._ws.send(message)
        print("send message:", message)

    def run(self):

        # call_back = CallBackFuncs()
        while True:
            msg = self._ws.recv()
            recv = json.loads(str(msg))
            # print("Received '%s'" % recv)
            self._call_back(recv)
            # 接收消息
            # call_back.fetch_websocket_msg(recv)
            # print("Received '%s'" % recv)

if __name__ == "__main__":
    # web_socket = WebSocketUtil()
    # web_socket.send_message("test sting 123")
    # web_socket.start()
    # 其他代码
    print("其他代码运行中")


