#!/usr/bin/python2.6 -tt
import sys
import time
import socket


def aprspass(callsign):
    # Taken with permission from APRS-XO by Jack Zielke KG4GJY http://zielkeassociates.com/~jack/aprs-xo/
	# Note: The doHash(char*) function is Copyright Steve Dimse 1998
    # As of April 11 2000 Steve Dimse has released this code to the open source aprs community
	 
    # remove SSID, trim callsign, convert to upper case
    cuthere = callsign.find("-")
    if (cuthere != -1):
        callsign = callsign[:cuthere]
    realcall = callsign[:10].upper()
 
    if (realcall == "NOCALL"):
        return "-1"
 
    # initialize hash
    hash = 0x73e2
    i = 0
    length = len(realcall)
 
    # hash callsign two bytes at a time
    while (i < length):
        hash ^= ord(realcall[i])<<8
        if (i+1 < length):
            hash ^= ord(realcall[i+1])
        i += 2
 
    # convert to string and mask off the high bit so number is always positive
    return str(hash & 0x7fff)
	
#user LU7DFV pass -1 vers PyAPRS 0.01b\n filter m/0\n
VERSION = "PyAPRS 0.01b"
CALL= "LU7DFV-10"
PASSWORD = aprspass(CALL)
serverHost = 'rotate.aprs2.net'
serverPort = 14580
address = CALL + '>APRS,TCPIP*:'
#email = '>APRS::EMAIL-2  :francisco79v@hotmail.com This a test.'
#If the positon begins with @ (With timestamp) or = (W/o timestamp) then we are message capable. 
#If not ! (Report w/o timestamp) or a / (Report with timestamp) indicates that there is no APRS messaging capability.
#For now we're just a beacon and we do not send timestamps
position = '!3447.74S/05823.84W-'
# comment length is supposed to be 0 to 43 char. long-this is 53 char. but it works
comment = 'LU7DFV Francisco - Adrogue, BA, AR'
packet = ''
delay = 60*45 # delay in seconds - 15 sec. is for testing - should be 20 to 30 min for fixed QTH

def send_packet():
    my_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_sock.connect((serverHost, serverPort))
	
	# filter m/0 should hide all packets except for those that you send or are sent directly to you.
    my_sock.send('user ' + CALL + ' pass ' + PASSWORD + ' vers ' + VERSION + ' filter m/0\n')
    data = my_sock.recv(4096)
    if data.startswith("#"):
        print "Succesfully logged to APRS-IS!"
    my_sock.send(address + position + comment + '\n')
    #my_sock.send(CALL + email + '\n')
    print packet
    print 'packet sent: ' + time.ctime() 
    time.sleep(15) # 15 sec. delay
    my_sock.shutdown(0)
    my_sock.close()

packet = address + position + comment
#packet = CALL + email
#print (packet) # prints the packet being sent
#print (len(comment)) # prints the length of the comment part of the packet

while 1:
    send_packet()
    time.sleep(delay)
