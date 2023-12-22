import os

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

def is_valid_move(grid, row, col):
    return row >= 0 and row < len(grid) and col >= 0 and col < len(grid[row]) and grid[row][col] == "."

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
        else:
            row.append(split_line[col])
    grid.append(row)

max_steps = 10
for i in range(0, max_steps):
    next_positions = set()
    for row, col in current_positions:
        for next_pos in get_next_steps(grid, row, col):
            next_positions.add(next_pos)
    current_positions = next_positions

print(len(current_positions))