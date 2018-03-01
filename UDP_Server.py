# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 10:40:38 2017

@author: Leah Perry and Alex Pokorny
"""

# UDPPingerServer.py
# We will need the following module to generate randomized lost packets
import random
from socket import *
from datetime import datetime
import time
#import everything we need

# Create a UDP socket 
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind(('', 12000))

msg=[] #create array to hold pieces of the incoming message
pmsg = [0,0] #another array to contain pieces of last message
fmt = '%Y-%m-%d %H:%M:%S.%f' #format to parse time

#prepare default message and time to compare to
messageToSend = ''
t0 = time.time()

while True:
	# Generate random number in the range of 0 to 10
	rand = random.randint(0, 10)    
	t1 = time.time()
	if t1 - t0 > 10: #compare current time to old time
		pmsg[1] = 0 #reset message count, assume new client if 10 seconds have passed
	# Receive the client packet along with the address it is coming from 
	message, address = serverSocket.recvfrom(1024)
	# If rand is less is than 4, we consider the packet lost and do not respond
	if rand < 4:
		continue
	#start timer
	t0 = time.time()
	# Otherwise, the server responds   
	#print message
	msg = message.split('\n') #break up the message so we can parse count & time
	if pmsg[1] == 0: #if count is 0, then it's the first in a series of messages
		serverSocket.sendto('FirstPacketReceived', address)
		pmsg[0] = int(msg[0]) #set previous count to 1, the message count
		pmsg[1] = msg[1] #set time as previous time
	else: #if not the first packet
		countDiff= int(msg[0]) - pmsg[0] #calculate packet number difference
		pmsg[0] = int(msg[0]) #then overwrite the previous count
		msgStamp = datetime.strptime(msg[1], fmt) #get time from message
		currStamp = datetime.now() #get current time
		timeDiff = currStamp - msgStamp #compare current to message time
		message = 'Packet sending time: ' + str(timeDiff) #send time elapsed
		pmsg[1] = msg[1] #overwrite previous time
		
		if countDiff > 1: #if we skipped a number, a packet was lost
			message = message + '\n' + str(countDiff - 1) + ' messages lost.'
		#split to get each part of the message
		serverSocket.sendto(message, address) # send information to the receiver
