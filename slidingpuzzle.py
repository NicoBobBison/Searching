import argparse
import networkx as nx
from src.search import *
import copy

class State:
    id_to_pos = {}
    pos_to_id = {}

    def __init__(self, width, id_to_pos = {}, pos_to_id = {}) -> None:
        self.width = width
        self.id_to_pos = id_to_pos
        self.pos_to_id = pos_to_id

    def neighbors(self):
        neighbors = []
        blank = self.id_to_pos["-"]
        # Possible directions to move the blank
        possible_dir = [blank + 1, blank - 1, blank + self.width, blank - self.width]
        for p in possible_dir:
            ## Off board
            if p >= self.width ** 2 or p < 0:
                possible_dir.remove(p)
            # Wrap left
            elif blank % self.width == 0 and p == blank - 1:
                possible_dir.remove(p)
            # Wrap right
            elif blank % self.width == self.width - 1 and p == blank + 1:
                possible_dir.remove(p)
        
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
        str = ""
        keys = sorted(self.pos_to_id.keys())
        for i in range(len(keys)):
            str += f"{self.pos_to_id[keys[i]]} "
            if i % self.width == self.width - 1:
                str += "\n"
        return str

def wrong_count(P, node):
    pass

def expand(P, node):
    state = P.G.nodes(data=True)[node]["state"]


parser = argparse.ArgumentParser(description="A program to test various search algorithms for 8 and 16 puzzles.")
parser.add_argument("type", choices=["8", "16"], help="The size of the puzzle.")
parser.add_argument("algorithm", choices=["dijkstras", "astar", "weighted_astar"], help="Search algorithm to run.")
args = parser.parse_args()

input = input(f"Enter {args.type} unique integers from 1 to {"8" if args.type == "8" else "15"} and a blank (\"-\")separated by spaces:\n")

s = State(3)
s.load_config(input.split(" "))
print(s)

for n in s.neighbors():
    print(n)

G = nx.Graph()
G.add_node(s)
p = Problem(G, astar, False, wrong_count, expand)