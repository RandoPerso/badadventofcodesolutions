import aoctools

tools = aoctools.aoc_tools()

tools.start_clock()

preinput = tools.get_array_input("2016/inputs/day_16_2016.txt")

preinput.pop(0)
preinput.pop(0)

lookupAvai = {}

def safe_inc(item):
    if item in lookupAvai:
        lookupAvai[item] += 1
    else:
        lookupAvai[item] = 1

for line in preinput:
    temp = line.split()
    safe_inc(int(temp[3][:-1]))

total = 0
for line in preinput:
    temp = line.split()
    used = int(temp[2][:-1])
    if used == 0:
        continue
    avai = int(temp[3][:-1])
    if avai >= used:
        total -= 1
    for value in lookupAvai:
        if value >= used:
            total += lookupAvai[value]

print(total)

tools.stop_clock()