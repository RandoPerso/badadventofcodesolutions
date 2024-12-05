import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()
lines = tools.get_array_input("2024/inputs/day_5_2024.txt")

total = 0
rules = []
wrong = []
started = False
for line in lines:
    if started:
        update = line.split(",")
        for rule in rules:
            #if re.findall(rule[1] + ".*" + rule[0], line):
            if rule[0] in update and rule[1] in update:
                a, b = (update.index(rule[0]), update.index(rule[1]))
                if a > b:
                    wrong.append(line)
                    break
        else:
            total += int(update[int((len(update) - 1)/2) ])
    else:
        if line == "":
            started = True
        else:
            rules.append(line.split("|"))

print(total)

tools.stop_clock()

total = 0
for line in wrong:
    update = line.split(",")
    fixed = False
    while not fixed:
        fixed = True
        for rule in rules:
            if rule[0] in update and rule[1] in update:
                a, b = (update.index(rule[0]), update.index(rule[1]))
                if a > b:
                    fixed = False
                    update[a] = rule[1]
                    update[b] = rule[0]
    total += int(update[int((len(update) - 1)/2) ])

print(total)

tools.stop_clock()