import aoctools
import numpy as np
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()

line = tools.get_line_input("2023/inputs/day_15_2023.txt")
strings = line.split(",")

def hash_char(value, character):
    return ((value + ord(character)) * 17) % 256

def hash_string(string):
    value = 0
    for i in string:
        value = hash_char(value, i)
    return value

total = 0
for string in strings:
    total += hash_string(string)

print(total)

tools.stop_clock()

boxes = [[] for i in range(256)]
boxes_2 = [[] for i in range(256)]

for i in strings:
    if i[-1] == "-":
        number = hash_string(i[:-1])
        if i[:-1] in boxes[number]:
            index = boxes[number].index(i[:-1])
            boxes[number].pop(index)
            boxes_2[number].pop(index)
    else:
        number = hash_string(i[:-2])
        if i[:-2] in boxes[number]:
            boxes_2[number][boxes[number].index(i[:-2])] = int(i[-1])
        else:
            boxes[number].append(i[:-2])
            boxes_2[number].append(int(i[-1]))

total = 0
for i in range(256):
    for j in range(len(boxes[i])):
        total += (i + 1) * (j + 1) * boxes_2[i][j]

print(total)

tools.stop_clock()