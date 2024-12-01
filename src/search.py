import networkx as nx
import heapq
import math

class Searcher:
    def __init__(self, G, algorithm):
        self.G = G
        self.algorithm = algorithm

    def search(self, start, end):
        end = self.algorithm(self.G, start, end)
        path = []
        while end != None:
            path.insert(0, end)
            end = self.G.nodes(data=True)[end]["parent"]
        return path

def dijkstras(G: nx.Graph, start, end):
    print("Starting dijkstras...")
    frontier = []
    reached = dict()
    # Reset distances to start
    for node in G.nodes(data=True):
        if node == start:
            node[1]["dist"] = 0
        else:
            node[1]["dist"] = math.inf
        node[1]["parent"] = None

    # Push starting node to heap
    heapq.heappush(frontier, (0, start))
    while len(frontier) > 0:
        popped = heapq.heappop(frontier)
        print(popped)
        for neighbor in G.neighbors(popped[1]):
            if neighbor == end:
                return neighbor

            weight = math.dist(G.nodes(data=True)[popped[1]]["pos"], G.nodes(data=True)[popped[1]]["pos"])
            neighbor_tuple = (G.nodes(data=True)[popped[1]]["dist"] + weight, neighbor)
            if neighbor_tuple[0] < G.nodes(data=True)[neighbor]["dist"]:
                n = G.nodes(data=True)[neighbor[1]]
                n["dist"] = neighbor_tuple[0]
                n["parent"] = popped[1]
                
            if reached.get(neighbor):
                continue
            heapq.heappush(frontier, neighbor_tuple)
            reached[neighbor] = neighbor_tuple
    return None