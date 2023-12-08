import os
import re

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

steps = 0

directions = list(lines[0].strip())
definitions = {}
current_location = "AAA"

for raw_line in lines[2:]:
    line = raw_line.strip()
    line_match = re.match(r'^(?P<start>[A-Z]+) = \((?P<left>[A-Z]+), (?P<right>[A-Z]+)\)', line)
    if line_match is None:
        continue
    definitions[line_match.group("start")] = (line_match.group("left"), line_match.group("right"))

while current_location != "ZZZ":
    next_direction = directions[steps % len(directions)]
    if next_direction == "L":
        current_location = definitions[current_location][0]
    else:
        current_location = definitions[current_location][1]
    steps += 1

print(steps)