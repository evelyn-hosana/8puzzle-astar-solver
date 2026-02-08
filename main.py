def validate_puzzle_input(input_string):
    # checks if puzzle input is valid
    # format example: "7 2 4 5 _ 6 8 3 1" (digits 1-8 + underscore for blank)

    # clean up and split
    elements = input_string.strip().split()

    # need exactly 9 elements
    if len(elements) != 9:
        return False, f"Error: Expected 9 elements, but got {len(elements)}"

    # no commas
    if ',' in input_string:
        return False, "Error: Use spaces to separate elements, not commas"

    # check blank space
    underscore_count = elements.count('_')
    if underscore_count == 0:
        return False, "Error: Missing blank space '_'"
    elif underscore_count > 1:
        return False, f"Error: Found {underscore_count} blank spaces, need exactly 1"

    # grab just digits
    digits = [elem for elem in elements if elem != '_']

    # need 8 digits
    if len(digits) != 8:
        return False, "Error: Must have exactly 8 digits and 1 blank space"

    # validate each digit
    for digit in digits:
        if not digit.isdigit():
            return False, f"Error: '{digit}' is not a valid digit"
        if digit == '0':
            return False, "Error: Use '_' for blank space, not '0'"
        if int(digit) < 1 or int(digit) > 8:
            return False, f"Error: '{digit}' is out of range (use 1-8)"

    # no duplicates allowed
    digit_set = set(digits)
    if len(digit_set) != 8:
        return False, "Error: Each digit 1-8 must appear exactly once"

    # make sure 1-8 are all there
    expected_digits = set('12345678')
    if digit_set != expected_digits:
        missing = expected_digits - digit_set
        return False, f"Error: Missing digit(s): {', '.join(sorted(missing))}"

    return True, "Correct string format!"


def main():
    # request initial state from user input, validate it and return if valid
    initial_input = input("Enter the initial state: ").strip()
    is_valid, message = validate_puzzle_input(initial_input)
    print(message)

    if not is_valid:
        return None, None

    # request goal state from user input, validate it and return if valid
    goal_input = input("Enter the goal state: ").strip()
    is_valid, message = validate_puzzle_input(goal_input)
    print(message)

    if not is_valid:
        return initial_input, None

    # initial and goal states must be different
    if initial_input == goal_input:
        print("Error: Initial state and goal state cannot be the same")
        return None, None

    return initial_input, goal_input

if __name__ == "__main__":
    main()