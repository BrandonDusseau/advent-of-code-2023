import re
import os

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

def isWord(chars, index, test):
    testLength = len(test)
    if index + testLength > len(chars):
        return False
    return "".join(chars[index:index+testLength]).lower() == test.lower()

def convertToNumber(chars, index):
    if re.match(r"[\d]", chars[index]):
        return chars[index]
    elif isWord(chars, index, "zero"):
        return 0
    elif isWord(chars, index, "one"):
        return 1
    elif isWord(chars, index, "two"):
        return 2
    elif isWord(chars, index, "three"):
        return 3
    elif isWord(chars, index, "four"):
        return 4
    elif isWord(chars, index, "five"):
        return 5
    elif isWord(chars, index, "six"):
        return 6
    elif isWord(chars, index, "seven"):
        return 7
    elif isWord(chars, index, "eight"):
        return 8
    elif isWord(chars, index, "nine"):
        return 9
    return None

numbers = []
for line in lines:
    strippedLine = line.strip()
    if strippedLine == "":
        continue

    firstNumber = None
    lastNumber = None
    chars = list(strippedLine)
    for i in range(0, len(chars)):
        result = convertToNumber(chars, i)
        if result is not None:
            if firstNumber is None:
                firstNumber = str(result)
            lastNumber = str(result)

    numbers.append(int(firstNumber + lastNumber))

print(sum(numbers))