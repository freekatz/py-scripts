import socket
from threading import Thread
from dataMain import dataPack, dataUnpack, init
import sys
import re
class ChatClient:

    def __init__(self):
        self.s = socket.socket()
        server = socket.gethostname()
        port = 1231
        self.s.connect((server, port))  # 连接服务器
        self.run()
        recv1 = self._socket.recv(1024).decode()
        print(recv1)
        recv2 = self._socket.recv(1024).decode()
        print(recv2)

    def run(self):
        prepareRecv = self.PrepareRecv(self.s)
        prepareRecv.start()
        while True:
            init()
            data = input("")
            print("                     你说： " + str(data) + "\n")
            packData = dataPack(data)
            try:
                self.s.send(str(data).encode())
                self.s.send(str(packData).encode())
                if data == "quit":
                    break
            except:
                print("与服务器连接中断！")
                break

        self.s.close()  # 关闭连接

    class PrepareRecv(Thread):

        def __init__(self, _socket):
            Thread.__init__(self)
            self.setDaemon = True  # 主线程结束终止子线程
            self._socket = _socket

        def run(self):
            while True:
                init()
                try:
                    readText = self._socket.recv(1024).decode()
                    bit = re.search(r'  >> (.*)', readText).groups()[0]
                    tmp = readText.replace(bit, '')
                    tmp = tmp.replace(">> ", "说：")
                    print("=======================")
                    print("接受到的数据为：{0}".format(bit))
                    data = dataUnpack(bit)
                    if readText == "":
                        self._socket.close()
                        break
                    else:
                        print(tmp + data)
                except:
                    self._socket.close()
                    break


if __name__ == '__main__':
    ChatClient()
