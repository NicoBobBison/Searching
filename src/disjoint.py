from slidingpuzzle import *

# Disjoint pattern database used for sliding puzzles
class DisjointPattern:
    def __init__(self):
        self.state_cost = {}
    
    def populate(self, goal: State):
        self.state_cost = {}
        self.__store_state(goal, 0)
    
    def __store_state(self, state: State, dist):
        if self.state_cost.get(state):
            return
        self.state_cost[state] = dist
        for neighbor in state.neighbors:
            self.__store_state(neighbor, dist + 1)