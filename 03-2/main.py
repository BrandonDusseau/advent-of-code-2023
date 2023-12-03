import os

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

rows = []
number_map = []
gear_numbers = {}
gear_sum = 0

def locate_gear_for_number(row, start, end):
    for i in range(row - 1, row + 2):
        # Avoid going out of row bounds.
        if i < 0 or i > len(rows) - 1:
            continue

        for j in range(start - 1, end + 2):
            # Don't check the numbers.
            if i == row and j >= start and j <= end:
                continue
            # Avoid going out of column bounds.
            if j < 0 or j > len(rows[row]) - 1:
                continue

            if rows[i][j] == "*":
                return (i, j)

    return None

def create_number(row, start, end):
    return int("".join(rows[row][start:end + 1]))

for raw_line in lines:
    line = raw_line.strip()
    if line == "":
        continue

    rows.append(list(line))

# Locate the numbers and potential gears.
# The number map is a 3-tuple with format (row, col_start, col_end).
# The gear map is a dict with key in format (row, col) and value as a
# list of part numbers.
for row in range(0, len(rows)):
    row_content = rows[row]
    current_num_start = None
    for col in range(0, len(row_content)):
        # Any * is a potential gear
        if row_content[col] == "*":
            gear_numbers[(row, col)] = []

        if row_content[col].isdigit():
            if current_num_start is None:
                current_num_start = col
        else:
            if current_num_start is not None:
                number_map.append((row, current_num_start, col - 1))
                current_num_start = None
    # Handle end of row
    if current_num_start is not None:
        number_map.append((row, current_num_start, len(rows[row]) - 1))
        current_num_start = None

for num in number_map:
    located_gear = locate_gear_for_number(num[0], num[1], num[2])
    if located_gear is not None:
        gear_numbers[located_gear].append(create_number(num[0], num[1], num[2]))

for numbers in gear_numbers.values():
    if len(numbers) == 2:
        gear_sum += numbers[0] * numbers[1]

print(gear_sum)