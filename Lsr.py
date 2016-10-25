#!/usr/bin/python

import socket
import pickle
import sys
import time

def broadcast(s, packet, num_of_neighbour, broadcast_port):
  for i in range(0,num_of_neighbour):
    s.sendto(packet, ('',broadcast_port))
  

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

self = sys.argv[1]
port = int(sys.argv[2])
f = open(sys.argv[3],'r')
neighbours_cost = {}
neighbours_port = {}
num_of_neighbour = f.readline()
num_of_neighbour = int(num_of_neighbour)
broadcast_port = []
for i in range (0,num_of_neighbour):
  read = f.readline()
  read = read.split()
  neighbours_cost[read[0]] = float(read[1])
  neighbours_port[read[0]] = read[2]
  broadcast_port.append(read[2])

print neighbours
print broadcast_port
cur_time = time.time() #in seconds
print cur_time
time.sleep(1)
print time.time()
# while True:
#   if (time.time()-curtime) > 1000
#     broadcast(s, packet, num_of_neighbour, broadcast_port)
#1 sec send, 30 sec print
  
