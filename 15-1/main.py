import os

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    raw_lines = f.readlines()

sequence = raw_lines[0].strip().split(",")

hashes = []
for step in sequence:
    current_value = 0
    chars = list(step)
    for char in chars:
        current_value += ord(char)
        current_value *= 17
        current_value = current_value % 256
    hashes.append(current_value)
