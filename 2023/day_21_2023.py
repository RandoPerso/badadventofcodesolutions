import aoctools
from copy import deepcopy
import time

tools = aoctools.aoc_tools()

tools.start_clock()

lines = [list(i) for i in tools.get_array_input("2023/inputs/day_21_2023.txt")]

MOVES = 64

start = (-1, -1)

for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char == "S":
            start = (x, y)
            lines[y][x] = "."
            break
    if start != (-1, -1):
        break

frontier = [start]

def safe_get(x, y):
    if x < 0 or y < 0 or x >= len(lines[0]) or y >= len(lines):
        return "#"
    else:
        return lines[y][x]

def tup_add(tup1, tup2):
   return (tup1[0] + tup2[0], tup1[1] + tup2[1])

for i in range(MOVES):
    old_front = frontier.copy()
    frontier = []
    for i in old_front:
        for dir in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            temp = tup_add(i, dir)
            if temp not in frontier and safe_get(temp[0], temp[1]) != "#":
                frontier.append(temp)

print(len(frontier))

tools.stop_clock()

# completed = {}

length = len(lines)

MOVES2 = 26501365
# MOVES2 = 5000

N = 3

MOVES3 = (131 * N) + 65

def safe_get2(x, y):
    return lines[y % length][x % length]

def safe_get(x, y):
    if x < 0 or y < 0 or x >= len(lines[0]) or y >= len(lines):
        return (lines[y % length][x % length],)
    else:
        return lines[y][x]

"""frontier = {((0, 0), start)}

for i in range(MOVES2):
    old_front = frontier.copy()
    frontier = set()
    for i in old_front:
        for dir in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            temp = tup_add(i[1], dir)
            temp2 = safe_get(temp[0], temp[1])
            if type(temp2) != tuple:
                if temp2 != "#":
                    frontier.add((i[0], temp))
            else:
                if temp2[0] != "#":
                    match dir:
                        case (1, 0):
                            next_thing = tup_add(temp, (-length, 0))
                        case (0, 1):
                            next_thing = tup_add(temp, (0, -length))
                        case (-1, 0):
                            next_thing = tup_add(temp, (length, 0))
                        case (0, -1):
                            next_thing = tup_add(temp, (0, length))
                    next_dimension = tup_add(i[0], dir)
                    frontier.add((next_dimension, next_thing))

print(len(frontier))"""

"""checker = set()
top = [set([(i, 0) for i in range(length) if i % 2 == 0]), set([(i, 0) for i in range(length) if i % 2 == 1])]
bot = [set([(i, length - 1) for i in range(length) if i % 2 == 0]), set([(i, length - 1) for i in range(length) if i % 2 == 1])]
lef = [set([(0, i) for i in range(length) if i % 2 == 0]), set([(0, i) for i in range(length) if i % 2 == 1])]
rig = [set([(length - 1, i) for i in range(length) if i % 2 == 0]), set([(length - 1, i) for i in range(length) if i % 2 == 1])]

for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if (x + y) % 2 == 0 and char != "#":
            checker.add((x, y))

frontier = {(0, 0): set((start,))}

for k in range(MOVES2):
    old_front = deepcopy(frontier)
    frontier = dict()
    for j in old_front:
        if j not in frontier:
            frontier[j] = set()
        for dir in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            next_dimension = tup_add(j, dir)
            if next_dimension in completed:
                match dir:
                    case (1, 0):
                        frontier[j].update(lef[completed[next_dimension]])
                    case (0, 1):
                        frontier[j].update(top[completed[next_dimension]])
                    case (-1, 0):
                        frontier[j].update(rig[completed[next_dimension]])
                    case (0, -1):
                        frontier[j].update(bot[completed[next_dimension]])
        for i in old_front[j]:
            for dir in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                temp = tup_add(i, dir)
                temp2 = safe_get(temp[0], temp[1])
                if type(temp2) != tuple:
                    if temp2 != "#":
                        frontier[j].add(temp)
                else:
                    if temp2[0] != "#":
                        next_dimension = tup_add(j, dir)
                        if next_dimension in completed:
                            continue
                        match dir:
                            case (1, 0):
                                next_thing = tup_add(temp, (-length, 0))
                            case (0, 1):
                                next_thing = tup_add(temp, (0, -length))
                            case (-1, 0):
                                next_thing = tup_add(temp, (length, 0))
                            case (0, -1):
                                next_thing = tup_add(temp, (0, length))
                        if next_dimension not in frontier:
                            frontier[next_dimension] = set()
                        frontier[next_dimension].add(next_thing)
    for j in completed:
        completed[j] = (completed[j] + 1) % 2
    for j in deepcopy(frontier):
        if frontier[j] == checker:
            frontier.pop(j)
            completed[j] = 1

total = 0
for j in frontier:
    total += len(frontier[j])

temp4 = int(length * length - 0.5)
for j in completed:
    total += temp4 + completed[j]

print(total)"""

"""frontier = set((start,))
older_front = set()
contained = set()

for i in range(MOVES2):
    old_front = frontier.copy()
    frontier = set()
    for j in old_front:
        for dir in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            temp = tup_add(j, dir)
            if temp not in older_front and safe_get2(temp[0], temp[1]) != "#":
                frontier.add(temp)
                contained.add(temp)
    older_front = old_front.copy()
    if i % 1000 == 0:
        print(100 * i / MOVES2)

total = 0

for j in contained:
    if sum(j) % 2 == MOVES2 % 2:
        total += 1

print(total)"""

"""tools.start_clock()

frontier = set((start,))
older_front = set()

total = 0

if MOVES2 % 2 == 0:
    total += 1

parity = (MOVES2 % 2) + 1

for i in range(MOVES2):
    old_front = frontier.copy()
    frontier = set()
    for j in old_front:
        for dir in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            temp = tup_add(j, dir)
            if temp not in older_front and safe_get2(temp[0], temp[1]) != "#":
                frontier.add(temp)
    older_front = old_front.copy()
    if i % 2 == parity:
        total += len(frontier)
    if i % 1000 == 0:
        print(100 * i / MOVES2, time.time() - tools.clock)

print(total)"""

frontier = {(0, 0): set((start,))}

for k in range(MOVES3):
    old_front = deepcopy(frontier)
    frontier = dict()
    for j in old_front:
        if j not in frontier:
            frontier[j] = set()
        for i in old_front[j]:
            for dir in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                temp = tup_add(i, dir)
                temp2 = safe_get(temp[0], temp[1])
                if type(temp2) != tuple:
                    if temp2 != "#":
                        frontier[j].add(temp)
                else:
                    if temp2[0] != "#":
                        next_dimension = tup_add(j, dir)
                        match dir:
                            case (1, 0):
                                next_thing = tup_add(temp, (-length, 0))
                            case (0, 1):
                                next_thing = tup_add(temp, (0, -length))
                            case (-1, 0):
                                next_thing = tup_add(temp, (length, 0))
                            case (0, -1):
                                next_thing = tup_add(temp, (0, length))
                        if next_dimension not in frontier:
                            frontier[next_dimension] = set()
                        frontier[next_dimension].add(next_thing)

total = 0

M = 202300

"""print(len(frontier[(0, 0)]))
print(len(frontier[(1, 0)]))"""

total += (M ** 2) * len(frontier[(0, 0)])
total += ((M - 1) ** 2) * len(frontier[(1, 0)])

"""print(len(frontier[(N, 0)]))
print(len(frontier[(-N, 0)]))
print(len(frontier[(0, N)]))
print(len(frontier[(0, -N)]))"""

total += len(frontier[(N, 0)])
total += len(frontier[(-N, 0)])
total += len(frontier[(0, N)])
total += len(frontier[(0, -N)])

"""print(len(frontier[(N, 1)]))
print(len(frontier[(N, -1)]))
print(len(frontier[(-N, 1)]))
print(len(frontier[(-N, -1)]))"""

total += len(frontier[(N, 1)]) * M
total += len(frontier[(N, -1)]) * M
total += len(frontier[(-N, 1)]) * M
total += len(frontier[(-N, -1)]) * M

"""print(len(frontier[(N - 1, 1)]))
print(len(frontier[(N - 1, -1)]))
print(len(frontier[(-N + 1, 1)]))
print(len(frontier[(-N + 1, -1)]))"""

total += len(frontier[(N - 1, 1)]) * (M - 1)
total += len(frontier[(N - 1, -1)]) * (M - 1)
total += len(frontier[(-N + 1, 1)]) * (M - 1)
total += len(frontier[(-N + 1, -1)]) * (M - 1)

print(total)

tools.stop_clock()