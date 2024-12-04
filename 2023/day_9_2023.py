import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()

lines = tools.get_array_input("2023/inputs/day_9_2023.txt")
total = 0

for line in lines:
    sequence = [int(i) for i in line.split()]
    meta_sequence = [sequence.copy()]
    while meta_sequence[-1].count(0) != len(meta_sequence[-1]):
        meta_sequence.append([meta_sequence[-1][i + 1] - meta_sequence[-1][i] for i in range(len(meta_sequence[-1]) - 1)])
    meta_sequence.reverse()
    for i in range(len(meta_sequence) - 1):
        meta_sequence[i + 1].append(meta_sequence[i][-1] + meta_sequence[i + 1][-1])
    total += meta_sequence[-1][-1]

print(total)
tools.stop_clock()

total = 0

for line in lines:
    sequence = [int(i) for i in line.split()]
    meta_sequence = [sequence.copy()]
    while meta_sequence[-1].count(0) != len(meta_sequence[-1]):
        meta_sequence.append([meta_sequence[-1][i + 1] - meta_sequence[-1][i] for i in range(len(meta_sequence[-1]) - 1)])
    meta_sequence.reverse()
    for i in range(len(meta_sequence) - 1):
        meta_sequence[i + 1].insert(0, (meta_sequence[i + 1][0] - meta_sequence[i][0]))
    total += meta_sequence[-1][0]

print(total)
tools.stop_clock()
