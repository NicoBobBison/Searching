import networkx as nx
import heapq
import math
from src.stopwatch import *
from src.utils import *

class Searcher:
    def __init__(self, G, algorithm):
        self.G = G
        self.algorithm = algorithm

    def search(self, start, end):
        s = Stopwatch()
        end = self.algorithm(self.G, start, end)
        path = []
        while end != None:
            path.insert(0, end)
            end = self.G.nodes(data=True)[end]["parent"]
        print(f"Searched completed in {s.get_ms()} ms")
        return path

    def path_len(self, path):
        length = 0
        for i in range(len(path) - 1):
            length += edge_length(self.G, path[i], path[i+1])
        return length

def dijkstras(G: nx.Graph, start, end):
    frontier = []
    reached = dict()
    # Reset distances to start
    for node in G.nodes(data=True):
        if node[0] == start:
            node[1]["dist"] = 0
        else:
            node[1]["dist"] = math.inf
        node[1]["parent"] = None

    # Push starting node to heap
    heapq.heappush(frontier, (0, start))
    while len(frontier) > 0:
        popped = heapq.heappop(frontier)
        for neighbor_id in G.neighbors(popped[1]):
            neighbor = G.nodes(data=True)[neighbor_id]
            if neighbor_id == end:
                neighbor["parent"] = popped[1]
                return neighbor_id

            weight = edge_length(G, popped[1], neighbor_id)
            neighbor_tuple = (G.nodes(data=True)[popped[1]]["dist"] + weight, neighbor_id)
            if neighbor_tuple[0] < neighbor["dist"]:
                neighbor["dist"] = neighbor_tuple[0]
                neighbor["parent"] = popped[1]
                
            if reached.get(neighbor_id):
                continue
            heapq.heappush(frontier, neighbor_tuple)
            reached[neighbor_id] = neighbor_tuple
    return None

def astar(G: nx.Graph, start, end):
    frontier = []
    reached = dict()
    # Reset distances to start
    for node in G.nodes(data=True):
        if node[0] == start:
            node[1]["dist"] = h(G, start, end)
        else:
            node[1]["dist"] = math.inf
        node[1]["parent"] = None

    # Push starting node to heap
    heapq.heappush(frontier, (h(G, start, end), start))
    while len(frontier) > 0:
        popped = heapq.heappop(frontier)
        for neighbor_id in G.neighbors(popped[1]):
            neighbor = G.nodes(data=True)[neighbor_id]
            if neighbor_id == end:
                neighbor["parent"] = popped[1]
                return neighbor_id

            weight = edge_length(G, popped[1], neighbor_id)
            neighbor_tuple = (G.nodes(data=True)[popped[1]]["dist"] + weight + h(G, neighbor_id, end), neighbor_id)
            if neighbor_tuple[0] < neighbor["dist"]:
                neighbor["dist"] = neighbor_tuple[0]
                neighbor["parent"] = popped[1]
                
            if reached.get(neighbor_id):
                continue
            heapq.heappush(frontier, neighbor_tuple)
            reached[neighbor_id] = neighbor_tuple
    return None
