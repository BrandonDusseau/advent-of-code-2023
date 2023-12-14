import os

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    raw_lines = f.readlines()

dish = []

def print_dish():
    print()
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
        print(f"Rolling ({row}, {col}) to ({next_row}, {col})")


for raw_line in raw_lines:
    line = raw_line.strip()
    if line == "":
        continue
    dish.append(list(line))

print_dish()

for row in range(1, len(dish)):
    for col in range(0, len(dish[0])):
        if dish[row][col] != "O":
            continue
        roll_north(row, col)

total_weight = 0
dish_vert = len(dish)
for row in range(0, len(dish)):
    for col in range(0, len(dish[0])):
        if dish[row][col] == "O":
            total_weight += dish_vert - row

print_dish()
print(total_weight)