import os
import re

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

points = 0
for raw_line in lines:
    line = raw_line.strip()
    if line == "":
        continue

    card_points = 0
    is_first_match = True
    card_match = re.match(r"^Card\s+\d+:\s*(?P<winningnums>(?:\d+\s*)+)\|\s*(?P<cardnums>(\d+\s*)+)", line)
    winning_numbers = card_match.group("winningnums").split()
    card_numbers = card_match.group("cardnums").split()

    for num in card_numbers:
        if num in winning_numbers:
            if is_first_match:
                is_first_match = False
                card_points += 1
            else:
                card_points *= 2
    points += card_points

print(points)
