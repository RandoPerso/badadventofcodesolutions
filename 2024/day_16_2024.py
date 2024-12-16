import aoctools
from copy import deepcopy
from fractions import Fraction

tools = aoctools.aoc_tools()

tools.start_clock()
lines = tools.get_array_input("2024/inputs/day_16_2024.txt")

dirs = ((1, 0, 0), (0, 1, 0), (-1, 0, 0), (0, -1, 0))

path = set()
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char in ".SE":
            path.add((x, y))
        if char == "S":
            start = (x, y, 0)
        if char == "E":
            end = (x, y)

visited = {start: 0}
frontier = {(start, 0)}

def tup_add(x, y) -> tuple:
    return (x[0] + y[0], x[1] + y[1], (x[2] + y[2]) % 4)

def safe_get(x):
    if x in visited:
        return visited[x]
    return 9999999999999

minimal = 9999999999999
while frontier:
    new_frontier = set()
    for position in frontier:
        if (position[0][0], position[0][1]) == end:
            if position[1] < minimal:
                minimal = position[1]
            continue
        new = tup_add(position[0], dirs[position[0][2]])
        if (new[0], new[1]) in path and position[1] + 1 < safe_get(new):
            visited[new] = position[1] + 1
            new_frontier.add((new, position[1] + 1))
        new = tup_add(position[0], (0, 0, 1))
        if (new[0], new[1]) in path and position[1] + 1000 < safe_get(new):
            visited[new] = position[1] + 1000
            new_frontier.add((new, position[1] + 1000))
        new = tup_add(position[0], (0, 0, -1))
        if (new[0], new[1]) in path and position[1] + 1000 < safe_get(new):
            visited[new] = position[1] + 1000
            new_frontier.add((new, position[1] + 1000))
    frontier = new_frontier

print(minimal)

tools.stop_clock()

# back tracking time!

frontier = set()
for dir in range(4):
    if (end[0], end[1], dir) in visited and visited[(end[0], end[1], dir)] == minimal:
        frontier.add(((end[0], end[1], dir), minimal))

def chop(x):
    return (x[0], x[1])

correct = {chop(start), end}
while frontier:
    new_frontier = set()
    for position in frontier:
        if position[0] == start:
            continue
        new = tup_add(position[0], dirs[(position[0][2] + 2) % 4])
        if new in visited and visited[new] == position[1] - 1:
            correct.add(chop(new))
            new_frontier.add((new, position[1] - 1))
        new = tup_add(position[0], (0, 0, 1))
        if new in visited and visited[new] == position[1] - 1000:
            correct.add(chop(new))
            new_frontier.add((new, position[1] - 1000))
        new = tup_add(position[0], (0, 0, -1))
        if new in visited and visited[new] == position[1] - 1000:
            correct.add(chop(new))
            new_frontier.add((new, position[1] - 1000))
    frontier = new_frontier

print(len(correct))

tools.stop_clock()