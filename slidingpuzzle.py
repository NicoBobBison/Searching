import argparse
import networkx as nx
from src.search import *
import copy

class State:
    def __init__(self, width, id_to_pos, pos_to_id) -> None:
        self.width = width
        self.id_to_pos = id_to_pos
        self.pos_to_id = pos_to_id

    def neighbors(self):
        def should_remove(i):
            ## Off board
            if i >= self.width ** 2 or i < 0:
                return True
            # Wrap left
            elif blank % self.width == 0 and i == blank - 1:
                return True
            # Wrap right
            elif blank % self.width == self.width - 1 and i == blank + 1:
                return True
            return False

        neighbors = []
        blank = self.id_to_pos["-"]
        # Possible directions to move the blank
        possible_dir = [blank + 1, blank - 1, blank + self.width, blank - self.width]
        possible_dir[:] = [i for i in possible_dir if not should_remove(i)]
        
        for p in possible_dir:
            swapped = self.pos_to_id[p]
            self.swap_id("-", swapped)
            neighbors.append(State(self.width, copy.deepcopy(self.id_to_pos), copy.deepcopy(self.pos_to_id)))
            self.swap_id("-", swapped)
        return neighbors
        
    def swap_id(self, id1, id2):
        pos1 = self.id_to_pos[id1]
        pos2 = self.id_to_pos[id2]

        self.id_to_pos.pop(id1)
        self.id_to_pos.pop(id2)
        self.pos_to_id.pop(pos1)
        self.pos_to_id.pop(pos2)

        self.id_to_pos[id1] = pos2
        self.id_to_pos[id2] = pos1
        self.pos_to_id[pos1] = id2
        self.pos_to_id[pos2] = id1

    def load_config(self, config):
        for i in range(len(config)):
            self.id_to_pos[config[i]] = i
            self.pos_to_id[i] = config[i]
    
    def __str__(self) -> str:
        if len(self.id_to_pos) == 0:
            return ""
        str = ""
        keys = sorted(self.pos_to_id.keys())
        for i in range(len(keys)):
            str += f"{self.pos_to_id[keys[i]]} "
            if i % self.width == self.width - 1:
                str += "\n"
        return str
    
    def __lt__(self, value: object):
        return self.__str__() < value.__str__()
    
    def __eq__(self, value: object) -> bool:
        if value is None:
            return False
        return self.id_to_pos == value.id_to_pos
    
    def __hash__(self) -> int:
        return hash(self.__str__())

# Counts the number of wrong cells
def wrong_count(P: Problem, node: State):
    count = 0
    for i in range(len(node.pos_to_id)):
        if node.pos_to_id[i] == "-":
            continue
        if i != node.pos_to_id[i]:
            count += 1
    return count

# Counts the Manhattan distance between each tile with its goal position
# Much better heuristic, used by default
def manhattan_to_correct(P: Problem, node: State):
    count = 0
    for i in range(len(node.pos_to_id)):
        if node.pos_to_id[i] == "-":
            continue
        x_desired = i % node.width
        y_desired = i // node.width
        x_actual = int(node.pos_to_id[i]) % node.width
        y_actual = int(node.pos_to_id[i]) // node.width

        count += abs(x_desired - x_actual) + abs(y_desired - y_actual)

    return count

def expand(P: Problem, node):
    for neighbor in node.neighbors():
        if P.G.has_node(neighbor):
            continue
        P.G.add_node(neighbor, dist=math.inf, parent=None)
        P.G.add_edge(node, neighbor)
    return node.neighbors()

parser = argparse.ArgumentParser(description="A program to test various search algorithms for 8 and 16 puzzles.")
parser.add_argument("type", choices=["8", "16"], help="The size of the puzzle.")
parser.add_argument("algorithm", choices=["dijkstras", "astar", "weighted_astar"], help="Search algorithm to run.")
args = parser.parse_args()

input = input(f"Enter {args.type} unique integers from 1 to {"8" if args.type == "8" else "15"} and a blank (\"-\") separated by spaces:\n")

width = 3 if args.type == "8" else 4
s = State(width, {}, {})
s.load_config(input.split(" "))
print(s)

final = State(width, {}, {})
if width == 3:
    final.load_config(["-", "1", "2", "3", "4", "5", "6", "7", "8"])
else:
    final.load_config(["-", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"])

G = nx.Graph()
G.add_node(s)
match args.algorithm:
    case "dijkstras":
        p = Problem(G, dijkstras, False, neighbor_gen=expand)
    case "astar":
        p = Problem(G, astar, False, manhattan_to_correct, expand)
    case "weighted_astar":
        p = Problem(G, weighted_astar, False, manhattan_to_correct, expand)

path = p.search(s, final)

if path == "same":
    print("Start and end nodes are the same!")
elif len(path) == 0:
    # This should never happen
    print(f"Could not find a path between\n{s}and final state.")
else:
    print("Found path:")
    for node in path:
        print(node)
    print(f"Path length: {len(path)}")
