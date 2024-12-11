import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()
line = tools.get_line_input("2024/inputs/day_11_2024.txt")

stones = [int(i) for i in line.split()]

for i in range(25):
    new_stones = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
        elif len(str(stone)) % 2 == 0:
            new_stones.append(int(str(stone)[:int(len(str(stone))/2)]))
            new_stones.append(int(str(stone)[int(len(str(stone))/2):]))
        else:
            new_stones.append(stone * 2024)
    stones = new_stones

print(len(stones))

tools.stop_clock()

smart_stones = {}
for stone in stones:
    if stone in smart_stones:
        smart_stones[stone] += 1
    else:
        smart_stones[stone] = 1

def safe_edit(object, z, value):
    if z in object:
        object[z] += value
    else:
        object[z] = value

for i in range(50):
    new_stones = {}
    for stone in smart_stones:
        if stone == 0:
            safe_edit(new_stones, 1, smart_stones[stone])
        elif len(str(stone)) % 2 == 0:
            safe_edit(new_stones, int(str(stone)[:int(len(str(stone))/2)]), smart_stones[stone])
            safe_edit(new_stones, int(str(stone)[int(len(str(stone))/2):]), smart_stones[stone])
        else:
            safe_edit(new_stones, stone * 2024, smart_stones[stone])
    smart_stones = new_stones

print(sum([smart_stones[i] for i in smart_stones]))

tools.stop_clock()