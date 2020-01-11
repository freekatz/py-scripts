from socketserver import TCPServer, ThreadingMixIn, StreamRequestHandler
from dataMain import dataUnpack
import sys
import os

class Server(ThreadingMixIn, TCPServer):
 
    def __init__(self, server_address, RequestHandlerClass):
        TCPServer.__init__(
            self, server_address, RequestHandlerClass)
        self.users = {}
        print("服务器连接成功！！！")
 
 
class MyHandler(StreamRequestHandler):
 
    def handle(self):
        self.addr = self.request.getpeername()
        self.server.users[self.addr[1]] = self.request
        print("用户" + self.addr[0] + ":" + str(self.addr[1]) + "加入了此聊天室...")
        print("此时聊天室中共有 %d 人" % len(self.server.users))
        while True:
            # init()
            try:
                data = self.request.recv(1024).decode()
                packData = self.request.recv(1024).decode()
                if data == "quit":
                    del self.server.users[self.addr[1]]
                    break
                print("用户" + self.addr[0] + ":" + str(self.addr[1]) + " 说： " + str(data))
                self.broadCast(packData)
            except:
                # pass
                raise
                break
        self.request.close()
 
 
    def broadCast(self, message):
        # print(dataUnpack(message))
        for user, output in self.server.users.items():
            if str(user)!=str(self.addr[1]):
                # output.send(str(message).encode())
                output.send(("用户 " + self.addr[0] + ":" + str(self.addr[1]) + " " + " >> " + str(message)).encode())
 
if __name__ == "__main__":
    host = ""
    port = 1231
    server = Server((host, port), MyHandler)
 
    server.serve_forever()