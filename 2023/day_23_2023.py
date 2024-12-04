import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()

lines = [list(i) for i in tools.get_array_input("2023/inputs/day_23_2023.txt")]

start = (1, 0)
goal = (len(lines[0]) - 2, len(lines) - 1)

def tup_add(tup1, tup2):
    return (tup1[0] + tup2[0], tup1[1] + tup2[1])

def safe_get(x, y):
    if x < 0 or y < 0 or x >= len(lines[0]) or y >= len(lines):
        return "#"
    else:
        return lines[y][x]

max_length = 0
dirs = ((1, 0), (0, -1), (-1, 0), (0, 1))

states = [(start, (start,))]

while states:
    current_state = states.pop()
    if current_state[0] == goal:
        max_length = max(max_length, len(current_state[1]) - 1)
    else:
        for ind, dir in enumerate(dirs):
            temp = tup_add(current_state[0], dir)
            if temp in current_state[1]:
                continue
            if safe_get(temp[0], temp[1]) != "#":
                if safe_get(temp[0], temp[1]) != ".":
                    if safe_get(temp[0], temp[1]) != ["<", "v", ">", "^"][ind]:
                        states.append((tup_add(temp, dirs[[">", "^", "<", "v"].index(safe_get(temp[0], temp[1]))]), current_state[1] + (temp, tup_add(temp, dirs[[">", "^", "<", "v"].index(safe_get(temp[0], temp[1]))]))))
                else:
                    states.append((temp, current_state[1] + (temp,)))

print(max_length)

tools.stop_clock()

"""max_length = 0
# dirs = ((1, 0), (0, -1), (-1, 0), (0, 1))

states = [(start, (start,))]

while states:
    current_state = states.pop()
    if current_state[0] == goal:
        max_length = max(max_length, len(current_state[1]) - 1)
    else:
        for dir in dirs:
            temp = tup_add(current_state[0], dir)
            if temp in current_state[1]:
                continue
            if safe_get(temp[0], temp[1]) != "#":
                states.append((temp, current_state[1] + (temp,)))

print(max_length)"""

nodes = [start, goal]

for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char != ".":
            continue
        if sum([safe_get(x + i[0], y + i[1]) != "#" for i in dirs]) > 2:
            nodes.append((x, y))

# print(nodes)

connections = [set() for i in nodes]

for index, node in enumerate(nodes):
    states = [(node, (node,))]
    while states:
        current_state = states.pop()
        if current_state[0] != node and current_state[0] in nodes:
            connections[index].add((nodes.index(current_state[0]), len(current_state[1]) - 1))
        else:
            for ind, dir in enumerate(dirs):
                temp = tup_add(current_state[0], dir)
                if temp in current_state[1]:
                    continue
                if safe_get(temp[0], temp[1]) != "#":
                    states.append((temp, current_state[1] + (temp,)))

# print(connections)

states = [(0, (0,), 0)]
max_length = 0

while states:
    current_state = states.pop()
    if current_state[0] == 1:
        max_length = max(max_length, current_state[2])
    else:
        for next in connections[current_state[0]]:
            if next[0] in current_state[1]:
                continue
            states.append((next[0], current_state[1] + (next[0],), current_state[2] + next[1]))

print(max_length)

tools.stop_clock()