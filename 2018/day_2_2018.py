import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()
lines = tools.get_array_input("2018/inputs/day_2_2018.txt")

counted_2 = set()
counted_3 = set()
for line in lines:
    for char in set(line):
        if line.count(char) == 2:
            counted_2.add(line)
        if line.count(char) == 3:
            counted_3.add(line)

print(len(counted_2) * len(counted_3))

tools.stop_clock()

def one_away(x, y):
    mistake = False
    for index, char in enumerate(x):
        if char != y[index]:
            if mistake:
                return False
            mistake = True
    return mistake

for index, line in enumerate(lines):
    for line2 in lines[index + 1:]:
        if one_away(line, line2):
            for index, char in enumerate(line):
                if char == line2[index]:
                    print(char, end="")
            print("")

tools.stop_clock()