import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()
lines = tools.get_array_input("2024/inputs/day_20_2024.txt")

LIMIT = 100

path = set()
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char == "#":
            continue
        path.add((x, y))
        if char == "S":
            start = (x, y)
        if char == "E":
            end = (x, y)

frontier = {start}
visited = {start: 0}
while frontier:
    new_frontier = set()
    for position in frontier:
        if position == end:
            continue
        for dir in tools.dirs:
            new = tools.tup_add(position, dir)
            if new not in path:
                continue
            if new in visited:
                if visited[new] <= visited[position] + 1:
                    continue
            visited[new] = visited[position] + 1
            new_frontier.add(new)
    frontier = new_frontier

frontier = {start}
total = 0
for position in visited:
    if position == end:
        continue
    sub_front = {position}
    for i in range(2):
        new_front = set()
        for sub_position in sub_front:
            for dir in tools.dirs:
                new = tools.tup_add(sub_position, dir)
                new_front.add(new)
        sub_front = sub_front.union(new_front)
    for sub_position in sub_front:
        if sub_position not in path:
            continue
        if visited[sub_position] - visited[position] - 2 >= LIMIT:
            total += 1

print(total)

tools.stop_clock()

def man_dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

total = 0
for position in visited:
    if position == end:
        continue
    total_front = {position}
    front = {position}
    for i in range(20):
        new_front = set()
        for sub_position in front:
            for dir in tools.dirs:
                new = tools.tup_add(sub_position, dir)
                if new not in total_front:
                    new_front.add(new)
                    total_front.add(new)
        front = new_front
    for sub_position in total_front:
        if sub_position not in path:
            continue
        if visited[sub_position] - visited[position] - man_dist(sub_position, position) >= LIMIT:
            total += 1

print(total)

tools.stop_clock()