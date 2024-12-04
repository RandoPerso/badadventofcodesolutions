import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()

lines = tools.get_array_input("2023/inputs/day_19_2023.txt")

def get_stats(string: str):
    temp = []
    temp2 = ""
    for char in string:
        if char.isnumeric():
            temp2 += char
        elif temp2 != "":
            temp.append(int(temp2))
            temp2 = ""
    return temp

def get_individual(string: str):
    temp = string.split("{")
    name = temp[0]
    temp2 = temp[1][:-1].split(",")
    for ind, i in enumerate(temp2):
        if ":" in i:
            temp3 = i.split(":")
            temp4 = (temp3[0][0], temp3[0][1], int(temp3[0][2:]), temp3[1])
            temp2[ind] = temp4
    return {name: temp2}

rules = {}
objects = []
ended_rules = False
for line in lines:
    if len(line) < 2:
        ended_rules = True
        continue
    if ended_rules:
        objects.append(get_stats(line))
    else:
        rules.update(get_individual(line))

xmas = {"x": 0, "m": 1, "a": 2, "s": 3}
total = 0

for j in objects:
    location = "in"
    while location not in ("A", "R"):
        for rule in rules[location]:
            if type(rule) == str:
                location = rule
                break
            else:
                if eval(str(j[xmas[rule[0]]]) + rule[1] + str(rule[2])):
                    location = rule[3]
                    break
    if location == "A":
        total += sum(j)

print(total)

def calc_diff(pair):
    return pair[1] - pair[0] + 1

total = 0
start = [[1, 4000], [1, 4000], [1, 4000], [1, 4000], "in"]
frontier = [start]

while len(frontier) > 0:
    place = frontier.pop()
    location = place[-1]
    if location == "A":
        total += calc_diff(place[0]) * calc_diff(place[1]) * calc_diff(place[2]) * calc_diff(place[3])
        continue
    elif location == "R":
        continue
    for rule in rules[location]:
        if type(rule) == str:
            place[-1] = rule
            frontier.append(place)
        else:
            checker = xmas[rule[0]]
            match rule[1]:
                case ">":
                    if place[checker][1] > rule[2]:
                        temp = deepcopy(place)
                        temp[checker][0] = rule[2] + 1
                        temp[-1] = rule[3]
                        frontier.append(temp)
                    if place[checker][0] <= rule[2]:
                        place[checker][1] = rule[2]
                    else:
                        break
                case "<":
                    if place[checker][0] < rule[2]:
                        temp = deepcopy(place)
                        temp[checker][1] = rule[2] - 1
                        temp[-1] = rule[3]
                        frontier.append(temp)
                    if place[checker][1] >= rule[2]:
                        place[checker][0] = rule[2]
                    else:
                        break

print(total)

tools.stop_clock()