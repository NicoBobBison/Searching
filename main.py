from matplotlib import pyplot
import networkx as nx
from src.search import *

path = "./graphs/ur.txt"
start = "i1"
end = "i10"

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
nx.draw_networkx_edges(G, pos=pos)
pyplot.show()
