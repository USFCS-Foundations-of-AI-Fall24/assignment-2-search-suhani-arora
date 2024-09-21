## actions:
## pick up tool
## move_to_sample
## use_tool
## move_to_station
## drop_tool
## drop_sample
## move_to_battery
## charge

## locations: battery, sample, station
## holding_sample can be True or False
## holding_tool can be True or False
## Charged can be True or False

from copy import deepcopy
from search_algorithms import breadth_first_search, depth_first_search, subproblem_search

class RoverState :
    def __init__(self, loc="station", sample_extracted=False, holding_sample=False, holding_tool=False, charged=False):
        self.loc = loc
        self.sample_extracted=sample_extracted
        self.holding_sample = holding_sample
        self.holding_tool = holding_tool
        self.charged=charged
        self.prev = None

    ## you do this.
    def __eq__(self, other):
       return (self.loc == other.loc and 
               self.sample_extracted == other.sample_extracted and
               self.holding_sample == other.holding_sample and
               self.holding_tool == other.holding_tool and
               self.charged == other.charged)


    def __repr__(self):
        return (f"Location: {self.loc}\n" +
                f"Sample Extracted?: {self.sample_extracted}\n"+
                f"Holding Sample?: {self.holding_sample}\n" +
                f"Holding Tool?: {self.holding_tool}\n" +
                f"Charged? {self.charged}")

    def __hash__(self):
        return self.__repr__().__hash__()

    def successors(self, list_of_actions):

        ## apply each function in the list of actions to the current state to get
        ## a new state.
        ## add the name of the function also
        succ = [(item(self), item.__name__) for item in list_of_actions]
        ## remove actions that have no effect

        succ = [item for item in succ if not item[0] == self]
        return succ

## our actions will be functions that return a new state.

def move_to_sample(state) :
    r2 = deepcopy(state)
    r2.loc = "sample"
    r2.prev=state
    return r2
def move_to_station(state) :
    r2 = deepcopy(state)
    r2.loc = "station"
    r2.prev = state
    return r2

def move_to_battery(state) :
    r2 = deepcopy(state)
    r2.loc = "battery"
    r2.prev = state
    return r2
# add tool functions here

def pick_up_tool(state) :
    r2 = deepcopy(state)
    if state.loc == "station" and state.sample_extracted == False:
        r2.holding_tool = True
    r2.prev = state
    return r2

def drop_tool(state) :
    r2 = deepcopy(state)
    if state.loc == "station" and state.sample_extracted:
        r2.holding_tool = False
    r2.prev = state
    return r2

def use_tool(state) :
    r2 = deepcopy(state)
    if state.loc == "sample" and state.holding_tool:
        r2.sample_extracted = True
    r2.prev = state
    return r2

def pick_up_sample(state) :
    r2 = deepcopy(state)
    if state.sample_extracted and state.loc == "sample":
        r2.holding_sample = True
    r2.prev = state
    return r2

def drop_sample(state) :
    r2 = deepcopy(state)
    if state.sample_extracted and state.loc == "station":
        r2.holding_sample = False
    r2.prev = state
    return r2

def charge(state) :
    r2 = deepcopy(state)
    if state.sample_extracted and state.loc == "battery":
        r2.charged = True
    r2.prev = state
    return r2


action_list = [charge, drop_sample, pick_up_sample,
               move_to_sample, move_to_battery, move_to_station, pick_up_tool, drop_tool, use_tool]

def battery_goal(state) :
    return state.loc == "battery"
## add your goals here.

def mission_complete(state) :
    return (state.loc == "battery" and
            state.charged == True and
            state.sample_extracted == True and
            state.holding_tool == False and
            state.holding_sample == False)

def main():
    s = RoverState()
    result_bfs, states_generated_bfs = breadth_first_search(s, action_list, mission_complete)
    print(f"\n** Results for Breadth First Search: \n{result_bfs}\nTotal BFS States Generated: {states_generated_bfs}\n", "\n_______________________________________\n")

    result_dfs, states_generated_dfs = depth_first_search(s, action_list, mission_complete)
    print(f"\n** Results for Depth First Search: \n{result_dfs}\nTotal DFS States Generated: {states_generated_dfs}\n", "\n_______________________________________\n")

    result_dls, states_generated_dls = depth_first_search(s, action_list, mission_complete, True,limit=7)
    print(f"\n** Results for Depth Limited Search; Limit = 7\n{result_dls}\nTotal DLS States Generated: {states_generated_dls}\n", "\n_______________________________________\n")

    result_subs, states_generated_subs = subproblem_search(s, action_list)
    print(f"\n** Results for Subproblem Search:\n{result_subs}\nTotal Subproblem States Generated: {states_generated_subs}\n", "\n_______________________________________\n")
    
    print(f"\n** Q2 Summmary **\n\nBreadth First Search generated {states_generated_bfs} states.\n")
    print(f"Depth First Search generated {states_generated_dfs} states.\n")
    print(f"Depth Limited Search generated {states_generated_dls} states.\n")
    print(f"Subproblem Search generated {states_generated_subs} states.\n")
    
if __name__=="__main__" :
    main()
