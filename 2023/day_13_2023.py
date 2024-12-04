import aoctools
from copy import deepcopy
import numpy as np

tools = aoctools.aoc_tools()

tools.start_clock()

lines = tools.get_array_input("2023/inputs/day_13_2023.txt")

patterns = []

temp = []
for line in lines:
    if len(line) > 0:
        temp.append([i for i in line])
    else:
        patterns.append(temp)
        temp = []

def check(y_guess, pattern):
    i = 0
    while y_guess - i >= 0 and y_guess + i + 1 < len(pattern):
        if pattern[y_guess - i] != pattern[y_guess + i + 1]:
            return False
        i += 1
    return True

total = 0

for pattern in patterns:
    going = True
    for y_guess in range(len(pattern) - 1):
        if check(y_guess, pattern):
            total += 100 * (y_guess + 1)
            going = False
            break
    if going:
        temp = np.rot90(np.array(pattern), 3).tolist()
        for x_guess in range(len(temp) - 1):
            if check(x_guess, temp):
                total += x_guess + 1
                break

print(total)

tools.stop_clock()

def difference_ok(row1, row2):
    counter = 0
    for i in range(len(row1)):
        if row1[i] != row2[i]:
            counter += 1
        if counter > 1:
            return False
    return True

def check2(y_guess, pattern):
    i = 0
    diff = 0
    while y_guess - i >= 0 and y_guess + i + 1 < len(pattern):
        if pattern[y_guess - i] != pattern[y_guess + i + 1]:
            if difference_ok(pattern[y_guess - i], pattern[y_guess + i + 1]):
                diff += 1
                if diff > 1:
                    return False
            else:
                return False
        i += 1
    if diff == 1:
        return True
    else:
        return False

total = 0

for pattern in patterns:
    going = True
    for y_guess in range(len(pattern) - 1):
        if check2(y_guess, pattern):
            total += 100 * (y_guess + 1)
            going = False
            break
    if going:
        temp = np.rot90(np.array(pattern), 3).tolist()
        for x_guess in range(len(temp) - 1):
            if check2(x_guess, temp):
                total += x_guess + 1
                break

print(total)

tools.stop_clock()
