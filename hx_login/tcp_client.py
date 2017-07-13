#!/usr/bin/python

import socket
import sys
import hashlib


# md5
class Encrypt:
    def md5(self, message):
        m = hashlib.md5()
        m.update(str(message))
        return m.hexdigest()


HOST, PORT = "192.168.83.101", 9999
# be used to verify
data = sys.argv[1] + "|" + sys.argv[2] + "|" + Encrypt().md5(sys.argv[3])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((HOST, PORT))
    sock.sendall(data + "\n")
    received = str(sock.recv(1024))
finally:
    sock.close()

if received == "0":
    print("login successfully")
elif received == "1":
    print("wrong password")
elif received == "2":
    print("no such username")
else:
    print("error")
