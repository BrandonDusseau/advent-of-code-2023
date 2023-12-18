import math
import os

def polygon_area(points):
    area = 0
    for i in range(0, len(points)):
        j = (i + 1) % len(points)
        area += points[i][0] * points[j][1]
        area -= points[i][1] * points[j][0]
    return abs(area / 2)

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    raw_lines = f.readlines()

instructions = []

for raw_line in raw_lines:
    line = raw_line.strip()
    if line == "":
        continue

    split_line = line.split()

    hex_value = split_line[2]
    distance = int(hex_value[2:7], 16)
    direction_hex = hex_value[-2]

    if direction_hex == "0":
        direction = "R"
    elif direction_hex == "1":
        direction = "D"
    elif direction_hex == "2":
        direction = "L"
    else:
        direction = "U"

    instructions.append((direction, distance))

current_row = 0
current_col = 0
min_row = 0
max_row = 0
min_col = 0
max_col = 0

points = [(0, 0)]
edges = []
edge_size = 0
for instruction in instructions:
    direction = instruction[0]
    size = instruction[1]
    origin_row = current_row
    origin_col = current_col

    if direction == "R":
        current_col += size
        if current_col > max_col:
            max_col = current_col
    elif direction == "L":
        current_col -= size
        if current_col < min_col:
            min_col = current_col
    elif direction == "D":
        current_row += size
        if current_row > max_row:
            max_row = current_row
    else:
        current_row -= size
        if current_row < min_row:
            min_row = current_row

    edges.append([(origin_row, origin_col), (current_row, current_col)])
    points.append((current_row, current_col))
    edge_size += size

# Full disclosure: I don't know why this works, but it does.
print(math.floor(polygon_area(points[:-1]) + (edge_size / 2)) + 1)
