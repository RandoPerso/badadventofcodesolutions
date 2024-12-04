import aoctools
import numpy as np
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()

lines = [list(i) for i in tools.get_array_input("2023/inputs/day_14_2023.txt")]
rotated = np.rot90(np.array(lines), 3).tolist()

def sift_row(line):
    good = False
    while not good:
        temp = line.copy()
        for i in range(len(lines) - 1, -1, -1):
            if i + 1 >= len(lines):
                continue
            elif line[i] == "O" and line[i + 1] == ".":
                line[i] = "."
                line[i + 1] = "O"
        if temp == line:
            good = True
    return line

for i in range(len(rotated)):
    rotated[i] = sift_row(rotated[i])

rotated = np.rot90(np.array(rotated), 3).tolist()

total = 0

for i in range(len(rotated)):
    for char in rotated[i]:
        if char == "O":
            total += i + 1

print(total)

tools.stop_clock()

def process_north(lines):
    rotated = np.rot90(np.array(lines), 3).tolist()
    for i in range(len(rotated)):
        rotated[i] = sift_row(rotated[i])
    return rotated

def process_4(lines):
    temp = process_north(lines)
    temp = process_north(temp)
    temp = process_north(temp)
    return process_north(temp)

good = False

all_lines = []

while not good:
    all_lines.append(deepcopy(lines))
    lines = process_4(lines)
    if lines in all_lines:
        index = all_lines.index(lines)
        good = True

loop_len = len(all_lines) - index

remaining = (1000000000 - index) % loop_len

for i in range(remaining):
    lines = process_4(lines)

rotated = np.rot90(np.array(lines), 2).tolist()

total = 0

for i in range(len(rotated)):
    for char in rotated[i]:
        if char == "O":
            total += i + 1

print(total)

tools.stop_clock()
