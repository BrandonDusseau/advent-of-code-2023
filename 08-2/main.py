import os
import re
import math

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

directions = list(lines[0].strip())
definitions = {}

for raw_line in lines[2:]:
    line = raw_line.strip()
    line_match = re.match(r'^(?P<start>[A-Z1-9]+) = \((?P<left>[A-Z1-9]+), (?P<right>[A-Z1-9]+)\)', line)
    if line_match is None:
        continue
    definitions[line_match.group("start")] = (line_match.group("left"), line_match.group("right"))

current_locations = [x for x in definitions.keys() if x.endswith("A")]

steps = []
for current_location in current_locations:
    current_steps = 0
    while not current_location.endswith("Z"):
        next_direction = directions[current_steps % len(directions)]
        if next_direction == "L":
            current_location = definitions[current_location][0]
        else:
            current_location = definitions[current_location][1]
        current_steps += 1
    steps.append(current_steps)

print(math.lcm(*steps))