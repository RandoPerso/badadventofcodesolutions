import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()
lines = tools.get_array_input("2018/inputs/day_1_2018.txt")

total = 0

for line in lines:
    total += int(line)

print(total)

tools.stop_clock()

visited = {0}
current = 0
index = 0

while True:
    current += int(lines[index])
    if current in visited:
        print(current)
        break
    visited.add(current)
    index = (index + 1) % len(lines)

tools.stop_clock()