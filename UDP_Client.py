# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 10:41:54 2017

@author: Leah Perry and Alex Pokorny
"""


import socket
from datetime import datetime
from time import time

#information for contact
UDP_IP = "127.0.0.1"
UDP_Name="Localhost"
UDP_PORT = 12000
MESSAGE = 'Ping'

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT

sum = 0 #sum to hold packet times
count = 0 #count of responses
SentPackets = 23 #number of packets to send
#max and min for response time
min = 99999999999999999999999999
max = 0
#an array for our times

for i in range (0,SentPackets):
    thyme= datetime.now()
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    MESSAGE = str(i) + '\n' + str(thyme) 
    #construct a message from the count and the time
    sock.sendto(MESSAGE, (UDP_Name,UDP_PORT)) #send message
    sock.settimeout(1) #set timeout to wait for response
    try:
        modifiedMessage,serverAddress = sock.recvfrom(1024) #receive response
        thyme2THESEQUEL = datetime.now() #get current time
        elapsed = thyme - thyme2THESEQUEL #compare current to sent time
        sum = sum + elapsed.microseconds #calculate sum of all times in session
        if elapsed.microseconds < min: #if time is less than min, assume new min
            min = elapsed.microseconds
        if elapsed.microseconds > max: #if time is more than max, assume new max
            max = elapsed.microseconds
        count= count + 1 #increase count of messages sent
        print modifiedMessage #print out response
        print 'Time elapsed: ' ,elapsed.microseconds, 'microseconds\n'
    except timeout: #if no response, assume packet is lost
        print 'Request timed out.'
        

if count != 0: #if there was a response
    average = sum / count #calculate the average time based on sum
loss = (float(SentPackets - count) / SentPackets) * 100 #calculate loss rate

#report information
print 'The minimum time was: ' ,min, 'microseconds\n'
print 'The maximum time was: ' ,max, 'microseconds\n'
print 'The average time is: ' ,average, 'microseconds\n'
print 'Percentage packets lost: ' ,loss, '%\n'
