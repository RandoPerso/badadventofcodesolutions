import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()

lines = tools.get_array_input("2023/inputs/day_3_2023.txt")
total = 0

def get_char(x, y):
    if (x < 0) or (y < 0) or (x >= len(lines[0])) or (y >= len(lines)):
        return "."
    else:
        return lines[y][x]

def get_surrounds(x, y):
    surrounds = []
    surrounds.append(get_char(x + 1, y))
    surrounds.append(get_char(x - 1, y))
    surrounds.append(get_char(x + 1, y + 1))
    surrounds.append(get_char(x - 1, y + 1))
    surrounds.append(get_char(x + 1, y - 1))
    surrounds.append(get_char(x - 1, y - 1))
    surrounds.append(get_char(x, y + 1))
    surrounds.append(get_char(x, y - 1))
    return surrounds

def is_symbol(char):
    if char.isnumeric():
        return False
    if char == ".":
        return False
    return True

for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char.isnumeric():
            if not get_char(x - 1, y).isnumeric():
                next_to = False
                if True in [is_symbol(i) for i in get_surrounds(x, y)]:
                    next_to = True
                running_total = char
                current_x = x + 1
                while get_char(current_x, y).isnumeric():
                    running_total += get_char(current_x, y)
                    if True in [is_symbol(i) for i in get_surrounds(current_x, y)]:
                        next_to = True
                    current_x += 1
                if next_to:
                    total += int(running_total)

print(total)

tools.stop_clock()

total = 0

gears = {}

def is_gear(char):
    if char == "*":
        return True
    return False

def get_gears(x, y):
    gears = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if is_gear(get_char(x + dx, y + dy)):
                gears.append((x + dx, y + dy))
    return gears

for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char.isnumeric():
            if not get_char(x - 1, y).isnumeric():
                known_gears = get_gears(x, y)
                running_total = char
                current_x = x + 1
                while get_char(current_x, y).isnumeric():
                    running_total += get_char(current_x, y)
                    if get_gears(current_x, y):
                        for gear in get_gears(current_x, y):
                            if gear not in known_gears:
                                known_gears.append(gear)
                    current_x += 1
                for gear in known_gears:
                    if gear in list(gears.keys()):
                        gears[gear].append(int(running_total))
                    else:
                        gears.update({gear: [int(running_total)]})

for gear in gears:
    if len(gears[gear]) == 2:
        total += gears[gear][0] * gears[gear][1]

print(total)

tools.stop_clock()
