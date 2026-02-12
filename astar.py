import heapq

# h1: count tiles not in goal position (skip blank)
# admissible: each misplaced tile needs at least one move
def misplaced_tiles(state, goal):
    count = 0
    for i in range(9):
        if state[i] != 0 and state[i] != goal[i]:
            count += 1
    return count

# h2: sum of Manhattan distances (|Δrow| + |Δcol|) for each tile (skip blank)
# admissible and better than h1 (h2 >= h1); A* expands fewer nodes with h2
def manhattan_distance(state, goal):
    distance = 0
    for i in range(9):
        tile = state[i]
        if tile != 0:
            goal_pos = goal.index(tile)
            # convert 1D index to 2D (row, col) for dist calc
            curr_row, curr_col = i // 3, i % 3
            goal_row, goal_col = goal_pos // 3, goal_pos % 3
            distance += abs(curr_row - goal_row) + abs(curr_col - goal_col)
    return distance

# generate successor states by "sliding" a tile into blank space
def get_neighbors(state):
    neighbors = []
    blank = state.index(0)
    row, col = blank // 3, blank % 3
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)] # up, down, left, right
    for dr, dc in moves:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_pos = new_row * 3 + new_col
            state_list = list(state)
            state_list[blank], state_list[new_pos] = state_list[new_pos], state_list[blank]
            neighbors.append(tuple(state_list))
    return neighbors

def reconstruct_path(parent, state):
    path = []
    while state is not None:
        path.append(state)
        state = parent.get(state)
    path.reverse()
    return path

def inversion_parity(state):
    arr = [x for x in state if x != 0]
    inv = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inv += 1
    return inv % 2

def is_solvable(initial, goal):
    return inversion_parity(initial) == inversion_parity(goal)

# A* search: f(n) = g(n) + h(n)
# optimal when heuristic is admissible (both h1 and h2 are)
def astar(initial, goal, heuristic):
    if initial == goal:
        return [initial], 1, 0

    if not is_solvable(initial, goal):
        return None, 0, 0

    nodes_generated = 1         # generated = pushed into frontier (incuding start) 
    nodes_expanded = 0          # expanded = popped from frontier and processed 
    
    h = heuristic(initial, goal)
    # frontier: min-heap sorted by f with tie-breaker (avoid tuple comparison)
    frontier = [(h, 0, initial, 0)]
    reached = set() # tracks expanded states
    counter = 1

    parent = {initial: None}    # track parent of each state    
    best_g = {initial: 0}       # best known g for each state

    while frontier:
        # pop state with lowest f(n)
        f, _, state, g = heapq.heappop(frontier)

        # skip duplicate entries for states that expanded already
        if state in reached: continue
        reached.add(state)

        nodes_expanded += 1

        # goal test on expansion
        if state == goal:
            return reconstruct_path(parent, state), nodes_generated, nodes_expanded

        # expand: evaluate neighbors with f = g + h
        for neighbor in get_neighbors(state):
            new_g = g + 1
            
            # only consider this path if it is better than any previous one 
            if neighbor not in best_g or new_g < best_g[neighbor]:
                best_g[neighbor] = new_g
                parent[neighbor] = state
                
                # g: parent cost + step cost
                # h: heuristic estimate to goal
                # f = g + h
                new_h = heuristic(neighbor, goal)
                new_f = new_g + new_h
                heapq.heappush(frontier, (new_f, counter, neighbor, new_g))
                counter += 1
                nodes_generated += 1 
    return None, nodes_generated, nodes_expanded
