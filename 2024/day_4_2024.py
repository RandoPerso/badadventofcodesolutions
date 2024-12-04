import aoctools
from copy import deepcopy
import re

tools = aoctools.aoc_tools()

tools.start_clock()
lines = tools.get_array_input("2024/inputs/day_4_2024.txt")

total = 0
for line in lines:
    total += len(re.findall("XMAS", line))
    total += len(re.findall("SAMX", line))

rotated = tools.rot_array_cc([list(i) for i in lines])
temp = ["".join(i) for i in rotated]
for col in temp:
    total += len(re.findall("XMAS", col))
    total += len(re.findall("SAMX", col))

for y in range(len(lines) - 3):
    for x in range(len(lines[0]) - 3):
        if lines[y][x] == "X" and lines[y + 1][x + 1] == "M" and lines[y + 2][x + 2] == "A" and lines[y + 3][x + 3] == "S":
            total += 1
        elif lines[y][x] == "S" and lines[y + 1][x + 1] == "A" and lines[y + 2][x + 2] == "M" and lines[y + 3][x + 3] == "X":
            total += 1

for y in range(len(rotated) - 3):
    for x in range(len(rotated[0]) - 3):
        if rotated[y][x] == "X" and rotated[y + 1][x + 1] == "M" and rotated[y + 2][x + 2] == "A" and rotated[y + 3][x + 3] == "S":
            total += 1
        elif rotated[y][x] == "S" and rotated[y + 1][x + 1] == "A" and rotated[y + 2][x + 2] == "M" and rotated[y + 3][x + 3] == "X":
            total += 1

print(total)

tools.stop_clock()

correct = ("MMSS", "SMMS", "SSMM", "MSSM")

total = 0
for y in range(1, len(lines) - 1):
    for x in range(1, len(lines[0]) - 1):
        if lines[y][x] == "A":
            if lines[y-1][x-1] + lines[y-1][x+1] + lines[y+1][x+1] + lines[y+1][x-1] in correct:
                total += 1

print(total)

tools.stop_clock()