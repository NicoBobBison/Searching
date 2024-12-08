import argparse
import networkx as nx
from search import *

class State:
    id_to_pos = {}
    pos_to_id = {}

    def __init__(self, width, id_to_pos = {}, pos_to_id = {}) -> None:
        self.size = width
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
            if p % self.width == 0 and p == blank - 1:
                possible_dir.remove(p)
            # Wrap right
            if p % self.width == self.width - 1 and p == blank + 1:
                possible_dir.remove(p)
        
        for p in possible_dir:
            swapped = self.pos_to_id[p]
            self.swap("-", swapped)
            neighbors.append(State(self.width, self.id_to_pos, self.pos_to_id))
            self.swap("-", swapped)
        return neighbors
    
    def swap(self, id1, id2):
        pass

    def load_config(self, config):
        for i in range(len(config)):
            self.id_to_pos[config[i]] = i
            self.pos_to_id[i] = config[i]

def h(P, node):
    pass

def expand(P, node):
    state = P.G.nodes(data=True)[node]["state"]


parser = argparse.ArgumentParser(description="A program to test various search algorithms for 8 and 16 puzzles.")
parser.add_argument("type", choices=["8", "16"], help="The size of the puzzle.")
parser.add_argument("start", help="The starting orientation of the puzzle (for 8 puzzles, pass in 7 unique numbers from 1 to 8, and \"-\" for the blank space).")
parser.add_argument("algorithm", choices=["dijkstras", "astar", "weighted_astar"], help="Search algorithm to run.")
args = parser.parse_args()

G = nx.Graph()
p = Problem(G, astar, False, h, expand)