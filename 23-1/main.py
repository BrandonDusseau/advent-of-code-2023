import os
from pprint import pprint

class Position(object):
    def __init__(self, row, col, neighbors):
        self.row = row
        self.col = col
        self.neighbors = neighbors

    def get_key(self):
        return (self.row, self.col)

    def __repr__(self):
        print_neighbors = [f"({row}, {col})" for row, col in self.neighbors]
        return f"[Position ({self.row}, {self.col}) with neighbors [{', '.join(print_neighbors)}]]"

def print_level(msg, level):
    spaces = "".join([" " for i in range(0, level)])
    print(f"{spaces}{msg}")

def get_most_steps_to_end(nodes, start, end, discovered, level):
    print_level(f"Currently at ({start[0], start[1]})", level)
    if start == end:
        print_level("Found end, returning 0", level)
        return 0

    current = nodes[start]
    new_discovered = discovered + [start]
    path_steps = []
    for neighbor in current.neighbors:
        if neighbor in discovered:
            continue
        next_steps = get_most_steps_to_end(nodes, neighbor, end, new_discovered, level + 1)
        if next_steps is not None:
            path_steps.append(next_steps)

    if len(path_steps) == 0:
        print_level("No paths available, returning none", level)
        return None

    print_level(f"Found path lengths: [{', '.join([str(x) for x in path_steps])}]", level)

    return 1 + max(path_steps)

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    raw_lines = f.readlines()

grid = []
for raw_line in raw_lines:
    line = raw_line.strip()
    if line == "":
        continue
    grid.append(list(line))

positions = {}
start = None
end = None
for row in range(0, len(grid)):
    for col in range(0, len(grid[0])):
        symbol = grid[row][col]
        if symbol == "#":
            continue

        if start is None:
            start = (row, col)
        end = (row, col)

        up_symbol = grid[row - 1][col] if row > 0 else None
        left_symbol = grid[row][col - 1] if col > 0 else None
        down_symbol = grid[row + 1][col] if row < len(grid) - 1 else None
        right_symbol = grid[row][col + 1] if col < len(grid[0]) - 1 else None

        neighbors = []
        if up_symbol is not None and up_symbol != "#" and symbol not in ["<", ">", "v"]:
            neighbors.append((row - 1, col))
        if left_symbol is not None and left_symbol != "#" and symbol not in ["^", ">", "v"]:
            neighbors.append((row, col - 1))
        if down_symbol is not None and down_symbol != "#" and symbol not in ["^", "<", ">"]:
            neighbors.append((row + 1, col))
        if right_symbol is not None and right_symbol != "#" and symbol not in ["^", "<", "v"]:
            neighbors.append((row, col + 1))
        positions[(row, col)] = Position(row, col, neighbors)

print(get_most_steps_to_end(positions, start, end, [], 0))