import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()

lines = tools.get_array_input("2023/inputs/day_1_2023.txt")
sum = 0

for line in lines:
    temp = ""
    for char in line:
        try:
            temp2 = int(char)
            temp += char
        except:
            pass
    sum += int(temp[0] + temp[-1])

print(sum)

tools.stop_clock()

sum = 0

for line in lines:
    temp1 = []
    temp2 = []
    numbers = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    for index, i in enumerate(numbers):
        if line.find(i) != -1:
            temp1.append((index, line.find(i)))
    for index, i in enumerate(numbers):
        if line[::-1].find(i[::-1]) != -1:
            temp2.append((index, line[::-1].find(i[::-1])))
    for numbers in range(10):
        if line.find(str(numbers)) != -1:
            temp1.append((numbers, line.find(str(numbers))))
        if line[::-1].find(str(numbers)) != -1:
            temp2.append((numbers, line[::-1].find(str(numbers)[::-1])))
    temp1.sort(reverse=False, key=lambda a: a[1])
    temp2.sort(reverse=False, key=lambda a: a[1])
    sum += temp1[0][0] * 10 + temp2[0][0]

print(sum)

tools.stop_clock()