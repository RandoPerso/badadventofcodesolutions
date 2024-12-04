import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()

lines = tools.get_array_input("2023/inputs/day_22_2023.txt")

temp_bricks = []

for line in lines:
    temp = line.split("~")
    temp_bricks.append([[int(i) for i in temp[0].split(",")], [int(i) for i in temp[1].split(",")]])

bricks = {}

for brick in temp_bricks:
    position = max(brick[0][2], brick[1][2])
    height = abs(brick[1][2] - brick[0][2])
    x = [brick[0][0], brick[1][0]]
    y = [brick[0][1], brick[1][1]]
    x.sort()
    y.sort()
    if position not in bricks:
        bricks[position] = []
    bricks[position].append((height, x[0], x[1], y[0], y[1]))

def intersecting(x1, x2, y1, y2, x3, x4, y3, y4):
    x5 = max(x1, x3)
    y5 = max(y1, y3)
    x6 = min(x2, x4)
    y6 = min(y2, y4)
    if (x5 > x6) or (y5 > y6):
        return False
    return True

def safe_add(where, item):
    if where not in bricks:
        bricks[where] = []
    bricks[where].append(item)

while True:
    old_bricks = deepcopy(bricks)
    bricks = {}
    for i in old_bricks:
        for j in old_bricks[i]:
            next_layer = i - j[0] - 1
            if next_layer < 0:
                raise Exception("help help help")
            if next_layer == 0:
                safe_add(i, j)
                continue
            if next_layer not in old_bricks:
                safe_add(i - 1, j)
                continue
            for k in old_bricks[next_layer]:
                if intersecting(k[1], k[2], k[3], k[4], j[1], j[2], j[3], j[4]):
                    safe_add(i, j)
                    break
            else:
                safe_add(i - 1, j)
    if bricks == old_bricks:
        break

unsafe = set()

for i in bricks:
    for j in bricks[i]:
        next_layer = i - j[0] - 1
        if next_layer < 0:
            raise Exception("help help help")
        if next_layer == 0:
            continue
        temp = []
        for ind, k in enumerate(bricks[next_layer]):
            if intersecting(k[1], k[2], k[3], k[4], j[1], j[2], j[3], j[4]):
                if temp:
                    break
                temp.append(ind)
        else:
            unsafe.add((next_layer, temp[0]))

print(len(lines) - len(unsafe))

tools.stop_clock()

supports = {}

for i in bricks:
    for ind_j, j in enumerate(bricks[i]):
        next_layer = i - j[0] - 1
        if next_layer < 0:
            raise Exception("help help help")
        if next_layer == 0:
            continue
        temp = []
        for ind, k in enumerate(bricks[next_layer]):
            if intersecting(k[1], k[2], k[3], k[4], j[1], j[2], j[3], j[4]):
                temp.append((next_layer, ind))
        supports[(i, ind_j)] = temp

def safe_add2(where, item):
    if where not in anti_supports:
        anti_supports[where] = []
    anti_supports[where].append(item)

anti_supports = {}

for i in supports:
    for j in supports[i]:
        safe_add2(j, i)

total = 0

for k in anti_supports:
    t_sup = deepcopy(supports)
    t_ant = deepcopy(anti_supports)
    handle = [k]
    while handle:
        temp = handle.pop()
        if temp not in t_ant:
            continue
        for i in t_ant[temp]:
            t_sup[i].remove(temp)
            if len(t_sup[i]) == 0:
                handle.append(i)
                total += 1

print(total)

tools.stop_clock()