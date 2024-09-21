import mars_planner, routefinder, search_algorithms, Graph, antenna_freq
from mars_planner import *
from routefinder import *
from Graph import *
from search_algorithms import *


# -- Question 2
print("\n(Question 2)")
mars_planner.main()

# -- Question 3
print("\n(Question 3)")
mars_graph = read_mars_graph("MarsMap.txt")
s = map_state(location="5,1", mars_graph=mars_graph)

    # A* Search with SLD
result_a_star, states_generated_a_star = a_star(startState=s, heuristic_func=sld, goal_test=map_state.is_goal)
print(f"\nA* Search generated {states_generated_a_star} states.\n")

    # Uniform Cost Search
result_ucs, states_generated_ucs = a_star(startState=s, heuristic_func=h1, goal_test=map_state.is_goal)
print(f"Uniform Cost Search generated {states_generated_ucs} states.\n")


# -- Question 4
print("\n(Question 4)\n")
antenna_freq.main()
