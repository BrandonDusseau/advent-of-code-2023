import os

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    raw_lines = f.readlines()

def get_empty_space_between(a, b, empty_spaces):
    start = min(a, b)
    end = max(a, b)
    return len([x for x in empty_spaces if x >= start and x <= end])

rows = []
empty_rows = []
empty_cols = []
for raw_line in raw_lines:
    line = raw_line.strip()
    if line == "":
        continue
    rows.append(list(line))

for row in range(0, len(rows)):
    row_is_empty = True
    for col in range(0, len(rows[row])):
        if rows[row][col] != ".":
            row_is_empty = False
    if row_is_empty:
        empty_rows.append(row)

galaxies = []
for col in range(0, len(rows[0])):
    col_is_empty = True
    for row in range(0, len(rows)):
        if rows[row][col] != ".":
            col_is_empty = False
            galaxies.append((row, col))
    if col_is_empty:
        empty_cols.append(col)

pairs = []
for galaxy_index in range(0, len(galaxies) - 1):
    for dest_index in range(galaxy_index + 1, len(galaxies)):
        pairs.append([galaxy_index, dest_index])

distances = {}
for pair_index in range(0, len(pairs)):
    galaxy_a_index = pairs[pair_index][0]
    galaxy_b_index = pairs[pair_index][1]

    galaxy_a = galaxies[galaxy_a_index]
    galaxy_b = galaxies[galaxy_b_index]

    multiplier = 999999

    vertical_distance = abs(galaxy_b[0] - galaxy_a[0])
    empty_vert_spaces = get_empty_space_between(galaxy_a[0], galaxy_b[0], empty_rows)
    vertical_distance += empty_vert_spaces * multiplier

    horizontal_distance = abs(galaxy_b[1] - galaxy_a[1])
    empty_horiz_spaces = get_empty_space_between(galaxy_a[1], galaxy_b[1], empty_cols)
    horizontal_distance += empty_horiz_spaces * multiplier
    total_distance = vertical_distance + horizontal_distance

    distances[pair_index] = total_distance

print(sum(distances.values()))