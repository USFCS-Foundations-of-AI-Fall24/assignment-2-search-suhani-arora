import math
from Graph import *
from search_algorithms import *

class map_state() :
    ## f = total estimated cost
    ## g = cost so far
    ## h = estimated cost to goal
    def __init__(self, location="", mars_graph=None,
                 prev_state=None, g=0,h=0):
        self.location = location
        self.mars_graph = mars_graph
        self.prev_state = prev_state
        self.g = g
        self.h = h
        self.f = self.g + self.h

    def __eq__(self, other):
        return self.location == other.location

    def __hash__(self):
        return hash(self.location)

    def __repr__(self):
        return "(%s)" % (self.location)

    def __lt__(self, other):
        return self.f < other.f

    def __le__(self, other):
        return self.f <= other.f

    def is_goal(self):
        return self.location == '1,1'

## default heuristic - we can use this to implement uniform cost search
def h1(state) :
    return 0

## you do this - return the straight-line distance between the state and (1,1)
def sld(state) :
    # sqt(a^ + b2)
    p1 = tuple(map(int, state.location.split(',')))  # Convert the location to (x, y)
    p2 = (1,1)  # Goal is (1,1)
    # Calculate the Euclidean distance
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

## you implement this. Open the file filename, read in each line,
## construct a Graph object and assign it to self.mars_graph().
def read_mars_graph(filename):
    graph = Graph()
    with open(filename, 'r') as f:
        for line in f:
            node_data = line.strip().split(':')     # separate node frome edges (:)
            node = node_data[0].strip()             # extract current node
            edges = node_data[1].strip().split()    # extract current node's edges
            
            graph.add_node(node)
            
            for e in edges:
                graph.add_edge(Edge(node, e, 1))
                
    return graph

def main():
    mars_graph = read_mars_graph("MarsMap.txt")
    s = map_state(location="5,1", mars_graph=mars_graph)

    # A* Search with SLD
    result_a_star, states_generated_a_star = a_star(startState=s, heuristic_func=sld, goal_test=map_state.is_goal)
    print(f"\nA* Search generated {states_generated_a_star} states.\n")

    # Uniform Cost Search
    result_ucs, states_generated_ucs = a_star(startState=s, heuristic_func=h1, goal_test=map_state.is_goal)
    print(f"Uniform Cost Search generated {states_generated_ucs} states.\n")

if __name__=="__main__" :
    main()