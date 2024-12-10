import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()
lines = tools.get_array_input("2024/inputs/day_10_2024.txt")

dirs = ((0, -1), (1, 0), (0, 1), (-1, 0))

max_x = len(lines[0])
max_y = len(lines)

grid = [[int(i) for i in row] for row in lines]

total = 0
for y, row in enumerate(grid):
    for x, char in enumerate(row):
        if char != 0:
            continue
        frontier = {(x, y)}
        for i in range(1, 10):
            new_frontier = set()
            for location in frontier:
                for dir in dirs:
                    new_location = (location[0] + dir[0], location[1] + dir[1])
                    if tools.in_bounds(new_location, max_x, max_y) and grid[new_location[1]][new_location[0]] == i:
                        new_frontier.add(new_location)
            frontier = new_frontier
        total += len(frontier)

print(total)

tools.stop_clock()

total = 0
for y, row in enumerate(grid):
    for x, char in enumerate(row):
        if char != 0:
            continue
        frontier = {(x, y): 1}
        for i in range(1, 10):
            new_frontier = {}
            for location in frontier:
                for dir in dirs:
                    new_location = (location[0] + dir[0], location[1] + dir[1])
                    if tools.in_bounds(new_location, max_x, max_y) and grid[new_location[1]][new_location[0]] == i:
                        if new_location in new_frontier:
                            new_frontier[new_location] += frontier[location]
                        else:
                            new_frontier[new_location] = frontier[location]
            frontier = new_frontier
        total += sum([frontier[i] for i in frontier])

print(total)

tools.stop_clock()