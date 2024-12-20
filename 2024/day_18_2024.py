import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()
lines = tools.get_array_input("2024/inputs/day_18_2024.txt")

blocked = set()
for index in range(1024):
    blocked.add(tuple(int(i) for i in lines[index].split(",")))

MAX_X = 71
MAX_Y = 71

frontier = {(0, 0)}
visited = set()
counter = 0
end = (MAX_X - 1, MAX_Y - 1)
solved = False
while not solved:
    counter += 1
    new_front = set()
    for position in frontier:
        for dir in tools.dirs:
            if tools.tup_add(position, dir) in visited:
                continue
            if tools.in_bounds(tools.tup_add(position, dir), MAX_X, MAX_Y) and tools.tup_add(position, dir) not in blocked:
                if tools.tup_add(position, dir) == end:
                    solved = True
                    print(counter)
                    break
                new_front.add(tools.tup_add(position, dir))
        if solved:
            break
    if solved:
        break
    visited = visited | frontier
    frontier = new_front

tools.stop_clock()

def has_path():
    frontier = {(0, 0)}
    visited = set()
    while frontier:
        new_front = set()
        for position in frontier:
            for dir in tools.dirs:
                if tools.tup_add(position, dir) in visited:
                    continue
                if tools.in_bounds(tools.tup_add(position, dir), MAX_X, MAX_Y) and tools.tup_add(position, dir) not in blocked:
                    if tools.tup_add(position, dir) == end:
                        return True
                    new_front.add(tools.tup_add(position, dir))
        visited = frontier
        frontier = new_front
    return False

blocked = set()
for line in lines:
    blocked.add(tuple(int(i) for i in line.split(",")))
    if not has_path():
        print(line)
        break

tools.stop_clock()