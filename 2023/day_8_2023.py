import aoctools
from copy import deepcopy
from sympy.ntheory.modular import crt

tools = aoctools.aoc_tools()

tools.start_clock()

lines = tools.get_array_input("2023/inputs/day_8_2023.txt")

sequence = lines[0]

maps = {}

for line in lines[2:]:
    temp = line.split()
    maps.update({temp[0]: (temp[2][1:4], temp[3][:3])})

total = 0
index = 0
location = "AAA"
while location != "ZZZ":
    total += 1
    location = maps[location][0 if sequence[index] == "L" else 1]
    index = (index + 1) % len(sequence)

print(total)

tools.stop_clock()

locations = []
seen = []
seen_2 = []
for mapping in list(maps.keys()):
    if mapping[-1] == "A":
        locations.append(mapping)
        seen.append([mapping])
        seen_2.append([])

between = [0, 0, 0, 0, 0, 0]

"""total = 0
index = 0
while sum([False if i[-1] == "Z" else True for i in locations]) != 0:
    total += 1
    for i in locations:
        i = maps[i][0 if sequence[index] == "L" else 1]
    index = (index + 1) % len(sequence)"""

total = 0
index = 0
correct_index = 0
while sum([True if len(seen[i]) != len(list(set(seen[i]))) else False for i in range(len(locations))]) != len(locations):
    total += 1
    for ind, i in enumerate(locations):
        locations[ind] = maps[i][0 if sequence[index] == "L" else 1]
        if locations[ind][-1] == "Z":
            between[ind] = seen[ind][-1]
            correct_index = index
    index = (index + 1) % len(sequence)
    if index == 0:
        for ind, i in enumerate(locations):
            if len(seen[ind]) != len(list(set(seen[ind]))):
                continue
            seen[ind].append(i)

while len(seen_2) == 0 or sum([True if len(seen_2[i]) != len(list(set(seen_2[i]))) else False for i in range(len(locations))]) != len(locations):
    total += 1
    for ind, i in enumerate(locations):
        locations[ind] = maps[i][0 if sequence[index] == "L" else 1]
    index = (index + 1) % len(sequence)
    if index == 0:
        for ind, i in enumerate(locations):
            if len(seen_2[ind]) != len(list(set(seen_2[ind]))):
                continue
            seen_2[ind].append(i)

# print(seen_2)
# print(seen)
# print(between)
# print(total)

looper = []

for i in seen_2:
    while True:
        if i[0] == i[-1]:
            i.pop(0)
            looper.append(i)
            break
        else:
            i.pop(0)

# print(seen)

"""while locations != between:
    total += len(sequence)
    for ind, place in enumerate(locations):
        locations[ind] = looper[ind][(looper[ind].index(place) + 1) % len(looper[ind])]"""

temp = crt([len(i) for i in looper], [(looper[ind].index(between[ind]) - looper[ind].index(i)) % len(looper[ind]) for ind, i in enumerate(locations)])[0]

total += temp * len(sequence)
print(total + correct_index + 1)

"""locations = [looper[ind][(looper[ind].index(i) + temp) % len(looper[ind])] for ind, i in enumerate(locations)]

while sum([False if i[-1] == "Z" else True for i in locations]) != 0:
    total += 1
    for ind, i in enumerate(locations):
        locations[ind] = maps[i][0 if sequence[index] == "L" else 1]
    index = (index + 1) % len(sequence)

print(total)"""

tools.stop_clock()