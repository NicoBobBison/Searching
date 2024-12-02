from matplotlib import pyplot
import networkx as nx
import argparse
from src.search import *

parser = argparse.ArgumentParser(description="A program to test various search algorithms.")
parser.add_argument("filepath", help="File path to raw graph data (stored in ./graphs/___.txt).")
parser.add_argument("start", help="Name of starting intersection.")
parser.add_argument("end", help="Name of ending intersection.")
parser.add_argument("--map", help="Shows an image of the map and shortest path.", action="store_true")
args = parser.parse_args()

G = nx.Graph()
intersections = 0
roads = 0
file = open(args.filepath, "r")
pos = {}
for line in file:
    line = line.strip()
    list = line.split("\t")
    if list[0] == "i":
        node_pos = (float(list[3]), float(list[2]))
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
path = s.search(args.start, args.end)
if len(path) == 0:
    print(f"Could not find a path between {args.start} and {args.end}")
else:
    print(f"Found path {path}")
path_edges = [(path[n], path[n+1]) for n in range(len(path) - 1)]

if args.map:
    nx.draw_networkx_edges(G, pos=pos)
    nx.draw_networkx_edges(G, pos=pos, edgelist=path_edges, width=1.5, edge_color="tab:red")
    nx.draw_networkx_nodes(G, pos=pos, nodelist=[args.start, args.end], node_size=10, node_color="tab:red")
    nx.draw_networkx_labels(G, pos=pos, labels={args.start:args.start, args.end:args.end}, font_color="tab:red")

    pyplot.show()
