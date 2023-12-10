import os

class Node(object):
    def __init__(self, row, col, type, north, south, east, west):
        self.row = row
        self.col = col
        self.type = type
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.explored = False

    def __repr__(self):
        return f"[{self.row}, {self.col}, {self.type}, [N:{self.north}, W:{self.west}, S:{self.south}, E:{self.east}]]"

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    raw_lines = f.readlines()

rows = []
for raw_line in raw_lines:
    line = raw_line.strip()
    if line == "":
        continue
    rows.append(list(line))

def can_travel_north(row, col):
    return row != 0 and rows[row - 1][col] in ["|", "7", "F", "S"]

def can_travel_west(row, col):
    return col != 0 and rows[row][col - 1] in ["-", "L", "F", "S"]

def can_travel_east(row, col):
    return col != len(rows[row]) - 1 and rows[row][col + 1] in ["-", "J", "7", "S"]

def can_travel_south(row, col):
    return row != len(rows) - 1 and rows[row + 1][col] in ["|", "L", "J", "S"]

def get_next_move(current, skip=None):
    node = nodes[current]
    if node.north is not None and skip != node.north and not nodes[node.north].explored:
        return node.north
    if node.east is not None and skip != node.east and not nodes[node.east].explored:
        return node.east
    if node.west is not None and skip != node.west and not nodes[node.west].explored:
        return node.west
    if node.south is not None and skip != node.south and not nodes[node.south].explored:
        return node.south

    return None

def determine_start_type(row, col):
    north = can_travel_north(row, col)
    west = can_travel_west(row, col)
    east = can_travel_east(row, col)
    south = can_travel_south(row, col)

    if north and south:
        return "|"
    if east and west:
        return "-"
    if north and east:
        return "L"
    if north and west:
        return "J"
    if south and west:
        return "7"
    if south and east:
        return "F"

    print("Start tile is not valid")
    exit(1)

nodes = {}
start = None
for row in range(0, len(rows)):
    for col in range(0, len(rows[row])):
        type = rows[row][col]
        if type == ".":
            continue
        if type == "S":
            start = (row, col)
            type = determine_start_type(row, col)

        north = (row - 1, col) if can_travel_north(row, col) and type in ["|", "L", "J"] else None
        west = (row, col - 1) if can_travel_west(row, col) and type in ["-", "7", "J"] else None
        south = (row + 1, col) if can_travel_south(row, col) and type in ["|", "F", "7"] else None
        east = (row, col + 1) if can_travel_east(row, col) and type in ["-", "F", "L"] else None

        nodes[(row, col)] = Node(row, col, type, north, south, east, west)

steps = 0
current_node_a = start
current_node_b = start

while current_node_a == start or (current_node_a is not None and current_node_b is not None):
    nodes[current_node_a].explored = True
    nodes[current_node_b].explored = True
    current_node_a = get_next_move(current_node_a)
    current_node_b = get_next_move(current_node_b, current_node_a)
    print(f"Moving to {current_node_a} and {current_node_b}")
    steps += 1

print("Out of moves!")
print(steps)