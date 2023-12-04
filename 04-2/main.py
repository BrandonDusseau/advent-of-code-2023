import os
import re

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

card_data = {}
card_counts = {}

max_card_num = 0
for raw_line in lines:
    line = raw_line.strip()
    if line == "":
        continue

    card_match = re.match(r"^Card\s+(?P<cardnum>\d+):\s*(?P<winningnums>(?:\d+\s*)+)\|\s*(?P<cardnums>(\d+\s*)+)", line)
    card_num = int(card_match.group("cardnum"))
    winning_numbers = card_match.group("winningnums").split()
    card_numbers = card_match.group("cardnums").split()
    card = (winning_numbers, card_numbers)
    card_data[card_num] = card
    card_counts[card_num] = 1
    max_card_num = card_num

for i in range (1, max_card_num + 1):
    matching_numbers = 0
    print(f"Processing card {i} with {card_counts[i]} copies")
    card = card_data[i]
    for num in card[1]:
        if num in card[0]:
            matching_numbers += 1
    print(f"  Matching numbers: {matching_numbers}")

    # Don't go out of bounds.
    if (i + 1 > max_card_num):
        continue

    for copy_index in range(i + 1, min(i + matching_numbers, max_card_num) + 1):
        print(f"  Making {card_counts[i]} copies of card {copy_index}")
        card_counts[copy_index] += card_counts[i]

print(f"\nTotal cards: {sum(card_counts.values())}")