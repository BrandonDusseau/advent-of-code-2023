import os
import re
from pprint import pprint

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    raw_lines = f.readlines()

class Lens(object):
    def __init__(self, label, focal_length):
        self.label = label
        self.focal_length = focal_length

    def __repr__(self):
        return f"[{self.label} {self.focal_length}]"

sequence = raw_lines[0].strip().split(",")

boxes = []

def initialize_boxes():
    for i in range(0, 256):
        boxes.append([])

def print_boxes():
    for i in range(0, len(boxes)):
        if len(boxes[i]) != 0:
            print(f"Box {i}: {' '.join([x.__repr__() for x in boxes[i]])}")

def hash(text):
    current_value = 0
    chars = list(text)
    for char in chars:
        current_value += ord(char)
        current_value *= 17
        current_value = current_value % 256
    return current_value

def do_dash(label):
    box = hash(label)
    for i in range(0, len(boxes[box])):
        if boxes[box][i].label == label:
            del boxes[box][i]
            return

def do_equal(label, value):
    box = hash(label)
    for i in range(0, len(boxes[box])):
        if boxes[box][i].label == label:
            boxes[box][i] = Lens(label, value)
            return
    boxes[box].append(Lens(label, value))

def get_focusing_power(box_number, slot_number, focal_length):
    return (1 + box_number) * slot_number * focal_length

def get_total_focusing_power():
    total = 0
    for i in range(0, len(boxes)):
        lenses = boxes[i]
        if len(lenses) == 0:
            continue
        for j in range(0, len(lenses)):
            lens = lenses[j]
            # Slot numbers are 1-indexed
            total += get_focusing_power(i, j + 1, lens.focal_length)
    return total


hashes = []
initialize_boxes()
for step in sequence:
    match = re.match(r'(?P<label>[^-=]+)(?P<operator>[-=])(?P<value>\d+)?', step)
    label = match.group("label")
    operator = match.group("operator")
    value = int(match.group("value")) if match.group("value") is not None else None

    if operator == "-":
        do_dash(label)
    else:
        do_equal(label, value)

print(get_total_focusing_power())