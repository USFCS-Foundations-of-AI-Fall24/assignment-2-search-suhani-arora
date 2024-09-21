from collections import deque
from queue import PriorityQueue
from routefinder import *

## We will append tuples (state, "action") in the search queue
def breadth_first_search(startState, action_list, goal_test, use_closed_list=True) :
    search_queue = deque()
    closed_list = {}
    states_generated = 0

    search_queue.append((startState,""))
    if use_closed_list :
        closed_list[startState] = True
    while len(search_queue) > 0 :
        ## this is a (state, "action") tuple
        next_state = search_queue.popleft()
        states_generated += 1
        if goal_test(next_state[0]):
            print("Goal found")
            print(next_state)
            ptr = next_state[0]
            while ptr is not None :
                ptr = ptr.prev
                print(ptr)
            return next_state, states_generated
        else :
            successors = next_state[0].successors(action_list)
            if use_closed_list :
                successors = [item for item in successors
                                    if item[0] not in closed_list]
                for s in successors :
                    closed_list[s[0]] = True
            search_queue.extend(successors)
    return None, states_generated

### Note the similarity to BFS - the only difference is the search queue

## use the limit parameter to implement depth-limited search
def depth_first_search(startState, action_list, goal_test, use_closed_list=True,limit=0) :
    search_queue = deque()
    closed_list = {}
    states_generated = 0

    search_queue.append((startState,"",0)) # (state, "action", depth)
    if use_closed_list :
        closed_list[startState] = True
    while len(search_queue) > 0 :
        ## this is a (state, "action", depth) tuple
        next_state = search_queue.pop()
        states_generated += 1
        if goal_test(next_state[0]) and (next_state[2] <= limit or limit == 0):
            print("Goal found")
            print(next_state)
            ptr = next_state[0]
            while ptr is not None :
                ptr = ptr.prev
                print(ptr)
            return next_state, states_generated
        elif next_state[2] <= limit or limit == 0:
            successors = next_state[0].successors(action_list)
            if use_closed_list :
                successors = [item for item in successors
                                    if item[0] not in closed_list]
                for s in successors :
                    closed_list[s[0]] = True
            search_queue.extend([(item[0], item[1], next_state[2]+1) for item in successors])
    return None, states_generated

def subproblem_search(startState, action_list):
    total_states = 0
    
    def moveToSample(state):
        return state.sample_extracted

    result, states_generated = breadth_first_search(startState, action_list, moveToSample)
    total_states += states_generated
    print("MoveToSample States: ", states_generated)
    
    def removeSample(state):
        return state.holding_sample == False and state.holding_tool == False 
    
    result, states_generated = breadth_first_search(result[0], action_list, removeSample)
    total_states += states_generated
    print("removeSample States: ", states_generated)
    
    def returnToCharger(state):
        return state.loc == "battery" and state.charged
    
    result, states_generated = breadth_first_search(result[0], action_list, returnToCharger)
    total_states += states_generated
    print("returnToCharger States: ", states_generated)
    
    return result, total_states


def a_star(startState, heuristic_func, goal_test, use_closed_list=True) :
    search_queue = PriorityQueue()
    closed_list = {}
    states_generated = 0

    search_queue.put(startState)    
    if use_closed_list :
        closed_list[startState] = True
        
    while not search_queue.empty():
        current_state = search_queue.get()
        states_generated += 1
        if goal_test(current_state):
            return current_state, states_generated
        successors = current_state.mars_graph.get_edges(current_state.location)
        
        for edge in successors:
            next_state = map_state(edge.dest, current_state.mars_graph, current_state, current_state.g + 1)
            next_state.h = heuristic_func(next_state)  # Heuristic for next state
            next_state.f = next_state.g + next_state.h

            if use_closed_list and next_state in closed_list:
                continue

            # Add the new state to the search queue
            search_queue.put(next_state)

            if use_closed_list:
                closed_list[next_state] = True
    
    print(f"Search completed. Total states generated: {states_generated}")
    return None, states_generated