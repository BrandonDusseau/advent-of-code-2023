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
    def __init__(self, current, seen, path):
        self.current = current
        self.seen = seen
        self.path = path

def get_all_paths_to_end(nodes, start, end):
    stack = [StackData(start, [], [start])]
    paths = []

    while len(stack) != 0:
        current_stack_data = stack.pop()
        current_node = nodes[current_stack_data.current]
        current_seen = current_stack_data.seen
        current_path = current_stack_data.path

        current_seen.append(current_stack_data.current)

        for neighbor in current_node.neighbors:
            if neighbor not in current_seen:
                path_to_neighbor = current_path + [neighbor]

                if neighbor == end:
                    print("Found path!")
                    paths.append(path_to_neighbor.copy())
                stack.append(StackData(neighbor, current_seen.copy(), path_to_neighbor))

    return paths

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
        if up_symbol is not None and up_symbol != "#":
            neighbors.append((row - 1, col))
        if left_symbol is not None and left_symbol != "#":
            neighbors.append((row, col - 1))
        if down_symbol is not None and down_symbol != "#":
            neighbors.append((row + 1, col))
        if right_symbol is not None and right_symbol != "#":
            neighbors.append((row, col + 1))
        positions[(row, col)] = Position(row, col, neighbors)

paths = get_all_paths_to_end(positions, start, end)
path_lengths = [len(x) - 1 for x in paths]
pprint(path_lengths)
print(max(path_lengths))