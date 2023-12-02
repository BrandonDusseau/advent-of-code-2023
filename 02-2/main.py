import os

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

power_total = 0

for raw_line in lines:
    line = raw_line.strip()
    if line == "":
        continue

    game_data = line.split(": ")

    # Setting minimums to 1 so we don't multiply by 0.
    min_red = 1
    min_blue = 1
    min_green = 1
    power = 0
    pulls = game_data[1].split("; ")
    for pull in pulls:
        colors = pull.strip().split(", ")
        for color in colors:
            (count, color_name) = color.split(" ")

            if color_name.lower() == "green" and int(count) > min_green:
                min_green = int(count)
            elif color_name.lower() == "red" and int(count) > min_red:
                min_red = int(count)
            elif color_name.lower() == "blue" and int(count) > min_blue:
                min_blue = int(count)

    power_total += min_red * min_blue * min_green

print(power_total)