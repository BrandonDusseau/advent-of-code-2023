import hashlib
import json
import os

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    raw_lines = f.readlines()

dish = []

def print_dish():
    for row in dish:
        print("".join(row))
    print()

def roll_north(row, col):
    next_row = row
    moved = False
    while next_row - 1 >= 0 and dish[next_row - 1][col] not in ["O", "#"]:
        moved = True
        next_row -= 1

    if moved:
        dish[row][col] = "."
        dish[next_row][col] = "O"

def roll_west(row, col):
    next_col = col
    moved = False
    while next_col - 1 >= 0 and dish[row][next_col - 1] not in ["O", "#"]:
        moved = True
        next_col -= 1

    if moved:
        dish[row][col] = "."
        dish[row][next_col] = "O"

def roll_east(row, col):
    next_col = col
    moved = False
    while next_col + 1 < len(dish[0]) and dish[row][next_col + 1] not in ["O", "#"]:
        moved = True
        next_col += 1

    if moved:
        dish[row][col] = "."
        dish[row][next_col] = "O"

def roll_south(row, col):
    next_row = row
    moved = False
    while next_row + 1 < len(dish) and dish[next_row + 1][col] not in ["O", "#"]:
        moved = True
        next_row += 1

    if moved:
        dish[row][col] = "."
        dish[next_row][col] = "O"

def run_cycle():
    for row in range(1, len(dish)):
        for col in range(0, len(dish[0])):
            if dish[row][col] != "O":
                continue
            roll_north(row, col)

    for row in range(0, len(dish)):
        for col in range(1, len(dish[0])):
            if dish[row][col] != "O":
                continue
            roll_west(row, col)

    for row in range(len(dish) - 2, -1, -1):
        for col in range(0, len(dish[0])):
            if dish[row][col] != "O":
                continue
            roll_south(row, col)

    for row in range(0, len(dish)):
        for col in range(len(dish[0]) - 2, -1, -1):
            if dish[row][col] != "O":
                continue
            roll_east(row, col)

def hash_dish():
    return hashlib.md5(json.dumps(dish).encode('utf-8')).hexdigest()

for raw_line in raw_lines:
    line = raw_line.strip()
    if line == "":
        continue
    dish.append(list(line))

dishes = []
dish_md5s = []

current_hash = None
num_cycles = 0
while current_hash not in dish_md5s[:-1]:
    run_cycle()
    current_hash = hash_dish()
    dish_md5s.append(current_hash)
    dishes.append(json.dumps(dish))
    num_cycles += 1

loop_start_index = dish_md5s.index(current_hash)
print(f"Loop found after {num_cycles} runs. Cycle starts at index {loop_start_index}.")
cycles_in_loop = num_cycles - 1 - loop_start_index
print(f"Number of cycles within loop: {cycles_in_loop}")

# (1000000000 - num_cycles - 1) excludes the last index since that's our first repeat
remaining_cycles = (1000000000 - (num_cycles - 1)) % cycles_in_loop

final_index = loop_start_index + remaining_cycles - 1
print(f"Need to run {remaining_cycles} more times to get correct result, so index is {final_index}")

total_weight = 0
final_dish = json.loads(dishes[final_index])
dish_vert = len(final_dish)
for row in range(0, len(final_dish)):
    for col in range(0, len(final_dish[0])):
        if final_dish[row][col] == "O":
            total_weight += dish_vert - row

print(total_weight)