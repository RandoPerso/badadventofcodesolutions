import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()
lines = tools.get_array_input("2024/inputs/day_12_2024.txt")

visited = set()

dirs = ((0, -1), (1, 0), (0, 1), (-1, 0))
max_y = len(lines)
max_x = len(lines[0])

total = 0

for y, row in enumerate(lines):
    for x, char in enumerate(row):
        if (x, y) in visited:
            continue
        frontier = {(x, y)}
        region = {(x, y)}
        visited.add((x, y))
        perimeter = 0
        while len(frontier) > 0:
            new_frontier = set()
            for location in frontier:
                for dir in dirs:
                    new_location = (location[0] + dir[0], location[1] + dir[1])
                    if new_location not in visited and tools.in_bounds(new_location, max_x, max_y) and lines[new_location[1]][new_location[0]] == char:
                        new_frontier.add(new_location)
                        region.add(new_location)
                        visited.add(new_location)
                    elif new_location not in region:
                        perimeter += 1
            frontier = new_frontier
        total += len(region) * perimeter

print(total)

tools.stop_clock()

visited = set()

total = 0
for y, row in enumerate(lines):
    for x, char in enumerate(row):
        if (x, y) in visited:
            continue
        frontier = {(x, y)}
        region = {(x, y)}
        visited.add((x, y))
        while len(frontier) > 0:
            new_frontier = set()
            for location in frontier:
                for dir in dirs:
                    new_location = (location[0] + dir[0], location[1] + dir[1])
                    if new_location not in visited and tools.in_bounds(new_location, max_x, max_y) and lines[new_location[1]][new_location[0]] == char:
                        new_frontier.add(new_location)
                        region.add(new_location)
                        visited.add(new_location)
            frontier = new_frontier
        edges = 0
        # to anyone who is reading this: here is what the algorithm does:
        # you loop through each row and in each row, go left to right.
        # keep track of whether or not the previous cell had a top or bottom edge with the region
        # (cells that are in the region are disqualified and are considered to have no edges)
        # whenever you get to a cell with an edge the previous cell did not have, increment counter
        # do again but vertical
        # i am very aware that this is a bad way of doing it and i can make a solution that only loops through all cells once.
        # too bad, this is what you get.
        # have fun!
        #
        # also sorry about the variable names
        for y_1 in range(-1, max_y + 1):
            top_edging = False
            bottom_edging = False
            for x_1 in range(-1, max_x + 1):
                if (x_1, y_1) in region:
                    top_edging = False
                    bottom_edging = False
                    continue
                if (x_1, y_1 + 1) in region:
                    if not bottom_edging:
                        edges += 1
                        bottom_edging = True
                else:
                    bottom_edging = False
                if (x_1, y_1 - 1) in region:
                    if not top_edging:
                        edges += 1
                        top_edging = True
                else:
                    top_edging = False
        for x_1 in range(-1, max_x + 1):
            left_edging = False
            right_edging = False
            for y_1 in range(-1, max_y + 1):
                if (x_1, y_1) in region:
                    left_edging = False
                    right_edging = False
                    continue
                if (x_1 - 1, y_1) in region:
                    if not left_edging:
                        edges += 1
                        left_edging = True
                else:
                    left_edging = False
                if (x_1 + 1, y_1) in region:
                    if not right_edging:
                        edges += 1
                        right_edging = True
                else:
                    right_edging = False
        total += len(region) * edges
                
print(total)

tools.stop_clock()