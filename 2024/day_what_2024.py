import aoctools
from copy import deepcopy
from sympy.ntheory.modular import crt

tools = aoctools.aoc_tools()

tools.start_clock()
lines = tools.get_array_input("2024/inputs/day_what_2024.txt")

lengths = []
offsets = []
for line in lines:
    total = 0
    for char in line:
        if char == "O":
            offsets.append(total)
            total += 2
        elif char == "-":
            total += 2
        else:
            total += 1
    lengths.append(total)

time_to_same = crt(lengths, offsets)[0]

print(time_to_same)

tools.stop_clock()

previous_hit = -1

relative = []

for i in range(time_to_same):
    for modulo, residue in zip(lengths, offsets):
        if i % modulo == residue:
            if previous_hit != -1:
                relative.append(i - previous_hit)
            previous_hit = i
            break

absolute = [0]

for angle in relative:
    absolute.append((absolute[-1] + angle * 30 - 180) % 360)

print(absolute.count(0))

tools.stop_clock()