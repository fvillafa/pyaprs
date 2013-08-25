#!/usr/bin/python2.6 -tt
import sys
import time
import socket


def aprspass(callsign):
    cuthere = callsign.find("-")
    if (cuthere != -1):
        callsign = callsign[:cuthere]
    realcall = callsign[:10].upper()
    if (realcall == "NOCALL"):
        return "-1"
    hash = 0x73e2
    i = 0
    length = len(realcall)
    while (i < length):
        hash ^= ord(realcall[i])<<8
        if (i+1 < length):
            hash ^= ord(realcall[i+1])
        i += 2
    return str(hash & 0x7fff)

VERSION = "PyAPRS 0.01b"
CALL= "LU7DFV-10"
PASSWORD = aprspass(CALL)
serverHost = 'rotate.aprs2.net'
serverPort = 14580
address = CALL + '>APRS,TCPIP*:' 
position = '!3447.74S/05823.84W-'
#position = '=3447.74S/05823.84W-'
# comment length is supposed to be 0 to 43 char. long-this is 53 char. but it works
comment = 'LU7DFV Francisco - Adrogue, BA, AR'
packet = ''
delay = 60*45 # delay in seconds - 15 sec. is for testing - should be 20 to 30 min for fixed QTH

def send_packet():
    my_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_sock.connect((serverHost, serverPort))
    my_sock.send('user ' + CALL + ' pass ' + PASSWORD + ' vers ' + VERSION + 'filter p/LU/LW\n')
    data = my_sock.recv(4096)
    if data.startswith("#"):
        print "Succesfully logged to APRS-IS!"
    my_sock.send(address + position + comment + '\n')
    print "\033[1;36m"+packet+"\033[1;m"
    print("\033[1;32mpacket sent: " + time.ctime()+"\033[1;m" )
    time.sleep(15) # 15 sec. delay
    my_sock.shutdown(0)
    my_sock.close()
                                                          
packet = address + position + comment
#print (packet) # prints the packet being sent
#print (len(comment)) # prints the length of the comment part of the packet

while 1:
    send_packet()
    time.sleep(delay)

