import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()

lines = tools.get_array_input("2023/inputs/day_7_2023.txt")

def value_hand(hand):
    non_dupe = list(set(hand))
    if len(non_dupe) == 5:
        value = 0
    elif len(non_dupe) == 4:
        value = 13**5
    elif len(non_dupe) == 3:
        if max([hand.count(i) for i in non_dupe]) == 2:
            value = 2 * 13**5
        else:
            value = 3 * 13**5
    elif len(non_dupe) == 2:
        if max([hand.count(i) for i in non_dupe]) == 3:
            value = 4 * 13**5
        else:
            value = 5 * 13**5
    elif len(non_dupe) == 1:
        value = 6 * 13**5
    for index, card in enumerate(hand):
        card_score = 13 - "AKQJT98765432".index(card)
        value += card_score * 13**(4-index)
    return value

hands = [i.split() for i in lines]

hands.sort(key=lambda a: value_hand(a[0]))

hands = [int(i[1]) * (j + 1) for j, i in enumerate(hands)]

print(sum(hands))

tools.stop_clock()

def value_hand2(hand):
    non_dupe = list(set(hand))
    non_dupe2 = list(set(hand))
    your_joking = False
    if "J" in non_dupe:
        non_dupe.remove("J")
        your_joking = True
    if len(non_dupe) == 5:
        # High Card (no joker possible)
        value = 0
    elif len(non_dupe) == 4:
        # One pair
        # High Card with joker
        value = 13**5
    elif len(non_dupe) == 3:
        if not your_joking and max([hand.count(i) for i in non_dupe]) == 2:
            # Two Pair
            value = 2 * 13**5
        else:
            # Three of a kind
            # One Pair with joker
            # High Card with two jokers
            value = 3 * 13**5
    elif len(non_dupe) == 2:
        if not your_joking and max([hand.count(i) for i in non_dupe]) == 3:
            # Full House
            value = 4 * 13**5
        else:
            if max([hand.count(i) for i in non_dupe2]) == 2 and hand.count("J") == 1:
                # Two Pair and Joker
                value = 4 * 13**5
            else:
                # Four of a Kind
                # Three of a Kind and Joker
                # One pair and two jokers
                # High card and three jokers
                value = 5 * 13**5
    elif len(non_dupe) <= 1:
        value = 6 * 13**5
    for index, card in enumerate(hand):
        card_score = 13 - "AKQT98765432J".index(card)
        value += card_score * 13**(4-index)
    return value

hands = [i.split() for i in lines]

hands.sort(key=lambda a: value_hand2(a[0]))

hands = [int(i[1]) * (j + 1) for j, i in enumerate(hands)]

print(sum(hands))

tools.stop_clock()