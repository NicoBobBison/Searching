import networkx as nx
import heapq
import math
from src.stopwatch import *
from src.utils import *

class Problem:
    # G = Graph
    # algorithm = The search algorithm to use
    # weighted = True if the graph is weighted (if false, all edges have weight = 1)
    # h = The heuristic function (for informed algorithms)
    # neighbor_gen = Function to generate neighbors of nodes. If None, we assume that the graph G is complete
    def __init__(self, G: nx.Graph, algorithm, weighted = False, h = None, neighbor_gen = None):
        self.G = G
        self.algorithm = algorithm
        self.h = h
        self.neighbor_gen = neighbor_gen
        self.weighted = weighted

    def search(self, start, end):
        s = Stopwatch()
        self.start = start
        self.end = end
        end_node = self.algorithm(self)
        path = []
        while end_node != None:
            path.insert(0, end_node)
            end_node = self.G.nodes(data=True)[end_node]["parent"]
        print(f"Searched completed in {s.get_ms()} ms")
        return path

# Dijkstra's shortest path searches new nodes based on their distance to the starting node
# Characteristics: Complete, optimal
def dijkstras(P: Problem):
    n_count = 0
    frontier = []
    reached = dict()
    # Reset distances to start    
    for node in P.G.nodes(data=True):
        if node[0] == P.start:
            node[1]["dist"] = 0
        else:
            node[1]["dist"] = math.inf
        node[1]["parent"] = None

    # Push starting node to heap
    # We need to store each node in a tuple (with [0] being the priority in the queue)
    # since there is no custom comparator for heapq
    heapq.heappush(frontier, (0, P.start))
    while len(frontier) > 0:
        popped = heapq.heappop(frontier)
        n_count += 1

        if P.neighbor_gen is None:
            n_ids = P.G.neighbors(popped[1])
        else:
            n_ids = P.neighbor_gen(P, popped[1])

        for neighbor_id in n_ids:
            neighbor = P.G.nodes(data=True)[neighbor_id]
            if neighbor_id == P.end:
                neighbor["parent"] = popped[1]
                print(f"Nodes expanded: {n_count}")
                return neighbor_id

            if P.weighted:
                edge_weight = node_dist(P.G, popped[1], neighbor_id)
            else:
                edge_weight = 1

            neighbor_tuple = (P.G.nodes(data=True)[popped[1]]["dist"] + edge_weight, neighbor_id)
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
def astar(P: Problem, weight = 1):
    n_count = 0
    frontier = []
    reached = dict()
    # Reset distances to start
    for node in P.G.nodes(data=True):
        if node[0] == P.start:
            node[1]["dist"] = P.h(P, P.start)
        else:
            node[1]["dist"] = math.inf
        node[1]["parent"] = None

    # Push starting node to heap
    heapq.heappush(frontier, (P.h(P, P.start), P.start))
    while len(frontier) > 0:
        popped = heapq.heappop(frontier)
        n_count += 1

        if P.neighbor_gen is None:
            n_ids = P.G.neighbors(popped[1])
        else:
            n_ids = P.neighbor_gen(P, popped[1])

        for neighbor_id in n_ids:
            neighbor = P.G.nodes(data=True)[neighbor_id]
            if neighbor_id == P.end:
                neighbor["parent"] = popped[1]
                print(f"Nodes expanded: {n_count}")
                return neighbor_id

            if P.weighted:
                edge_weight = node_dist(P.G, popped[1], neighbor_id)
            else:
                edge_weight = 1

            # We need to remove the previous heuristic value (popped_h).
            popped_h = P.h(P, popped[1]) * weight
            neighbor_h = P.h(P, neighbor_id) * weight
            neighbor_tuple = (P.G.nodes(data=True)[popped[1]]["dist"] + edge_weight + neighbor_h - popped_h, neighbor_id)

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
def weighted_astar(P: Problem, weight = 1.5):
    return astar(P, weight)