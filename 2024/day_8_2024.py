import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()
lines = tools.get_array_input("2024/inputs/day_8_2024.txt")

antennas = {}
all_anti_nodes = set()

for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char != ".":
            if char not in antennas:
                antennas[char] = [(x, y)]
            else:
                antennas[char].append((x, y))

max_y = len(lines)
max_x = len(lines[0])

def in_bounds(pos):
    if pos[1] >= max_y or pos[1] < 0:
        return False
    if pos[0] >= max_x or pos[0] < 0:
        return False
    return True

for type in antennas:
    for index, a in enumerate(antennas[type]):
        for b in antennas[type][index + 1:]:
            anti_1 = (a[0] - (b[0] - a[0]), a[1] - (b[1] - a[1]))
            if in_bounds(anti_1):
                all_anti_nodes.add(anti_1)
            anti_2 = (b[0] - (a[0] - b[0]), b[1] - (a[1] - b[1]))
            if in_bounds(anti_2):
                all_anti_nodes.add(anti_2)

print(len(all_anti_nodes))

tools.stop_clock()

for type in antennas:
    for index, a in enumerate(antennas[type]):
        for b in antennas[type][index + 1:]:
            x_diff = b[0] - a[0]
            y_diff = b[1] - a[1]
            anti_1 = (a[0] + x_diff, a[1] + y_diff)
            while in_bounds(anti_1):
                all_anti_nodes.add(anti_1)
                anti_1 = (anti_1[0] + x_diff, anti_1[1] + y_diff)
            anti_2 = (b[0] - x_diff, b[1] - y_diff)
            while in_bounds(anti_2):
                all_anti_nodes.add(anti_2)
                anti_2 = (anti_2[0] - x_diff, anti_2[1] - y_diff)

print(len(all_anti_nodes))

tools.stop_clock()