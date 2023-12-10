# Point in polygon algorithm adapted from https://www.rosettacode.org/wiki/Ray-casting_algorithm#Python

import os
import sys

epsilon = 0.00001
huge = sys.float_info.max
tiny = sys.float_info.min

def ray_intersects_segment(point, edge):
    a, b = edge
    if a[1] > b[1]:
        a, b = b, a
    if point[1] == a[1] or point[1] == b[1]:
        point = (point[0], point[1] + epsilon)

    intersect = False

    if (point[1] > b[1] or point[1] < a[1]) or (point[0] > max(a[0], b[0])):
        return False

    if point[0] < min(a[0], b[0]):
        intersect = True
    else:
        if abs(a[0] - b[0]) > tiny:
            m_red = (b[1] - a[1]) / float(b[0] - a[0])
        else:
            m_red = huge
        if abs(a[0] - point[0]) > tiny:
            m_blue = (point[1] - a[1]) / float(point[0] - a[0])
        else:
            m_blue = huge
        intersect = m_blue >= m_red
    return intersect

def is_odd(x):
    return x % 2 == 1

def is_point_inside(point, edges):
    return is_odd(sum(ray_intersects_segment(point, edge) for edge in edges))

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

def get_next_move(current):
    node = nodes[current]
    if node.north is not None and not nodes[node.north].explored:
        return (node.north, "north")
    if node.east is not None and not nodes[node.east].explored:
        return (node.east, "east")
    if node.west is not None and not nodes[node.west].explored:
        return (node.west, "west")
    if node.south is not None and not nodes[node.south].explored:
        return (node.south, "south")

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

edges = []
current_node = start
is_first_step = True
current_edge_start = start
current_direction = None
path_points = set()

while is_first_step or current_node != start:
    is_first_step = False
    path_points.add(current_node)
    nodes[current_node].explored = True
    next_move = get_next_move(current_node)

    if next_move is None:
        break

    next_direction = next_move[1]

    if current_direction is None:
        current_direction = next_direction

    if next_direction != current_direction:
        edges.append([current_edge_start, current_node])
        current_edge_start = current_node
        current_direction = next_direction

    current_node = next_move[0]

edges.append([current_edge_start, start])

points_in_path = 0
for row in range(0, len(rows)):
    for col in range(0, len(rows[row])):
        if (row, col) in path_points:
            continue
        if is_point_inside((row, col), edges):
            points_in_path += 1

print(points_in_path)

