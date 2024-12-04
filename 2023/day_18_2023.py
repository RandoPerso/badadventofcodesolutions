import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()

lines = tools.get_array_input("2023/inputs/day_18_2023.txt")

directions = [i.split() for i in lines]

def tup_add(tup1, tup2):
   return (tup1[0] + tup2[0], tup1[1] + tup2[1])

def get_fill(direction, length, position):
    if direction == "U":
        return [(position[0], position[1] - i - 1) for i in range(length)]
    if direction == "R":
        return [(position[0] + i + 1, position[1]) for i in range(length)]
    if direction == "D":
        return [(position[0], position[1] + i + 1) for i in range(length)]
    if direction == "L":
        return [(position[0] - i - 1, position[1]) for i in range(length)]

edge = []

last = (0, 0)

for direction in directions:
    temp = get_fill(direction[0], int(direction[1]), last)
    edge.extend(temp)
    last = temp[-1]

temp5 = edge.copy()

x_max = -99999
x_min = 99999
y_max = -99999
y_min = 99999
for i in edge:
    if i[0] > x_max:
        x_max = i[0]
    if i[0] < x_min:
        x_min = i[0]
    if i[1] > y_max:
        y_max = i[1]
    if i[1] < y_min:
        y_min = i[1]

dirs = ((0, -1), (1, 0), (0, 1), (-1, 0))

for i in ((1, 1), (1, -1), (-1, -1), (-1, 1)):
    fail = False
    start = i
    contain = edge.copy()
    contain.append(start)
    frontier = [start]

    while len(frontier) > 0:
        place = frontier.pop()
        for i in dirs:
            temp2 = tup_add(place, i)
            if temp2 not in contain:
                if temp2[0] < x_min or temp2[0] > x_max or temp2[1] < y_min or temp2[1] > y_max:
                    fail = True
                frontier.append(temp2)
                contain.append(temp2)
            if fail:
                break
        if fail:
            break
    
    if not fail:
        break

if fail:
    raise Exception("OH NO")
print(len(contain))

tools.stop_clock()

def hex_decode(number):
    numb = int(number[2:7], base=16)
    match number[7]:
        case "0":
            dir = "R"
        case "1":
            dir = "D"
        case "2":
            dir = "L"
        case "3":
            dir = "U"
    return (dir, numb)

x_max = -99999999
x_min = 99999999
y_max = -99999999
y_min = 99999999

def get_fill2(direction, length, position):
    if direction == "U":
        global y_min
        if position[1] - length < y_min:
            y_min = position[1] - length
        return [(position[0], position[1] - length)]
    if direction == "R":
        global x_max
        if position[0] + length > x_max:
            x_max = position[0] + length
        return [(position[0] + i + 1, position[1]) for i in range(length)]
    if direction == "D":
        global y_max
        if position[1] + length > y_max:
            y_max = position[1] + length
        return [(position[0], position[1] + length)]
    if direction == "L":
        global x_min
        if position[0] - length < x_min:
            x_min = position[0] - length
        return [(position[0] - i - 1, position[1]) for i in range(length)]

new_edge = []

last = (0, 0)

for ind in range(len(directions)):
    directions[ind] = hex_decode(directions[ind][2])

for direction in directions:
    temp = get_fill(direction[0], int(direction[1]), last)
    new_edge.extend(temp)
    last = temp[-1]

count_edge = []
vertices = []

last = (0, 0)

for direction in directions:
    temp = get_fill2(direction[0], int(direction[1]), last)
    count_edge.extend(temp)
    last = temp[-1]
    vertices.append(temp[-1])

def in_poly(location):
    corr_x = count_edge[location][0]
    count = 0
    k = location + 1
    m = k
    while count_edge[m][0] == corr_x:
        m += 1
        if m >= len(count_edge):
            return False
    corr_x2 = count_edge[m][0]
    checked = []
    while count_edge[k][0] == corr_x and count_edge[m][0] == corr_x2:
        if count_edge[k][1] == count_edge[m][1]:
            checked.append(count_edge[k])
            count += 1
            k += 1
            m += 1
        elif count_edge[k][1] > count_edge[m][1]:
            k += 1
        else:
            m += 1
        if k >= len(count_edge) or m >= len(count_edge):
            break
    if count % 2 == 1:
        return True
    return False
    """if location in new_edge:
        return False
    else:
        count = 0
        j = -1
        while j + location[1] >= y_min:
            if (location[0], location[1] + j) in count_edge:
                count += 1
            j -= 1
        if count % 2 == 1:
            return True
        return False"""

"""for i in ((1, 1), (1, -1), (-1, -1), (-1, 1)):
    if in_poly(i):
        break

start = i
print(start)

contain = new_edge.copy()
contain.append(start)
frontier = [start]

while len(frontier) > 0:
    place = frontier.pop()
    for i in dirs:
        temp2 = tup_add(place, i)
        if temp2 not in contain:
            frontier.append(temp2)
            contain.append(temp2)

print(len(contain))"""

count_edge.sort(reverse=True)

# new_edge = list(set(new_edge) - set(count_edge))

print("it is starting")

total = 0
multiplier = 1 / (x_max - x_min)

for j in range(len(count_edge) - 1):
    if count_edge[j][0] != count_edge[j + 1][0]:
        continue
    place = tools.safe_search(vertices, count_edge[j])
    if place != -1:
        if directions[(place + 1) % len(directions)][0] == "U" or directions[place][0] == "D":
            continue
    if in_poly(j):
        total += count_edge[j][1] - count_edge[j + 1][1] - 1
    if j % 100000 == 0:
        print((x_max - count_edge[j][0]) * multiplier)

print(total + len(new_edge))

tools.stop_clock()
