import aoctools
from copy import deepcopy
import re

tools = aoctools.aoc_tools()

tools.start_clock()
line = tools.get_line_input("2024/inputs/day_3_2024.txt")

total = 0
instruct = re.findall("mul\(\d+,\d+\)", line)
for thing in instruct:
    total += int(thing[4:-1].split(",")[0]) * int(thing[4:-1].split(",")[1])

print(total)

tools.stop_clock()

total = 0
active = True
instruct = re.findall("mul\(\d+,\d+\)|do\(\)|don't\(\)", line)
for thing in instruct:
    if thing == "do()":
        active = True
    elif thing == "don't()":
        active = False
    elif active:
        total += int(thing[4:-1].split(",")[0]) * int(thing[4:-1].split(",")[1])

print(total)

tools.stop_clock()