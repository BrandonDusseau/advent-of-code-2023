import os
from pprint import pprint

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

hands = {}
ranked_hands = []

card_strengths = {
    "J": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
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
    counts = get_card_counts(hand)
    if 5 in counts.values() and len(counts.values()) == 1:
        return True

    # Any jokers + only one other card type = five of a kind
    joker_count = counts.get("J")
    if joker_count is not None and joker_count > 0 and len(counts) == 2:
        return True

    return False

def is_four_kind(hand):
    counts = get_card_counts(hand)
    if 4 in counts.values() and len(counts.values()) == 2:
        return True

    joker_count = counts.get("J")
    pairs = [x for x in counts.values() if x == 2]

    # 3 Jokers + two other types of cards = four of a kind
    if joker_count == 3 and len(counts) == 3:
        return True

    # 2 Jokers + one more pair = four of a kind
    if joker_count == 2 and len(pairs) == 2:
        return True

    # 1 Joker + three of another card = four of a kind
    if joker_count == 1 and 3 in counts.values() and len(counts) == 3:
        return True

    # 4 Jokers covered by main case
    # 5 covers = stronger hand than four of a kind

    return False

def is_full_house(hand):
    counts = get_card_counts(hand)
    if 3 in counts.values() and 2 in counts.values() and len(counts) == 2:
        return True

    joker_count = counts.get("J")
    pairs = [x for x in counts.values() if x == 2]

    # 1 joker + 2 pairs = full house
    if joker_count == 1 and len(pairs) == 2:
        return True

    # 3 of a kind + 1 joker + 1 other card type = full house
    if 3 in counts.values() and joker_count == 1 and len(counts) == 3:
        return True

    # 2 jokers + 1 more pair + 1 other card = full house
    if joker_count == 2 and len(pairs) == 2 and len(counts) == 3:
        return True

    # 3 jokers + 1 pair is covered by main case
    # 4+ jokers = stronger hand than full house

    return False

def is_three_kind(hand):
    counts = get_card_counts(hand)
    if 3 in counts.values() and len(counts) == 3:
        return True

    joker_count = counts.get("J")
    pairs = [x for x in counts.values() if x == 2]

    # 2 jokers + 3 other cards = three of a kind
    if joker_count == 2 and len(counts) == 4:
        return True

    # 1 joker + 1 pair + 2 other cards = three of a kind
    if joker_count == 1 and len(pairs) == 1 and len(counts) == 4:
        return True

    # 3 jokers covered by main case
    # 4+ jokers = stronger hand than three of a kind
    # 3 jokers + 1 pair = stronger hand
    # 3 of a kind + 1 joker + 1 other card type = stronger hand

    return False

def is_two_pair(hand):
    counts = get_card_counts(hand)
    pairs = [x for x in counts.values() if x == 2]
    if len(pairs) == 2 and len(counts) == 3:
        return True

    joker_count = counts.get("J")

    # 1 joker + 1 pair + 2 other cards = 2 pairs
    if joker_count == 1 and len(pairs) == 1 and len(counts) == 4:
        return True

    return False

def is_one_pair(hand):
    counts = get_card_counts(hand)
    if 2 in counts.values() and len(counts) == 4:
        return True

    joker_count = counts.get("J")

    # 1 joker + 4 other cards = one pair
    if joker_count == 1 and len(counts) == 5:
        return True

    return False

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