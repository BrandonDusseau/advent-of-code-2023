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

class StackData(object):
    def __init__(self, current, discovered, level):
        self.current = current
        self.discovered = discovered
        self.level = level

def print_level(msg, level):
    spaces = "".join([" " for i in range(0, level)])
    print(f"{spaces}{msg}")

def get_steps_to_end(nodes, start, end):
    stack = [StackData(start, [], 0)]
    steps_at_end = []
    while len(stack) != 0:
        current_stack_data = stack.pop()
        current_node = nodes[current_stack_data.current]
        current_discovered = current_stack_data.discovered

        if current_stack_data.current == end:
            steps_at_end.append(current_stack_data.level)

        for neighbor in current_node.neighbors:
            if neighbor in current_discovered:
                continue
            stack.append(StackData(neighbor, current_discovered + [current_stack_data.current], current_stack_data.level + 1))
    return steps_at_end

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

steps_to_end = get_steps_to_end(positions, start, end)
print(max(steps_to_end))