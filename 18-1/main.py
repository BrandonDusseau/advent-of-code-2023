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

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    raw_lines = f.readlines()

instructions = []
grid = [["#"]]

for raw_line in raw_lines:
    line = raw_line.strip()
    if line == "":
        continue

    split_line = line.split()
    instructions.append((split_line[0], int(split_line[1])))

def print_grid():
    for row in range(0, len(grid)):
        print("".join(grid[row]))
    print()

def expand_horiz_to(index):
    current_max_index = len(grid[0]) - 1

    if index > 0:
        difference = index - current_max_index
        if difference <= 0:
            return 0
        print(f"Expanding horizontally rightward by {difference} to {index}")
        for row in range(0, len(grid)):
            grid[row] = grid[row] + ["." for x in range(0, difference - 1)]
        return difference
    else:
        print(f"Expanding horizontally leftward by {index} to {index}")
        for row in range(0, len(grid)):
            grid[row] = ["." for x in range(index, 0)] + grid[row]
        return index

def expand_vert_to(index):
    current_max_index = len(grid) - 1
    current_width = len(grid[0])

    if index > 0:
        difference = index - current_max_index
        if difference <= 0:
            return 0

        print(f"Expanding vertically downward by {difference} to {index}")
        for i in range(0, difference - 1):
            grid.append(["." for x in range(0, current_width)])
        return difference
    else:
        print(f"Expanding vertically upward by {index} to {index}")
        for i in range(index, 0):
            grid.insert(0, ["." for x in range(0, current_width)])
        return index

def adjust_edges(edges, row_shift, col_shift):
    if row_shift > 0:
        row_shift = 0
    if col_shift > 0:
        col_shift = 0

    for edge in edges:
        edge[0] = (edge[0][0] + -row_shift, edge[0][1] + -col_shift)
        edge[1] = (edge[1][0] + -row_shift, edge[1][1] + -col_shift)

current_row = 0
current_col = 0
edges = []
for instruction in instructions:
    direction = instruction[0]
    size = instruction[1]
    origin_row = current_row
    origin_col = current_col

    row_shift = 0
    col_shift = 0

    print(f"Moving {size} in direction {direction}")

    if direction == "R":
        expand_horiz_to(current_col + size + 1)
        for i in range(0, size):
            current_col += 1
            grid[current_row][current_col] = "#"
    elif direction == "L":
        col_shift = expand_horiz_to(current_col - size)
        current_col += -col_shift
        origin_col += -col_shift
        print(f"Current column is now {current_col}")
        for i in range(0, size):
            current_col -= 1
            grid[current_row][current_col] = "#"
    elif direction == "D":
        expand_vert_to(current_row + size + 1)
        for i in range(0, size):
            current_row += 1
            grid[current_row][current_col] = "#"
    else:
        row_shift = expand_vert_to(current_row - size)
        current_row += -row_shift
        origin_row += -row_shift
        for i in range(0, size):
            current_row -= 1
            grid[current_row][current_col] = "#"

    adjust_edges(edges, row_shift, col_shift)
    edges.append([(origin_row, origin_col), (current_row, current_col)])

print_grid()
path_points = set()
for edge in edges:
    for row in range(edge[0][0], edge[1][0] + 1):
        for col in range(edge[0][1], edge[1][1] + 1):
            path_points.add((row, col))

points_in_path = 0
for row in range(0, len(grid)):
    for col in range(0, len(grid[row])):
        if (row, col) in path_points:
            continue
        if is_point_inside((row, col), edges):
            points_in_path += 1

print(points_in_path + len(path_points))

