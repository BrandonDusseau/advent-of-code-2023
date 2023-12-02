import re
import os

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

possible_id_sum = 0
max_red = 12
max_green = 13
max_blue = 14

for raw_line in lines:
    line = raw_line.strip()
    if line == "":
        continue

    game_data = line.split(": ")
    game_id = int(re.search(r"\d+", game_data[0]).group(0))

    possible = True
    pulls = game_data[1].split("; ")
    for pull in pulls:
        colors = pull.strip().split(", ")
        for color in colors:
            (count, color_name) = color.split(" ")

            if color_name.lower() == "green" and int(count) > max_green:
                possible = False
                break
            elif color_name.lower() == "red" and int(count) > max_red:
                possible = False
                break
            elif color_name.lower() == "blue" and int(count) > max_blue:
                possible = False
                break
        if not possible:
            break

    if possible:
        possible_id_sum += game_id

print(possible_id_sum)