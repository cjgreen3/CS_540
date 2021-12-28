import heapq
import numpy as np
import copy

def print_succ(state):
    # state = np.array(state)
    succs_list = succs(state)
    # succs_list = sorted(succs_list)
    for l in succs_list:
        print(l, 'h=' + str(manhattan_heuristic(l)))
def succs(state):
    
    state_list = []
    copy = []
    index= state.index(0)

  
    if index-3 >= 0 and index-3 <= 8:
        copy = state[:]
        indexm = index-3
        copy[index], copy[indexm] = copy[indexm], copy[index]
        state_list.append(copy)

    
    copy = []
    if index+3 >= 0 and index+3 <= 8:
        copy = state[:]
        indexm = index+3
        copy[index], copy[indexm] = copy[indexm], copy[index]
        state_list.append(copy)

    
    copy = []
    if (index-1 >= 0 and index-1 <= 8) and (index-1 !=2 and index-1 != 5):
        copy = state[:]

        indexm = index-1
        copy[index], copy[indexm] = copy[indexm], copy[index]
        state_list.append(copy)

    
    copy = []
    
    if (index+1 >= 0 and index+1 <= 8) and (index+1 !=3 and index+1 != 6):
        copy = state[:]

        indexm = index+1
        copy[index], copy[indexm] = copy[indexm], copy[index]
        state_list.append(copy)

    state_list = sorted(state_list)
    return state_list


# This function was inspired by the the stack overflow answer to calculating manhattan distance
# https://stackoverflow.com/questions/39759721/calculating-the-manhattan-distance-in-the-eight-puzzle/39759853
def manhattan_heuristic(state):
    # state = list_to_np(state)
    goal_state = [1,2,3,4,5,6,7,8,0]
    s = state
    dist = 0
    for i,v in enumerate(s):
        if v != 0:
            crow,ccol = int(i/3), i % 3
            grow,gcol = int((v-1)/3), ((v-1) % 3)
            dist += abs(crow-grow) + abs(ccol-gcol)
    return dist

def print_path(open, closed):
    # check past of closed list
    # moves = 0
    # for node in closed:
    #     print(node,"moves: "+ str(moves))
        # moves += 1
    for k,v in closed.items():
        print(k, '=>', v)
    # print(closed)
        
    for node in open:
        print(node)


# This function was created with help from peer mentor Kai Wang
def solve(state):
    goal_state = [1,2,3,4,5,6,7,8,0]
    initial_state = state
   
    open = []
    # closed dic: key:str(state),value:(g,h,parent)
    closed = {}
    h = manhattan_heuristic(state)
    heapq.heappush(open,(h, state,(0,h,-1)))
    closed = {str(state):(0,h,-1)}
    parents = []
    while len(open) != 0:
        
        curr = heapq.heappop(open)
        closed[str(curr[1])] = (curr[2][0],curr[2][1],curr[2][2])
       
        if curr[1] == goal_state:
          
            while closed[str(curr[1])][2] != -1:
                parents.append(curr[1])
                # print(curr[1], curr[2][1])
                curr = closed[str(curr[1])][2]

       

            parents.reverse()
            moves = 0
            print(state, "h=" + str(manhattan_heuristic(initial_state)), "moves:",moves)
            # print(state, "h=",manhattan_heuristic(initial_state), "moves:",moves)

            moves += 1
            for l in parents:
                # print(l, "h=", manhattan_heuristic(l), "moves:",moves)

                print(l, "h=" + str(manhattan_heuristic(l)), "moves:",moves)
                moves += 1
                
            return
        succ_list = succs(curr[1])
        for s in succ_list:
            if str(s) not in closed:
                g = 1 + curr[2][0]
                h = manhattan_heuristic(s)
                
                heapq.heappush(open,(g+h, s,(g,h, curr)))

        
def convert_list(state):
    return list(state.reshape(1,9)[0])
# def main():
    # state = [1,2,3,4,5,0,6,7,8]
    # print_succ([1,2,3,4,5,0,6,7,8])
    # print_succ([8,7,6,5,4,3,2,1,0])
    # solve([4,3,8,5,1,6,7,2,0])
    # solve([1,2,3,4,5,6,7,0,8])

   

# main()