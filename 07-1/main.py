import os

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

hands = {}
ranked_hands = []

card_strengths = {
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 5,
    "7": 6,
    "8": 7,
    "9": 8,
    "T": 9,
    "J": 10,
    "Q": 11,
    "K": 12,
    "A": 13
}

def get_card_counts(hand):
    counts = {}
    for card in hand:
        counts[card] = 1 if card not in counts else counts[card] + 1
    return counts

def is_five_kind(hand):
    counts = get_card_counts(hand).values()
    return 5 in counts and len(counts) == 1

def is_four_kind(hand):
    counts = get_card_counts(hand).values()
    return 4 in counts and len(counts) == 2

def is_full_house(hand):
    counts = get_card_counts(hand).values()
    return 3 in counts and 2 in counts and len(counts) == 2

def is_three_kind(hand):
    counts = get_card_counts(hand).values()
    return 3 in counts and len(counts) > 2

def is_two_pair(hand):
    counts = get_card_counts(hand).values()
    pairs = [x for x in counts if x == 2]
    return len(pairs) == 2 and len(counts) == 3

def is_one_pair(hand):
    counts = get_card_counts(hand).values()
    return 2 in counts and len(counts) == 4

def get_hand_strength(hand):
    if is_five_kind(hand):
        return 7
    elif is_four_kind(hand):
        return 6
    elif is_full_house(hand):
        return 5
    elif is_three_kind(hand):
        return 4
    elif is_two_pair(hand):
        return 3
    elif is_one_pair(hand):
        return 2
    else:
        return 1

def is_hand_better(hand_key, other_hand_key):
    hand_type_strength = hands[hand_key][2]
    other_hand_type_strength = hands[other_hand_key][2]
    if hand_type_strength > other_hand_type_strength:
        return True
    elif hand_type_strength < other_hand_type_strength:
        return False

    # For same hand type, check strength of each card.
    for card_index in range(0, 5):
        hand_card_strength = hands[hand_key][0][card_index]
        other_hand_card_strength = hands[other_hand_key][0][card_index]
        if hand_card_strength > other_hand_card_strength:
            return True
        if hand_card_strength < other_hand_card_strength:
            return False

    # Two hands shouldn't be the same, but...
    return False

for i in range(0, len(lines)):
    line = lines[i].strip()
    if line == "":
        continue

    (hand, bid) = line.split()
    split_hand = list(hand)
    hands[hand] = (
        [card_strengths[x] for x in split_hand], # Hand card strengths
        int(bid),                                # Bid
        get_hand_strength(split_hand)            # Hand strength
    )

    if len(ranked_hands) == 0:
        ranked_hands.append(hand)
    else:
        found_rank = False
        for rank_index in range(0, len(ranked_hands)):
            if is_hand_better(hand, ranked_hands[rank_index]):
                ranked_hands[rank_index:rank_index] = [hand]
                found_rank = True
                break

        # We didn't find weaker hand, so shove the one on the end.
        if not found_rank:
            ranked_hands.append(hand)

winnings = []
for i in range(0, len(ranked_hands)):
    rank_value = len(ranked_hands) - i
    hand_index = ranked_hands[i]
    rank_winnings = rank_value * hands[hand_index][1]
    winnings.append(rank_winnings)

print(sum(winnings))