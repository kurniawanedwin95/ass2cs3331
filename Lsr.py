#!/usr/bin/python

import socket
import pickle
import sys
from threading import Thread
import time

def broadcast(s, packet, num_of_neighbour, broadcast_port):
    while True:
        for i in range(0,num_of_neighbour):
            s.sendto(packet, ('127.0.0.1',broadcast_port[i]))
            print "sent to %d" %(broadcast_port[i])
        time.sleep(1)

def testprint():
    print 'test'

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

self = sys.argv[1]
port = int(sys.argv[2])
f = open(sys.argv[3],'r')
neighbours_cost = {}
neighbours_port = {}
threads = []
num_of_neighbour = f.readline()
num_of_neighbour = int(num_of_neighbour)
broadcast_port = []
for i in range (0,num_of_neighbour):
  read = f.readline()
  read = read.split()
  neighbours_cost[read[0]] = float(read[1])
  neighbours_port[read[0]] = int(read[2])
  broadcast_port.append(neighbours_port[read[0]])

cur_time = time.time() #in seconds
print cur_time
t1 = Thread(target=testprint)
packet = 'something'
t2 = Thread(target=broadcast, kwargs={'s':s,'packet':packet,'num_of_neighbour':num_of_neighbour,'broadcast_port':broadcast_port})
threads.append(t1)
threads.append(t2)
t1.start()
t2.start()

# while True:
#   if (time.time()-curtime) > 1000
#     broadcast(s, packet, num_of_neighbour, broadcast_port)
#1 sec send, 30 sec print
