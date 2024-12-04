import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()
lines = tools.get_array_input("2024/inputs/day_1_2024.txt")

list_a = []
list_b = []

for line in lines:
    temp = line.split()
    list_a.append(int(temp[0]))
    list_b.append(int(temp[1]))

list_a.sort()
list_b.sort()

total = 0
for i in range(len(list_a)):
    total += abs(list_a[i] - list_b[i])

print(total)

tools.stop_clock()

total = 0
for i in list_a:
    total += i * list_b.count(i)

print(total)

tools.stop_clock()