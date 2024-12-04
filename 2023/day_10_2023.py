import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()

lines = [list(i) for i in tools.get_array_input("2023/inputs/day_10_2023.txt")]

def safe_get(x, y):
    if x < 0 or x >= len(lines[0]) or y < 0 or y >= len(lines):
        return "."
    else:
        return lines[y][x]

"""def filter_out():
    for y, line in enumerate(lines):
        for x, pipe in enumerate(line):
            if pipe == "|":
                if (safe_get(x, y - 1) not in "F|7S" or safe_get(x, y + 1) not in "J|LS"):
                    lines[y][x] = "."
            elif pipe == "-":
                if (safe_get(x - 1, y) not in "L-FS" or safe_get(x + 1, y) not in "J-7S"):
                    lines[y][x] = "."
            elif pipe == "F":
                if (safe_get(x, y + 1) not in "J|LS" or safe_get(x + 1, y) not in "J-7S"):
                    lines[y][x] = "."
            elif pipe == "L":
                if (safe_get(x, y - 1) not in "F|7S" or safe_get(x + 1, y) not in "J-7S"):
                    lines[y][x] = "."
            elif pipe == "7":
                if (safe_get(x, y + 1) not in "J|LS" or safe_get(x - 1, y) not in "L-FS"):
                    lines[y][x] = "."
            elif pipe == "J":
                if (safe_get(x, y - 1) not in "F|7S" or safe_get(x - 1, y) not in "L-FS"):
                    lines[y][x] = "."

old_lines = []
while old_lines != lines:
    old_lines = deepcopy(lines)
    filter_out()"""

"""for line in lines:
    temp = ""
    for char in line:
        temp += char
    print(temp)"""

for y, line in enumerate(lines):
    for x, pipe in enumerate(line):
        if pipe == "S":
            location = [x, y]

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

locations = [(location[0], location[1] - 1, UP), (location[0], location[1] + 1, DOWN)]

total = 1
finished = False

pairs = {
    "-": (LEFT, RIGHT),
    "|": (UP, DOWN),
    "J": (UP, LEFT),
    "F": (DOWN, RIGHT),
    "L": (UP, RIGHT),
    "7": (DOWN, LEFT)
}

all = [(location[0], location[1] - 1), location, (location[0], location[1] + 1)]

while not finished:
    total += 1
    old_locations = deepcopy(locations)
    locations = []
    for place in old_locations:
        pipe = safe_get(place[0], place[1])
        directions = pairs[pipe]
        ind = directions.index((place[2] + 2) % 4)
        match directions[(ind + 1) % 2]:
            case 0:
                new = (place[0], place[1] - 1, UP)
            case 1:
                new = (place[0] + 1, place[1], RIGHT)
            case 2:
                new = (place[0], place[1] + 1, DOWN)
            case 3:
                new = (place[0] - 1, place[1], LEFT)
        if (
            (new[0], new[1], UP) in locations
            or (new[0], new[1], RIGHT) in locations
            or (new[0], new[1], DOWN) in locations
            or (new[0], new[1], LEFT) in locations):
                print(total)
                finished = True
                break
        locations.append(new)
        all.append((new[0], new[1]))

tools.stop_clock()

for y, line in enumerate(lines):
    for x, pipe in enumerate(line):
        if (x, y) not in all:
            lines[y][x] = "."

lines[location[1]][location[0]] = "|"

"""for line in lines:
    temp = ""
    for char in line:
        temp += char
    print(temp)"""

all = []
frontier = [(0, 0)]

def is_valid(x, y):
    if x < 0 or y < 0 or x >= len(lines[0]) - 1 or y >= len(lines) - 1:
        return False
    return True

def arr_add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def remover(x, y):
    if lines[y][x] == ".":
        lines[y][x] = " "
    if lines[y + 1][x] == ".":
        lines[y + 1][x] = " "
    if lines[y][x + 1] == ".":
        lines[y][x + 1] = " "
    if lines[y + 1][x + 1] == ".":
        lines[y + 1][x + 1] = " "

while len(frontier) != 0:
    all.extend(deepcopy(frontier))
    old_front = deepcopy(frontier)
    frontier = []
    for coord in old_front:
        remover(coord[0], coord[1])
        for ind, displace in enumerate(((0, -1), (1, 0), (0, 1), (-1, 0))):
            new_coord = arr_add(coord, displace)
            if not is_valid(new_coord[0], new_coord[1]) or new_coord in all or new_coord in frontier or new_coord in old_front:
                continue
            match ind:
                case 0:
                    if safe_get(coord[0], coord[1]) in "FL-":
                        continue
                case 1:
                    if safe_get(coord[0] + 1, coord[1]) in "7|F":
                        continue
                case 2:
                    if safe_get(coord[0], coord[1] + 1) in "FL-":
                        continue
                case 3:
                    if safe_get(coord[0], coord[1]) in "7|F":
                        continue
            frontier.append(new_coord)

total = 0

for line in lines:
    total += line.count(".")

"""for line in lines:
    temp = ""
    for char in line:
        temp += char
    print(temp)"""

print(total)

tools.stop_clock()
