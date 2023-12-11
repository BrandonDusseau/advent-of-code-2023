import os

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    raw_lines = f.readlines()

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

for col in range(0, len(rows[0])):
    col_is_empty = True
    for row in range(0, len(rows)):
        if rows[row][col] != ".":
            col_is_empty = False
    if col_is_empty:
        empty_cols.append(col)

for row in reversed(empty_rows):
    rows[row:row] = [rows[row]]

galaxies = []
for row in range(0, len(rows)):
    new_row = []
    for col in range(0, len(rows[row])):
        new_row.append(rows[row][col])
        if rows[row][col] == "#":
            galaxies.append((row, len(new_row) - 1))
        if col in empty_cols:
            new_row.append(".")
    rows[row] = new_row

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

    vertical_distance = abs(galaxy_b[1] - galaxy_a[1])
    horizontal_distance = abs(galaxy_b[0] - galaxy_a[0])
    total_distance = vertical_distance + horizontal_distance

    print(f"Distance from {galaxy_a} to {galaxy_b} is {total_distance}")
    distances[pair_index] = total_distance

print(sum(distances.values()))