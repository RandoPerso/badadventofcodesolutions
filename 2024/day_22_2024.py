import aoctools
from copy import deepcopy
from functools import cache

tools = aoctools.aoc_tools()

tools.start_clock()
lines = tools.get_array_input("2024/inputs/day_22_2024.txt")

def next_secret(x):
    x = (x ^ (x << 6)) & 16777215
    x = (x ^ (x >> 5)) & 16777215
    return (x ^ (x << 11)) & 16777215

def chop(x):
    return int(str(x)[-1])

total = 0
market = []
for line in lines:
    changes = []
    prices = {}
    secret = int(line)
    for i in range(2000):
        previous = chop(secret)
        secret = next_secret(secret)
        change = chop(secret) - previous
        changes.append(change)
        if len(changes) == 5:
            changes.pop(0)
        if len(changes) == 4:
            if tuple(changes) not in prices:
                prices[tuple(changes)] = chop(secret)
    total += secret
    market.append(prices)

print(total)

tools.stop_clock()

maximum = 0
for a in range(-9, 10):
    for b in range(-9, 10):
        for c in range(-9, 10):
            for d in range(-9, 10):
                sub_total = 0
                for seller in market:
                    if (a, b, c, d) in seller:
                        sub_total += seller[(a, b, c, d)]
                if sub_total > maximum:
                    maximum = sub_total

print(maximum)

tools.stop_clock()