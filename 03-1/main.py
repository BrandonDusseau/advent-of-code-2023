import os

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

rows = []
number_map = []
part_sum = 0

def is_valid_part_number(row, start, end):
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

            if not rows[i][j].isdigit() and rows[i][j] != ".":
                return True

    return False

def create_number(row, start, end):
    return int("".join(rows[row][start:end + 1]))

for raw_line in lines:
    line = raw_line.strip()
    if line == "":
        continue

    rows.append(list(line))

# Locate the numbers
# The number map is a 3-tuple with format (row, col_start, col_end)
for row in range(0, len(rows)):
    row_content = rows[row]
    current_num_start = None
    for col in range(0, len(row_content)):
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

# Add to sum if number is valid
for num in number_map:
    if is_valid_part_number(num[0], num[1], num[2]):
        part_number = create_number(num[0], num[1], num[2])
        part_sum += part_number

print(part_sum)