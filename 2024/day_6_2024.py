import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()
lines = tools.get_array_input("2024/inputs/day_6_2024.txt")

position = [0, 0]
direction = 0
grid = []
total = 0

for y, line in enumerate(lines):
    temp = list(line)
    if "^" in temp:
        position = [temp.index("^"), y]
    grid.append(temp)

max_x = len(grid[0])
max_y = len(grid)

starting = tuple(position.copy()) + (0,)

def in_bounds(pos):
    if -1 in pos:
        return False
    if pos[1] == max_y:
        return False
    if pos[0] == max_x:
        return False
    return True

while in_bounds(position):
    if grid[position[1]][position[0]] != "X":
        grid[position[1]][position[0]] = "X"
        total += 1
    match direction:
        case 0:
            position[1] -= 1
            if in_bounds(position):
                if grid[position[1]][position[0]] == "#":
                    position[1] += 1
                    direction = 1
        case 1:
            position[0] += 1
            if in_bounds(position):
                if grid[position[1]][position[0]] == "#":
                    position[0] -= 1
                    direction = 2
        case 2:
            position[1] += 1
            if in_bounds(position):
                if grid[position[1]][position[0]] == "#":
                    position[1] -= 1
                    direction = 3
        case 3:
            position[0] -= 1
            if in_bounds(position):
                if grid[position[1]][position[0]] == "#":
                    position[0] += 1
                    direction = 0

print(total)

tools.stop_clock()

# Slow! Part 2 took like 7 seconds to run.
def will_loop():
    position = starting
    visited = set()
    while in_bounds(position):
        if position in visited:
            return True
        visited.add(position)
        position = list(position)
        match position[2]:
            case 0:
                position[1] -= 1
                if in_bounds(position):
                    if grid[position[1]][position[0]] == "#":
                        position[1] += 1
                        position[2] = 1
            case 1:
                position[0] += 1
                if in_bounds(position):
                    if grid[position[1]][position[0]] == "#":
                        position[0] -= 1
                        position[2] = 2
            case 2:
                position[1] += 1
                if in_bounds(position):
                    if grid[position[1]][position[0]] == "#":
                        position[1] -= 1
                        position[2] = 3
            case 3:
                position[0] -= 1
                if in_bounds(position):
                    if grid[position[1]][position[0]] == "#":
                        position[0] += 1
                        position[2] = 0
        position = tuple(position)
    return False

total = 0

for y, line in enumerate(grid):
    for x, char in enumerate(line):
        if (x, y, 0) != starting and char == "X":
            grid[y][x] = "#"
            if will_loop():
                total += 1
            grid[y][x] = "X"

print(total)

tools.stop_clock()