import argparse

parser = argparse.ArgumentParser(description="A program to test various search algorithms for 8 and 16 puzzles.")
parser.add_argument("type", choices=["8, 16"], help="The size of the puzzle.")
parser.add_argument("start", help="The starting orientation of the puzzle (for 8 puzzles, pass in 7 unique numbers from 1 to 8, and \"-\" for the blank space).")
parser.add_argument("algorithm", choices=["dijkstras", "astar", "weighted_astar"], help="Search algorithm to run.")
args = parser.parse_args()



p = Problem()