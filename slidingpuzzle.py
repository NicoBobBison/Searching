import argparse
import networkx as nx
from src.search import *
import copy
import random

class State:
    def __init__(self, width, state) -> None:
        self.width = width
        self.state = state

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
        blank = self.state.index("-")
        # Possible directions to move the blank
        possible_dir = [blank + 1, blank - 1, blank + self.width, blank - self.width]
        possible_dir[:] = [i for i in possible_dir if not should_remove(i)]
        
        for p in possible_dir:
            swapped = self.state[p]
            self.swap_id("-", swapped)
            neighbors.append(State(self.width, copy.deepcopy(self.state)))
            self.swap_id("-", swapped)
        return neighbors
        
    def swap_id(self, id1, id2):
        self.swap_index(self.state.index(id1), self.state.index(id2))

    def swap_index(self, index1, index2):
        temp = self.state[index1]
        self.state[index1] = self.state[index2]
        self.state[index2] = temp
    
    def __str__(self) -> str:
        if len(self.state) == 0:
            return ""
        str = ""
        for i in range(len(self.state)):
            str += f"{self.state[i]} "
            if i % self.width == self.width - 1:
                str += "\n"
        return str
    
    def __lt__(self, value: object):
        return self.__str__() < value.__str__()
    
    def __eq__(self, value: object) -> bool:
        if value is None:
            return False
        return self.state == value.state
    
    def __hash__(self) -> int:
        return hash(self.__str__())

# Counts the number of wrong cells
def wrong_count(P: Problem, node: State):
    count = 0
    for i in range(len(node.state)):
        if node.state[i] == "-":
            continue
        if i != node.state[i]:
            count += 1
    return count

# Counts the Manhattan distance between each tile with its goal position
# Much better heuristic, used by default
def manhattan_to_correct(P: Problem, node: State):
    count = 0
    for i in range(len(node.state)):
        if node.state[i] == "-":
            continue
        x_desired = i % node.width
        y_desired = i // node.width
        x_actual = int(node.state[i]) % node.width
        y_actual = int(node.state[i]) // node.width
        count += abs(x_desired - x_actual) + abs(y_desired - y_actual)
    return count

def expand(P: Problem, node):
    for neighbor in node.neighbors():
        if P.G.has_node(neighbor):
            continue
        P.G.add_node(neighbor, dist=math.inf, parent=None)
        P.G.add_edge(node, neighbor)
    return node.neighbors()

def solvable(s: State):
    count = 0
    for i in range(len(s.state)):
        for j in range(i + 1, len(s.state)):
            if s.state[i] == "-" or s.state[j] == "-":
                continue
            if int(s.state[i]) > int(s.state[j]):
                count += 1

    if s.width % 2 == 1:
        return count % 2 == 0
    else:
        blank = s.state.index("-")
        row = blank // s.width
        row_from_bottom = (s.width - row) + 1
        return (count % 2 == 0 and row_from_bottom % 2 == 1) or (count % 2 == 1 and row_from_bottom % 2 == 0)

parser = argparse.ArgumentParser(description="A program to test various search algorithms for 8 and 16 puzzles.")
parser.add_argument("type", choices=["8", "16"], help="The size of the puzzle.")
parser.add_argument("algorithm", choices=["dijkstras", "astar", "weighted_astar"], help="Search algorithm to run.")
args = parser.parse_args()

input = input(f"Enter {args.type} unique integers from 1 to {"8" if args.type == "8" else "15"} and a blank (\"-\") separated by spaces, or enter \"random\" for a random puzzle:\n")

width = 3 if args.type == "8" else 4
s = State(width, [])

if input == "random":
    config = ["-"]
    for i in range(1, width ** 2):
        config.append(str(i))
    random.shuffle(config)
    s.state = config
    while not solvable(s):
        random.shuffle(config)
        s.state = config
else:
    s.state = input.split(" ")

print(s)

if not solvable(s):
    print("This puzzle is not solvable!")
    exit()

final = State(width, [])
if width == 3:
    final.state = ["-", "1", "2", "3", "4", "5", "6", "7", "8"]
else:
    final.state = ["-", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]

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
