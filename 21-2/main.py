import os
from pprint import pprint

def print_grid(grid, positions):
    for row in range(0, len(grid)):
        print_row = []
        for col in range(0, len(grid[0])):
            if (row, col) in positions:
                print_row.append("O")
            else:
                print_row.append(grid[row][col])
        print("".join(print_row))
    print()

def print_positions_with_counts(position_counts):
    pprint({k: v for k, v in position_counts.items() if v > 0})
    print()

def convert_to_simple_grid(grid, row, col):
    return (row % len(grid), col % len(grid[0]))

def convert_set_to_simple(grid, positions):
    new_positions = set()
    for row, col in positions:
        new_positions.add(convert_to_simple_grid(grid, row, col))
    return new_positions

# def get_position_count(grid, positions):
#     new_positions = {}
#     for row, col in positions:
#         new_position = convert_to_simple_grid(grid, row, col)
#         if new_position in new_positions:
#             new_positions[new_position] += 1
#         else:
#             new_positions[new_position] = 1
#     return new_positions

def is_valid_move(grid, row, col):
    simple_row, simple_col = convert_to_simple_grid(grid, row, col)
    return grid[simple_row][simple_col] == "."

def get_next_steps(grid, cur_row, cur_column):
    next = []
    if is_valid_move(grid, cur_row - 1, cur_column):
        next.append((cur_row - 1, cur_column))
    if is_valid_move(grid, cur_row + 1, cur_column):
        next.append((cur_row + 1, cur_column))
    if is_valid_move(grid, cur_row, cur_column - 1):
        next.append((cur_row, cur_column - 1))
    if is_valid_move(grid, cur_row, cur_column + 1):
        next.append((cur_row, cur_column + 1))

    return next

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    raw_lines = f.readlines()

grid = []
current_positions = set()
position_counts = {}
for line_num in range(0, len(raw_lines)):
    line = raw_lines[line_num].strip()
    if line == "":
        continue
    split_line = list(line)
    row = []
    for col in range(0, len(split_line)):
        if split_line[col] == "S":
            row.append(".")
            current_positions.add((line_num, col))
            position_counts[(line_num, col)] = 1
        else:
            position_counts[(line_num, col)] = 0
            row.append(split_line[col])
    grid.append(row)

max_steps = 10
steps = 0
for i in range(0, max_steps):
    steps += 1
    print(f"Step {steps}")
    next_positions = set()
    counts_moving_into_position = {}
    for row, col in current_positions:
        current_pos_simple = convert_to_simple_grid(grid, row, col)
        count_at_current_position = position_counts[current_pos_simple]
        position_counts[current_pos_simple] = 0

        print(f"There are {count_at_current_position} elves at {current_pos_simple} across all grids")
        next_steps = get_next_steps(grid, row, col)

        for next_step in next_steps:
            next_positions.add(next_step)
            if next_step not in counts_moving_into_position:
                counts_moving_into_position[next_step] = [count_at_current_position]
            else:
                counts_moving_into_position[next_step].append(count_at_current_position)

    print("Counts moving into positions")
    pprint(counts_moving_into_position)
    for position, counts in counts_moving_into_position.items():
        simple_pos = convert_to_simple_grid(grid, position[0], position[1])
        position_counts[simple_pos] += min(counts)

    print("Positions")
    pprint(next_positions)
    print("Position counts")
    print_positions_with_counts(position_counts)

    current_positions = convert_set_to_simple(grid, next_positions)
    print()

pprint(position_counts)
print(len(current_positions))
print(sum(position_counts.values()))