import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()
lines = tools.get_array_input("2024/inputs/day_7_2024.txt")

total = 0
for line in lines:
    things = line.split()
    desire = int(things[0][:-1])
    things.pop(0)
    numbers = [int(i) for i in things]
    numbers.reverse()
    frontier = {desire}
    pointer = 0
    while pointer < len(numbers):
        new_front = set()
        for number in frontier:
            if number % numbers[pointer] == 0:
                new_front.add(number // numbers[pointer])
            if number >= numbers[pointer]:
                new_front.add(number - numbers[pointer])
        pointer += 1
        frontier = new_front
    if 0 in frontier:
        total += desire

print(total)

tools.stop_clock()

total = 0
for line in lines:
    things = line.split()
    desire = int(things[0][:-1])
    things.pop(0)
    numbers = [int(i) for i in things]
    numbers.reverse()
    frontier = {desire}
    pointer = 0
    while pointer < len(numbers):
        new_front = set()
        for number in frontier:
            if number % numbers[pointer] == 0:
                new_front.add(number // numbers[pointer])
            if number >= numbers[pointer]:
                new_front.add(number - numbers[pointer])
            if len(str(number)) > len(str(numbers[pointer])) and str(number)[-len(str(numbers[pointer])):] == str(numbers[pointer]):
                new_front.add(int(str(number)[:-len(str(numbers[pointer]))]))
        pointer += 1
        frontier = new_front
    if 0 in frontier:
        total += desire

print(total)

tools.stop_clock()