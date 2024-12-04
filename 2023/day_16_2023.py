import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()

lines = [list(i) for i in tools.get_array_input("2023/inputs/day_16_2023.txt")]

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

positions = [(-1, 0, RIGHT)]
checked = []
heated = [(0, 0)]

def safe_get(x, y):
    if x < 0 or y < 0 or x >= len(lines[0]) or y >= len(lines):
        return None
    else:
        return lines[y][x]

def get_position(x, y, dir):
    if dir == UP:
        return (x, y - 1, dir)
    elif dir == RIGHT:
        return (x + 1, y, dir)
    elif dir == DOWN:
        return (x, y + 1, dir)
    elif dir == LEFT:
        return (x - 1, y, dir)
    raise Exception("improper position finding!")

def reflect(mirror, dir):
    if mirror == "/":
        if dir == RIGHT:
            return UP
        elif dir == DOWN:
            return LEFT
        elif dir == LEFT:
            return DOWN
        elif dir == UP:
            return RIGHT
        raise Exception("bad direction")
    elif mirror == "\\":
        if dir == RIGHT:
            return DOWN
        elif dir == UP:
            return LEFT
        elif dir == LEFT:
            return UP
        elif dir == DOWN:
            return RIGHT
        raise Exception("bad direction")
    raise Exception("bad mirror")

def split(splitter, dir):
    if splitter == "-":
        if dir in [RIGHT, LEFT]:
            return [dir]
        elif dir in [UP, DOWN]:
            return [LEFT, RIGHT]
        raise Exception("bad direction")
    elif splitter == "|":
        if dir in [UP, DOWN]:
            return [dir]
        elif dir in [LEFT, RIGHT]:
            return [UP, DOWN]
        raise Exception("bad direction")
    raise Exception("bad splitter")

while len(positions) > 0:
    old_pos = positions.copy()
    positions = []
    for position in old_pos:
        temp_new = get_position(position[0], position[1], position[2])
        char = safe_get(temp_new[0], temp_new[1])
        if char == None:
            continue
        if char == ".":
            next = [temp_new]
        elif char in "\\/":
            next = [(temp_new[0], temp_new[1], reflect(char, temp_new[2]))]
        elif char in "|-":
            next = [(temp_new[0], temp_new[1], i) for i in split(char, temp_new[2])]
        else:
            raise Exception("unknown char")
        for i in next:
            if i not in checked:
                checked.append(i)
                positions.append(i)
    for position in positions:
        if (position[0], position[1]) not in heated:
            heated.append((position[0], position[1]))

"""for y in range(len(lines)):
    temp = ""
    for x in range(len(lines[y])):
        if (x, y) in heated:
            temp += "#"
        else:
            temp += lines[y][x]
    print(temp)"""

print(len(heated))

tools.stop_clock()
total = 0

for k in range(len(lines)):
    positions = [(-1, k, RIGHT)]
    checked = []
    heated = []
    while len(positions) > 0:
        old_pos = positions.copy()
        positions = []
        for position in old_pos:
            temp_new = get_position(position[0], position[1], position[2])
            char = safe_get(temp_new[0], temp_new[1])
            if char == None:
                continue
            if char == ".":
                next = [temp_new]
            elif char in "\\/":
                next = [(temp_new[0], temp_new[1], reflect(char, temp_new[2]))]
            elif char in "|-":
                next = [(temp_new[0], temp_new[1], i) for i in split(char, temp_new[2])]
            else:
                raise Exception("unknown char")
            for i in next:
                if i not in checked:
                    checked.append(i)
                    positions.append(i)
        for position in positions:
            if (position[0], position[1]) not in heated:
                heated.append((position[0], position[1]))
    total = max(total, len(heated))
    positions = [(len(lines[0]), k, LEFT)]
    checked = []
    heated = []
    while len(positions) > 0:
        old_pos = positions.copy()
        positions = []
        for position in old_pos:
            temp_new = get_position(position[0], position[1], position[2])
            char = safe_get(temp_new[0], temp_new[1])
            if char == None:
                continue
            if char == ".":
                next = [temp_new]
            elif char in "\\/":
                next = [(temp_new[0], temp_new[1], reflect(char, temp_new[2]))]
            elif char in "|-":
                next = [(temp_new[0], temp_new[1], i) for i in split(char, temp_new[2])]
            else:
                raise Exception("unknown char")
            for i in next:
                if i not in checked:
                    checked.append(i)
                    positions.append(i)
        for position in positions:
            if (position[0], position[1]) not in heated:
                heated.append((position[0], position[1]))
    total = max(total, len(heated))

for k in range(len(lines[0])):
    positions = [(k, -1, DOWN)]
    checked = []
    heated = []
    while len(positions) > 0:
        old_pos = positions.copy()
        positions = []
        for position in old_pos:
            temp_new = get_position(position[0], position[1], position[2])
            char = safe_get(temp_new[0], temp_new[1])
            if char == None:
                continue
            if char == ".":
                next = [temp_new]
            elif char in "\\/":
                next = [(temp_new[0], temp_new[1], reflect(char, temp_new[2]))]
            elif char in "|-":
                next = [(temp_new[0], temp_new[1], i) for i in split(char, temp_new[2])]
            else:
                raise Exception("unknown char")
            for i in next:
                if i not in checked:
                    checked.append(i)
                    positions.append(i)
        for position in positions:
            if (position[0], position[1]) not in heated:
                heated.append((position[0], position[1]))
    total = max(total, len(heated))
    positions = [(k, len(lines), UP)]
    checked = []
    heated = []
    while len(positions) > 0:
        old_pos = positions.copy()
        positions = []
        for position in old_pos:
            temp_new = get_position(position[0], position[1], position[2])
            char = safe_get(temp_new[0], temp_new[1])
            if char == None:
                continue
            if char == ".":
                next = [temp_new]
            elif char in "\\/":
                next = [(temp_new[0], temp_new[1], reflect(char, temp_new[2]))]
            elif char in "|-":
                next = [(temp_new[0], temp_new[1], i) for i in split(char, temp_new[2])]
            else:
                raise Exception("unknown char")
            for i in next:
                if i not in checked:
                    checked.append(i)
                    positions.append(i)
        for position in positions:
            if (position[0], position[1]) not in heated:
                heated.append((position[0], position[1]))
    total = max(total, len(heated))

print(total)

tools.stop_clock()
