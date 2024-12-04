import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()

lines = [list(i) for i in tools.get_array_input("2023/inputs/day_11_2023.txt")]
lines2 = deepcopy(lines)

expand_y = []
expand_x = []

for y, line in enumerate(lines):
    if line.count("#") == 0:
        expand_y.insert(0, y)

for x in range(len(lines[0])):
    for line in lines:
        if line[x] == "#":
            break
    else:
        expand_x.insert(0, x)

for y in expand_y:
    lines.insert(y, ["." for i in range(len(lines[0]))])

for x in expand_x:
    for y in range(len(lines)):
        lines[y].insert(x, ".")

positions = []

"""print(expand_x)
print(expand_y)"""

def man_dist(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char == "#":
            positions.append((x, y))

total = 0
for i in range(len(positions)):
    pos = positions[i]
    for j in positions[i + 1:]:
        total += man_dist(pos, j)

"""for line in lines:
    temp = ""
    for char in line:
        temp += char
    print(temp)"""

print(total)

tools.stop_clock()

AMOUNT = 1_000_000 - 1

def man_2(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) + AMOUNT * len(set(expand_x) & set(range(min(pos1[0], pos2[0]), max(pos1[0], pos2[0])))) + AMOUNT * len(set(expand_y) & set(range(min(pos1[1], pos2[1]), max(pos1[1], pos2[1]))))

positions = []

for y, line in enumerate(lines2):
    for x, char in enumerate(line):
        if char == "#":
            positions.append((x, y))

total = 0
for i in range(len(positions)):
    pos = positions[i]
    for j in positions[i + 1:]:
        total += man_2(pos, j)

print(total)

tools.stop_clock()
