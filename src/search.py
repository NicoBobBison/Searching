import networkx as nx
import heapq
import math
from src.stopwatch import *

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
        # print(popped)
        for neighbor_id in G.neighbors(popped[1]):
            neighbor = G.nodes(data=True)[neighbor_id]
            if neighbor_id == end:
                neighbor["parent"] = popped[1]
                return neighbor_id

            weight = math.dist(G.nodes(data=True)[popped[1]]["pos"], G.nodes(data=True)[neighbor_id]["pos"])
            neighbor_tuple = (G.nodes(data=True)[popped[1]]["dist"] + weight, neighbor_id)
            # print(f"Weight: {weight}")
            # print(f"New possible val: {neighbor_tuple[0]}")
            # print(f"Original val: {G.nodes(data=True)[neighbor]["dist"]}")
            if neighbor_tuple[0] < neighbor["dist"]:
                # print("Found a shorter path")
                neighbor["dist"] = neighbor_tuple[0]
                neighbor["parent"] = popped[1]
                # print(f"Set parent of {n} to {popped[1]}")
                
            if reached.get(neighbor_id):
                continue
            heapq.heappush(frontier, neighbor_tuple)
            reached[neighbor_id] = neighbor_tuple
    return None