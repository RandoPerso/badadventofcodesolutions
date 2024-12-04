import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()
lines = tools.get_array_input("2024/inputs/day_2_2024.txt")

def is_pos(x):
    return x > 0

total = 0
for line in lines:
    numbers = [int(i) for i in line.split()]
    pos = is_pos(numbers[1] - numbers[0])
    for i in range(len(numbers) - 1):
        if abs(numbers[i+1]-numbers[i]) > 3 or numbers[i+1]==numbers[i]:
            break
        if is_pos(numbers[i+1]-numbers[i]) != pos:
            break
    else:
        total += 1

print(total)

tools.stop_clock()

def is_safe(numbers):
    pos = is_pos(numbers[1] - numbers[0])
    for i in range(len(numbers) - 1):
        if abs(numbers[i+1]-numbers[i]) > 3 or numbers[i+1]==numbers[i]:
            return False
        if is_pos(numbers[i+1]-numbers[i]) != pos:
            return False
    else:
        return True

total = 0
for line in lines:
    numbers = [int(i) for i in line.split()]
    if is_safe(numbers):
        total += 1
    else:
        for i in range(len(numbers)):
            new_num = numbers.copy()
            new_num.pop(i)
            if is_safe(new_num):
                total += 1
                break

print(total)

tools.stop_clock()