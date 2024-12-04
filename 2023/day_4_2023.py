import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()

lines = tools.get_array_input("2023/inputs/day_4_2023.txt")
total = 0

for line in lines:
    temp_line = line.split()
    winning_numbers = temp_line[2:2+10]
    given = temp_line[2+10+1:]
    temp = [i in winning_numbers for i in given]
    if temp.count(True) == 0:
        pass
    else:
        total += 2 ** (temp.count(True) - 1)

print(total)

tools.stop_clock()

current = [1 for i in range(189)]

for card, line in enumerate(lines):
    temp_line = line.split()
    winning_numbers = temp_line[2:2+10]
    given = temp_line[2+10+1:]
    temp = [i in winning_numbers for i in given]
    for i in range(temp.count(True)):
        current[card + i + 1] += current[card]

print(sum(current))

tools.stop_clock()