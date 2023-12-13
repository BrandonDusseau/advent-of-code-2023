import os
from pprint import pprint

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    raw_lines = f.readlines()

patterns = []
current_pattern = []
for raw_line in raw_lines:
    line = raw_line.strip()

    if line != "":
        current_pattern.append(list(line))
    else:
        patterns.append(current_pattern)
        current_pattern = []

if len(current_pattern) != 0:
    patterns.append(current_pattern)

def validate_horizontal_line(pattern, col):
    test_col_left = col
    test_col_right = col + 1

    while test_col_left >= 0 and test_col_right < len(pattern[0]):
        for row in range(0, len(pattern)):
            if pattern[row][test_col_left] != pattern[row][test_col_right]:
                return False

        test_col_left -= 1
        test_col_right += 1

    return True

def validate_vertical_line(pattern, row):
    test_row_above = row
    test_row_below = row + 1

    while test_row_above >= 0 and test_row_below < len(pattern):
        for col in range(0, len(pattern[0])):
            print(f"Checking ({test_row_above}, {col}) and ({test_row_below}, {col})")
            if pattern[test_row_above][col] != pattern[test_row_below][col]:
                return False

        test_row_above -= 1
        test_row_below += 1

    return True

total = 0
for pattern in patterns:
    potential_horiz_lines = list(range(0, len(pattern[0]) - 1))
    potential_vert_lines = list(range(0, len(pattern) - 1))
    for row in range(0, len(pattern) - 1):
        for col in range(0, len(pattern[row]) - 1):
            if row in potential_vert_lines and pattern[row][col] != pattern[row + 1][col]:
                potential_vert_lines.remove(row)

            if col in potential_horiz_lines and pattern[row][col] != pattern[row][col + 1]:
                potential_horiz_lines.remove(col)

    print("Potential cols for horizontal reflection:")
    pprint(potential_horiz_lines)
    print("Potential rows for vertical reflection:")
    pprint(potential_vert_lines)

    valid_horiz_lines = []
    for potential_horiz_line in potential_horiz_lines:
        if validate_horizontal_line(pattern, potential_horiz_line):
            valid_horiz_lines.append(potential_horiz_line)

    valid_vert_lines = []
    for potential_vert_line in potential_vert_lines:
        if validate_vertical_line(pattern, potential_vert_line):
            valid_vert_lines.append(potential_vert_line)

    for horiz_line in valid_horiz_lines:
        print(f"Adding {horiz_line + 1} to total for horizontal line {horiz_line}")
        total += horiz_line + 1

    for vert_line in valid_vert_lines:
        print(f"Adding {100 * (vert_line + 1)} to total for vertical line {vert_line}")
        total += 100 * (vert_line + 1)

    print(f"Valid horiz lines: {valid_horiz_lines}")
    print(f"Valid vert lines: {valid_vert_lines}")
    print()

print(total)
