import importlib
from matplotlib import pyplot
import networkx as nx
import argparse
import src.search
from src.search import *

parser = argparse.ArgumentParser(description="A program to test various search algorithms.")
parser.add_argument("filepath", help="File path to raw graph data (stored in ./graphs/___.txt).")
parser.add_argument("start", help="Name of starting intersection.")
parser.add_argument("end", help="Name of ending intersection.")
parser.add_argument("algorithm", choices=["dijkstras", "astar", "weighted_astar"], help="Search algorithm to run.")
parser.add_argument("--map", help="Shows an image of the map and shortest path.", action="store_true")
parser.add_argument("--fullpath", help="Shows the full path found.", action="store_true")
args = parser.parse_args()

print("Initializing graph...")
watch = Stopwatch()
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

print(f"Finished initializing in {watch.get_ms()} ms")
print(f"Found {intersections} intersections.")
print(f"Found {roads} roads")

s = Searcher(G, getattr(src.search, args.algorithm))
path = s.search(args.start, args.end)
path_edges = [(path[n], path[n+1]) for n in range(len(path) - 1)]

if len(path) == 0:
    print(f"Could not find a path between {args.start} and {args.end}")
else:
    if args.fullpath or len(path) <= 4:
        print(f"Found path {path}")
    else:
        print(f"Found path [{path[0]}, {path[1]}, ... , {path[len(path) - 2]}, {path[len(path) - 1]}]")
    print(f"Path length: {s.path_len(path)}")

if args.map:
    nx.draw_networkx_edges(G, pos=pos)
    if len(path) > 0:
        nx.draw_networkx_edges(G, pos=pos, edgelist=path_edges, width=2, edge_color="tab:red")
        nx.draw_networkx_nodes(G, pos=pos, nodelist=[args.start, args.end], node_size=10, node_color="tab:red")
        # nx.draw_networkx_labels(G, pos=pos, labels={args.start:args.start, args.end:args.end}, font_color="tab:red")

    pyplot.show()
