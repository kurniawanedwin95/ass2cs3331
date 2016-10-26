#!/usr/bin/python

import socket
import pickle
import sys
import random
from threading import Thread,Timer
import time
from collections import defaultdict

#graph implementation by Lynn Root
#https://gist.github.com/econchick/4666413
class Graph:
  def __init__(self):
    self.nodes = set()
    self.edges = defaultdict(list)
    self.distances = {}
    
  def add_node(self, value):
    self.nodes.add(value)
    
  def add_edge(self, from_node, to_node, distance):
    self.edges[from_node].append(to_node)
    self.edges[to_node].append(from_node)
    self.distances[(from_node, to_node)] = distance
    self.distances[(to_node, from_node)] = distance

  
def dijkstra(graph, initial):
  visited = {initial: 0}
  path = {}
  
  nodes = set(graph.nodes)
  
  while nodes:
    min_node = None
    for node in nodes:
      if node in visited:
        if min_node is None:
          min_node = node
        elif visited[node] < visited[min_node]:
          min_node = node
    
    if min_node is None:
      break
    
    nodes.remove(min_node)
    current_weight = visited[min_node]
    
    for edge in graph.edges[min_node]:
      weight = current_weight + graph.distances[(min_node, edge)]
      if edge not in visited or weight < visited[edge]:
        visited[edge] = weight
        path[edge] = min_node
        
  return visited, path


def broadcast(s, self, neighbours_cost, neighbours_port):
  while True:
    seq = random.randint(0,10000)
    for i, v in enumerate(neighbours_port):
        value = {'from':self,'neighbours':neighbours_cost,'seq':seq}
        packet = pickle.dumps(value)
        s.sendto(packet, ('127.0.0.1',neighbours_port[v]))#v is its neighbours
        # print value['neighbours'][v]
        print 'sent to %d' %(neighbours_port[v])
    time.sleep(1)


def rebroadcast(s, self, graph, port, neighbours_port):
  #gotta checks for incoming packet, and will rebroadcast while also adding more to the topology
  while True:
    print 'waiting for lsp'
    packet, client = s.recvfrom(1024) #lsp doesn't go over 300
    message = pickle.loads(packet)
    broadcasted_neighbour = message['neighbours']
    source = message['from']
    if source != self:
      print message
      for i, v in enumerate(broadcasted_neighbour):
        graph.add_node(v)
        graph.add_edge(message['from'],v,broadcasted_neighbour[v])
      
      for i, v in enumerate(neighbours_port):
        if v != source:
          s.sendto(packet, ('127.0.0.1',neighbours_port[v]))
          print 'rebroadcasted packet from %s' %(source)


def countShortest(self,graph):
  while True:
    dijkstra(graph, self)
    time.sleep(30)

#--------------------------------main is here----------------------------------
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

self = sys.argv[1]
port = int(sys.argv[2])
f = open(sys.argv[3],'r')
neighbours_cost = {}
neighbours_port = {}
threads = []
num_of_neighbour = f.readline()
num_of_neighbour = int(num_of_neighbour)

host=''
s.bind((host,port))


graph = Graph()
graph.add_node(self)

for i in range (0,num_of_neighbour):
  read = f.readline()
  read = read.split()
  neighbours_cost[read[0]] = float(read[1])
  neighbours_port[read[0]] = int(read[2])
  graph.add_node(read[0])
  graph.add_edge(self, read[0], float(read[1]))

print graph.edges
print graph.distances

try:
  #broadcast thread
  t1 = Thread(target=broadcast, kwargs={'s':s,'self':self,'neighbours_cost':neighbours_cost,'neighbours_port':neighbours_port})
  t1.daemon = True
  #rebroadcast thread
  t2 = Thread(target=rebroadcast, kwargs={'s':s,'self':self,'graph':graph,'port':port,'neighbours_port':neighbours_port})
  t2.daemon = True
  #dijkstra thread
  t3 = Thread(target=countShortest, kwargs={'self':self,'graph':graph})
  t3.daemon = True
  threads.append(t1)
  threads.append(t2)
  threads.append(t3)
  t1.start()
  t2.start()
  t3.start()
  while True:
      i = 1
except KeyboardInterrupt:
  print 'keyboard interrupt triggered'
  s.close()
  sys.exit(1)
