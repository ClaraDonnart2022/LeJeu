"""
A simple program to test the host/client connection
"""

import socket
import json
import time as tm

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
data = json.loads(s.recv(1024))
print(data)
