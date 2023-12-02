import re
import os

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

numbers = []
for line in lines:
    strippedLine = line.strip()
    if strippedLine == "":
        continue

    firstNumber = None
    lastNumber = None
    for char in list(strippedLine):
        if re.match(r"[\d]", char):
            if firstNumber is None:
                firstNumber = char
            lastNumber = char
    numbers.append(int(firstNumber + lastNumber))

print(sum(numbers))