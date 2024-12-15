import aoctools
from copy import deepcopy
from re import match

tools = aoctools.aoc_tools()

tools.start_clock()
lines = tools.get_array_input("2024/inputs/day_15_2024.txt")

dirs = ((0, -1), (1, 0), (0, 1), (-1, 0))

walls = set()
boxes = set()
instructions = []

MAX_X = len(lines[0])

making_grid = True
for y, line in enumerate(lines):
    if line == "":
        MAX_Y = y - 1
        making_grid = False
        continue
    if making_grid == True:
        for x, char in enumerate(line):
            if char == "#":
                walls.add((x, y))
            elif char == "O":
                boxes.add((x, y))
            elif char == "@":
                robot = (x, y)
    else:
        instructions.append(line)

def in_bound(position):
    if position[0] <= 0 or position[1] <= 0 or position[0] >= MAX_X or position[1] >= MAX_Y:
        return False
    return True

def tup_add(x, y):
    return (x[0] + y[0], x[1] + y[1])

def show_state():
    for y in range(MAX_Y + 1):
        for x in range(MAX_X):
            if (x, y) in walls:
                print("#", end="")
            elif (x, y) in boxes:
                print("O", end="")
            elif (x, y) == robot:
                print("@", end="")
            else:
                print(".", end="")
        print("")

for line in instructions:
    for char in line:
        # show_state()
        new = tup_add(robot, dirs["^>v<".index(char)])
        if not in_bound(new) or new in walls:
            continue
        if new in boxes:
            checking = new
            while checking in boxes:
                checking = tup_add(checking, dirs["^>v<".index(char)])
            if not in_bound(checking) or checking in walls:
                continue
            boxes.remove(new)
            boxes.add(checking)
        robot = new


total = 0
for box in boxes:
    total += 100 * box[1] + box[0]

print(total)

tools.stop_clock()

walls = set()
left_boxes = set()
right_boxes = set()

MAX_X = MAX_X * 2

def show_state():
    for y in range(MAX_Y + 1):
        for x in range(MAX_X):
            if (x, y) in walls:
                print("#", end="")
            elif (x, y) in left_boxes:
                print("[", end="")
            elif (x, y) in right_boxes:
                print("]", end="")
            elif (x, y) == robot:
                print("@", end="")
            else:
                print(".", end="")
        print("")

making_grid = True
for y, line in enumerate(lines):
    if line == "":
        making_grid = False
        continue
    if making_grid == True:
        for x, char in enumerate(line):
            if char == "#":
                walls.add((2*x, y))
                walls.add((2*x + 1, y))
            elif char == "O":
                left_boxes.add((2*x, y))
                right_boxes.add((2*x + 1, y))
            elif char == "@":
                robot = (2*x, y)
    else:
        break

for line in instructions:
    for char in line:
        #show_state()
        direction = dirs["^>v<".index(char)]
        new = tup_add(robot, direction)
        if new in walls:
            continue
        match char:
            case "^" | "v":
                if new in left_boxes or new in right_boxes:
                    check_stack = []
                    check_stack.append(new)
                    left_add = set()
                    left_remove = set()
                    right_add = set()
                    right_remove = set()
                    passing = True
                    while check_stack:
                        checking = check_stack.pop()
                        if checking in walls:
                            passing = False
                            break
                        if checking in left_boxes:
                            left_remove.add(checking)
                            left_add.add(tup_add(checking, direction))
                            check_stack.append(tup_add(checking, direction))
                            right_remove.add(tup_add(checking, (1, 0)))
                            right_add.add(tup_add(tup_add(checking, (1, 0)), direction))
                            check_stack.append(tup_add(tup_add(checking, (1, 0)), direction))
                        elif checking in right_boxes:
                            right_remove.add(checking)
                            right_add.add(tup_add(checking, direction))
                            check_stack.append(tup_add(checking, direction))
                            left_remove.add(tup_add(checking, (-1, 0)))
                            left_add.add(tup_add(tup_add(checking, (-1, 0)), direction))
                            check_stack.append(tup_add(tup_add(checking, (-1, 0)), direction))
                    if not passing:
                        continue
                    for location in left_remove:
                        left_boxes.remove(location)
                    for location in left_add:
                        left_boxes.add(location)
                    for location in right_remove:
                        right_boxes.remove(location)
                    for location in right_add:
                        right_boxes.add(location)
            case ">":
                if new in left_boxes:
                    left_add = []
                    left_remove = []
                    right_add = []
                    right_remove = []
                    checking = new
                    while checking in left_boxes:
                        left_remove.append(checking)
                        right_remove.append(tup_add(checking, (1, 0)))
                        checking = tup_add(checking, (2, 0))
                        left_add.append(tup_add(checking, (-1, 0)))
                        right_add.append(checking)
                    if checking in walls:
                        continue
                    for location in left_remove:
                        left_boxes.remove(location)
                    for location in left_add:
                        left_boxes.add(location)
                    for location in right_remove:
                        right_boxes.remove(location)
                    for location in right_add:
                        right_boxes.add(location)
            case "<":
                if new in right_boxes:
                    left_add = []
                    left_remove = []
                    right_add = []
                    right_remove = []
                    checking = new
                    while checking in right_boxes:
                        right_remove.append(checking)
                        left_remove.append(tup_add(checking, (-1, 0)))
                        checking = (checking[0] - 2, checking[1])
                        right_add.append(tup_add(checking, (1, 0)))
                        left_add.append(checking)
                    if checking in walls:
                        continue
                    for location in left_remove:
                        left_boxes.remove(location)
                    for location in left_add:
                        left_boxes.add(location)
                    for location in right_remove:
                        right_boxes.remove(location)
                    for location in right_add:
                        right_boxes.add(location)
        robot = new

# show_state()

total = 0
for box in left_boxes:
    total += 100 * box[1] + box[0]

print(total)

tools.stop_clock()