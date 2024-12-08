import math

def path_len(G, path):
    length = 0
    for i in range(len(path) - 1):
        length += node_dist(G, path[i], path[i+1])
    return length

def node_dist(G, start, end):
    return math.dist(G.nodes(data=True)[start]["pos"], G.nodes(data=True)[end]["pos"])