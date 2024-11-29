from matplotlib import pyplot
import networkx as nx

path = "monroe.txt"

graph = nx.Graph()
intersections = 0
roads = 0
file = open(path, "r")
pos = {}
for line in file:
    line = line.strip()
    list = line.split("\t")
    if list[0] == "i":
        graph.add_node(node_for_adding=list[1])
        pos[list[1]] = (float(list[2]), float(list[3]))
        intersections += 1
    elif list[0] == "r":
        graph.add_edge(u_of_edge=list[2], v_of_edge=list[3])
        roads += 1

print("Finished initializing.")
print(f"Found {intersections} intersections.")
print(f"Found {roads} roads")
nx.draw_networkx_edges(graph, pos=pos)
pyplot.show()