# --coding:utf-8--

# author:吕石磊 
# create time: 2020/01/03 


class CallBackDemo:

    def __init__(self):
        self.ai_call_back = None

    def sdk_received(self, data):
        data = "sdk处理加工后的数据，" + data
        self.ai_call_back(data)

    def register(self, call_back_func):
        self.ai_call_back = call_back_func


if __name__ == "__main__":
    callback = CallBackDemo()

    def ai_func(data):
        print("ai从sdk收到的数据：", data)

    callback.register(ai_func)
    callback.sdk_received("SDK从服务器接收到的数据")
