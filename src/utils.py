import math

def edge_length(G, start, end):
    return math.dist(G.nodes(data=True)[start]["pos"], G.nodes(data=True)[end]["pos"])

def h(G, node, end):
    return edge_length(G, node, end)