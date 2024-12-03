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

# Dijkstra's shortest path searches new nodes based on their distance to the starting node
# Characteristics: Complete, optimal
def dijkstras(G: nx.Graph, start, end):
    n_count = 0
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
    # We need to store each node in a tuple (with [0] being the priority in the queue)
    # since there is no custom comparator for heapq
    heapq.heappush(frontier, (0, start))
    while len(frontier) > 0:
        popped = heapq.heappop(frontier)
        n_count += 1
        for neighbor_id in G.neighbors(popped[1]):
            neighbor = G.nodes(data=True)[neighbor_id]
            if neighbor_id == end:
                neighbor["parent"] = popped[1]
                print(f"Nodes expanded: {n_count}")
                return neighbor_id

            edge_weight = edge_length(G, popped[1], neighbor_id)
            neighbor_tuple = (G.nodes(data=True)[popped[1]]["dist"] + edge_weight, neighbor_id)
            if neighbor_tuple[0] < neighbor["dist"]:
                neighbor["dist"] = neighbor_tuple[0]
                neighbor["parent"] = popped[1]
                
            if reached.get(neighbor_id):
                continue
            heapq.heappush(frontier, neighbor_tuple)
            reached[neighbor_id] = neighbor_tuple
    print(f"Nodes expanded: {n_count}")
    return None

# A* pathfinding is like Dijkstra's, but also factors in h(x),
# the heuristic evaluation representing the distance from a node x to the end node
# Characteristics: Complete, optimal
def astar(G: nx.Graph, start, end, weight = 1):
    n_count = 0
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
        n_count += 1
        for neighbor_id in G.neighbors(popped[1]):
            neighbor = G.nodes(data=True)[neighbor_id]
            if neighbor_id == end:
                neighbor["parent"] = popped[1]
                print(f"Nodes expanded: {n_count}")
                return neighbor_id

            edge_weight = edge_length(G, popped[1], neighbor_id)
            # We need to remove the previous heuristic value (popped_h).
            popped_h = h(G, popped[1], end) * weight
            neighbor_h = h(G, neighbor_id, end) * weight
            neighbor_tuple = (G.nodes(data=True)[popped[1]]["dist"] + edge_weight + neighbor_h - popped_h, neighbor_id)

            if neighbor_tuple[0] < neighbor["dist"]:
                neighbor["dist"] = neighbor_tuple[0]
                neighbor["parent"] = popped[1]
                
            if reached.get(neighbor_id):
                continue
            heapq.heappush(frontier, neighbor_tuple)
            reached[neighbor_id] = neighbor_tuple
    print(f"Nodes expanded: {n_count}")
    return None

# Weighted A* adds more weight to h(x)
# This causes the algorithm to search fewer nodes, but it may not find the optimal path if it goes outside
# the searches contour.
# Characteristics: Complete, but not optimal (path length will be bounded by C* and W x C*, with C* the 
# length of the shortest path and W the weight)
def weighted_astar(G: nx.Graph, start, end, weight = 1.5):
    return astar(G, start, end, weight)