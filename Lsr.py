#!/usr/bin/python

import socket
import pickle
import sys
from threading import Thread
import time

def broadcast(s, packet, num_of_neighbour, neighbours_port):
    while True:
        for i, v in enumerate(neighbours_port):
            s.sendto(packet, ('127.0.0.1',neighbours_port[v]))
            print 'sent to %s' %(v)
        time.sleep(1)

def rebroadcast(s, packet, num_of_neighbour, broadcast_port):
    #gotta checks for incoming packet, and will rebroadcast while also adding more to the topology
    message, client = s.recvfrom() #will check client's port and match it with existing
    for i in range(0,num_of_neighbour):
        s.sendto(packet, ('127.0.0.1',broadcast_port[i]))
        print 'rebroadcasted packet from'

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
for i in range (0,num_of_neighbour):
  read = f.readline()
  read = read.split()
  neighbours_cost[read[0]] = float(read[1])
  neighbours_port[read[0]] = int(read[2])

cur_time = time.time() #in seconds
print cur_time

try:
    t1 = Thread(target=testprint)
    packet = 'something'
    t2 = Thread(target=broadcast, kwargs={'s':s,'packet':packet,'num_of_neighbour':num_of_neighbour,'neighbours_port':neighbours_port})
    t2.daemon = True
    threads.append(t1)
    threads.append(t2)
    t1.start()
    t2.start()
    while True:
        i = 1
except KeyboardInterrupt:
    print 'keyboard interrupt triggered'
    sys.exit(1)
