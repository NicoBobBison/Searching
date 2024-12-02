from matplotlib import pyplot
import networkx as nx
from src.search import *

path = "./graphs/monroe.txt"
start = "i406"
end = "i5000"

G = nx.Graph()
intersections = 0
roads = 0
file = open(path, "r")
pos = {}
for line in file:
    line = line.strip()
    list = line.split("\t")
    if list[0] == "i":
        node_pos = (float(list[2]), float(list[3]))
        pos[list[1]] = node_pos
        G.add_node(node_for_adding=list[1], id=list[1], pos=node_pos)
        intersections += 1
    elif list[0] == "r":
        G.add_edge(u_of_edge=list[2], v_of_edge=list[3])
        roads += 1

print("Finished initializing.")
print(f"Found {intersections} intersections.")
print(f"Found {roads} roads")

s = Searcher(G, dijkstras)
path = s.search(start, end)
if path is None:
    print("Could not find a path")
else:
    print(f"Found path {path}")
path_edges = [(path[n], path[n+1]) for n in range(len(path) - 1)]

nx.draw_networkx_edges(G, pos=pos)
nx.draw_networkx_edges(G, pos=pos, edgelist=path_edges, width=1.5, edge_color="tab:red")
nx.draw_networkx_nodes(G, pos=pos, nodelist=[start, end], node_size=10, node_color="tab:red")
nx.draw_networkx_labels(G, pos=pos, labels={start:start, end:end}, font_color="tab:red")

pyplot.show()
