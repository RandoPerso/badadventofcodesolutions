import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()
lines = tools.get_array_input("2024/inputs/day_19_2024.txt")

total = 0
for index, line in enumerate(lines):
    if index == 0:
        possible = set(line.split(", "))
        continue
    if index == 1:
        continue
    frontier = {0}
    for i in range(len(line) + 1):
        for x in frontier.copy():
            if line[x:i] in possible:
                frontier.add(i)
    if len(line) in frontier:
        total += 1

print(total)

tools.stop_clock()

total = 0
for index, line in enumerate(lines):
    if index <= 1:
        continue
    frontier = {0: 1}
    for i in range(len(line) + 1):
        for x in frontier.copy():
            if line[x:i] in possible:
                if i in frontier:
                    frontier[i] += frontier[x]
                else:
                    frontier[i] = frontier[x]
    if len(line) in frontier:
        total += frontier[len(line)]

print(total)

tools.stop_clock()