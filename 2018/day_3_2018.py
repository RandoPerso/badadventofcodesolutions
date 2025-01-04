import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()
lines = tools.get_array_input("2018/inputs/day_3_2018.txt")

claims = []
for line in lines:
    temp = line.split()
    position = tuple(int(i) for i in temp[2][:-1].split(","))
    size = tuple(int(i) for i in temp[3].split("x"))
    claims.append((position[0], position[0] + size[0], position[1], position[1] + size[1]))

total = 0
for x in range(1000):
    for y in range(1000):
        matched = False
        for claim in claims:
            if x >= claim[0] and x < claim[1] and y >= claim[2] and y < claim[3]:
                if matched:
                    total += 1
                    break
                matched = True

print(total)

tools.stop_clock()

for index, claim in enumerate(claims):
    passing = True
    for x in range(claim[0], claim[1]):
        for y in range(claim[2], claim[3]):
            for test in claims:
                if claim == test:
                    continue
                if x >= test[0] and x < test[1] and y >= test[2] and y < test[3]:
                    passing = False
                    break
            if not passing:
                break
        if not passing:
            break
    if passing:
        print(index + 1)
        break
            
tools.stop_clock()