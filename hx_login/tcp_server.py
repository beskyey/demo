#!/usr/bin/python

import SocketServer
from db_submit import MysqlSubmit


class MyTCPHandler(SocketServer.BaseRequestHandler):
    #
    def verify(self, username, password):
        result = MysqlSubmit().proof(username, password)
        self.request.sendall(str(result))

    # get other arguments
    def others(others, argv1, argv2):
        print (argv1 + " " + argv2)

    def handle(self):
        self.data = str(self.request.recv(1024).strip())
        print ("{0} connected:".format(self.client_address[0]))
        self.function = self.data.split('|', 2)[0]
        self.argument1 = self.data.split('|', 2)[1]
        self.argument2 = self.data.split('|', 2)[2]
        # to choose function using the first argument
        if self.function == "mysql":
            self.verify(self.argument1, self.argument2)
        elif self.function == "others":
            self.others(self.argument1, self.argument2)


if __name__ == "__main__":
    HOST, PORT = "192.168.83.101", 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
