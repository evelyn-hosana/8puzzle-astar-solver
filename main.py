from astar import astar, misplaced_tiles, manhattan_distance

# checks if puzzle input is valid
def validate_puzzle_input(input_string):
    """Validate a 3x3 8-puzzle state. Returns (ok, state_tuple, message)."""
    # format example: "1 2 3 4 5 6 7 8 0" (0 considered blank space)
    elements = input_string.strip().split() # cleanup and split

    # need exactly 9 elements
    if len(elements) != 9:
        return False, None, f"Error: Expected 9 elements, but got {len(elements)}"

    # no commas
    if ',' in input_string:
        return False, None, "Error: Use spaces to separate elements, not commas"

    # validate all elements are digits
    for elem in elements:
        if not elem.isdigit():
            return False, None, f"Error: '{elem}' is not a valid digit"
        if int(elem) < 0 or int(elem) > 8:
            return False, None, f"Error: '{elem}' is out of range (use 0-8)"

    # extra validation: exactly one '0'
    zero_count = elements.count('0')
    if zero_count == 0:
        return False, None, "Error: Missing blank space '0'"
    elif zero_count > 1:
        return False, None, f"Error: Found {zero_count} blank spaces, need exactly 1"

    # no duplicates allowed
    digit_set = set(elements)
    if len(digit_set) != 9:
        return False, None, "Error: Each digit 0-8 must appear exactly once"

    # extra validation: check all digits exist
    expected_digits = set('012345678')
    if digit_set != expected_digits:
        missing = expected_digits - digit_set
        return False, None, f"Error: Missing digit(s): {', '.join(sorted(missing))}"

    # return state as tuple of integers for easier processing
    state = tuple(int(e) for e in elements)
    return True, state, "Valid input!"

# function that prints puzzle states as 3x3 board
def print_board(state):
    for i in range(0, 9, 3):
        row = state[i:i+3]
        print(" ".join(str(x) if x != 0 else "_" for x in row))
    print()

def print_results(title, path, generated, expanded):
    print(f"\n=== {title} ===")
    if path is None:
        print("No solution found.")
    else:
        print(f"Moves: {len(path) - 1}")
        print("Solution path:")
        for step, state in enumerate(path):
            print(f"Step {step}:")
            print_board(state)

    print(f"Nodes generated: {generated}")
    print(f"Nodes expanded:  {expanded}")

def main():
    # request initial state from user input, validate it and return if valid
    initial_input = input("Enter the initial state: ").strip()
    is_valid, initial_state, message = validate_puzzle_input(initial_input)
    print(message)
    if not is_valid: return None, None

    # request goal state from user input, validate it and return if valid
    goal_input = input("Enter the goal state: ").strip()
    is_valid, goal_state, message = validate_puzzle_input(goal_input)
    print(message)
    if not is_valid: return None, None

    # if start equals goal, report and skip running A*
    if initial_state == goal_state:
        print("Initial state is already the goal state.")
        print("Moves: 0")
        print("Solution path:")
        print_board(initial_state)
        return initial_state, goal_state
    
    return initial_state, goal_state

if __name__ == "__main__":
    while True:
        initial_state, goal_state = main()

        if initial_state is None or goal_state is None:
            print("Invalid input: Cannot run A* search")
        else:
            path1, gen1, exp1 = astar(initial_state, goal_state, misplaced_tiles)
            path2, gen2, exp2 = astar(initial_state, goal_state, manhattan_distance)

            print_results(" Misplaced Tiles (h1)", path1, gen1, exp1)
            print_results(" Manhattan Distance (h2)", path2, gen2, exp2)

        again = input("\nRun again? (y/n): ").strip().lower()
        if again != "y":
            break
