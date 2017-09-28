import socket
import os
import sys


host = '127.0.0.1'
port = 4440

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((host, port))

while True:
    cmd = raw_input("freshell#> ")
    split = cmd.split(" ")
    cd = split[0]
    path = split[-1]
    try:
        s.send(cmd)
    except:
        print "[-] Cannot send user input."
    if cmd == "quit":
        s.send("QUIT")
        s.close()
        exit()
    elif cd == "cd":
        continue
    else:
        data = s.recv(4096)
        sys.stdout.write(data)
        sys.stdout.flush()
