"""
This script is the server to wich players will connect.
This script should call the back end.
Then the players will only have to run the UI
"""


import socket
import json

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print("listening")
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if data and data != b"close connection":
                binary = str.encode(
                    json.dumps(
                        {
                            "cards": [
                                {
                                    "color": "blue",
                                    "picture": "img\sheep.jpg",
                                    "description": ["Super:", "une super carte"],
                                },
                                {
                                    "color": "pink",
                                    "picture": "img\sheep.jpg",
                                    "description": ["Super:", "une super carte"],
                                },
                                {
                                    "color": "gray",
                                    "picture": "img\sheep.jpg",
                                    "description": ["Super:", "une super carte"],
                                },
                                {
                                    "color": "blue",
                                    "picture": "img\sheep.jpg",
                                    "description": ["Super:", "une super carte"],
                                },
                                {
                                    "color": "pink",
                                    "picture": "img\sheep.jpg",
                                    "description": ["Super:", "une super carte"],
                                },
                                {
                                    "color": "gray",
                                    "picture": "img\sheep.jpg",
                                    "description": ["Super:", "une super carte"],
                                },
                            ]
                        }
                    )
                )
                conn.sendall(binary)

            # closing server
            elif data == b"close connection":
                print("connection closed")
                break

            # just waiting
            else:
                pass
