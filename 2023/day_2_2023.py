import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()

lines = tools.get_array_input("2023/inputs/day_2_2023.txt")
total = 0

for line in lines:
    temp_line = str(line).split()
    works = True
    for index, word in enumerate(temp_line):
        try:
            temp2 = int(word)
            if temp_line[index+1].find("green") != -1:
                if temp2 > 13:
                    works = False
            if temp_line[index+1].find("red") != -1:
                if temp2 > 12:
                    works = False
            if temp_line[index+1].find("blue") != -1:
                if temp2 > 14:
                    works = False
        except:
            pass
    if works:
        total += int(temp_line[1][:-1])

print(total)

tools.stop_clock()

total = 0

for line in lines:
    temp_line = str(line).split()
    max_green = 0
    max_red = 0
    max_blue = 0
    for index, word in enumerate(temp_line):
        try:
            temp2 = int(word)
            if temp_line[index+1].find("green") != -1:
                if temp2 > max_green:
                    max_green = temp2
            if temp_line[index+1].find("red") != -1:
                if temp2 > max_red:
                    max_red = temp2
            if temp_line[index+1].find("blue") != -1:
                if temp2 > max_blue:
                    max_blue = temp2
        except:
            pass
    total += max_red * max_green * max_blue

print(total)

tools.stop_clock()