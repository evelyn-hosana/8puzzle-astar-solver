import heapq

# h1: count tiles not in goal position (skip blank)
# admissible: each misplaced tile needs at least one move
def misplaced_tiles(state, goal):
    count = 0
    for i in range(9):
        if state[i] != 0 and state[i] != goal[i]:
            count += 1
    return count

# h2: sum of each tile's |row + column| distance from goal
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

# A* search: f(n) = g(n) + h(n)
# optimal when heuristic is admissible (both h1 and h2 are)
def astar(initial, goal, heuristic):
    # TODO: add nodes_generated counter
    # TODO: add nodes_expanded counter

    h = heuristic(initial, goal)
    # frontier: min-heap sorted by f with tie-breaker (avoid tuple comparison)
    frontier = [(h, 0, initial, 0)]
    reached = set() # tracks expanded states
    counter = 1

    # TODO: add parent tracking for path

    while frontier:
        # pop state with lowest f(n)
        f, _, state, g = heapq.heappop(frontier)

        # skip duplicate entries for states that expanded already
        if state in reached: continue
        reached.add(state)

        # goal test on expansion
        if state == goal:
            # TODO: return solution path
            return True

        # expand: evaluate neighbors with f = g + h
        for neighbor in get_neighbors(state):
            if neighbor not in reached:
                # g: parent cost + step cost
                # h: heuristic estimate to goal
                # f = g + h
                new_g = g + 1
                new_h = heuristic(neighbor, goal)
                new_f = new_g + new_h
                heapq.heappush(frontier, (new_f, counter, neighbor, new_g))
                counter += 1

    return False