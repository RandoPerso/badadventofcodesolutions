import aoctools
from copy import deepcopy
from fractions import Fraction

tools = aoctools.aoc_tools()

tools.start_clock()
lines = tools.get_array_input("2024/inputs/day_13_2024.txt")

def tup_add(x, y):
    return (x[0] + y[0], x[1] + y[1])

def tup_mul(x, const):
    return (x[0]*const, x[1]*const)

def double_check(location, target):
    return location[0] <= target[0] and location[1] <= target[1]

total = 0
button_a = (0, 0)
button_b = (0, 0)
for line in lines:
    temp = line.split()
    if len(temp) == 0:
        continue
    if temp[1] == "A:":
        button_a = (int(temp[2][2:-1]), int(temp[3][2:]))
    elif temp[1] == "B:":
        button_b = (int(temp[2][2:-1]), int(temp[3][2:]))
    else:
        prize = (int(temp[1][2:-1]), int(temp[2][2:]))
        minimum = 600
        for a in range(101):
            for b in range(101):
                if tup_add(tup_mul(button_a, a), tup_mul(button_b, b)) == prize and 3 * a + b < minimum:
                    minimum = 3 * a + b
        if minimum < 600:
            total += minimum

print(total)

tools.stop_clock()

total = 0
button_a = (0, 0)
button_b = (0, 0)
for line in lines:
    temp = line.split()
    if len(temp) == 0:
        continue
    if temp[1] == "A:":
        button_a = (Fraction(temp[2][2:-1]), Fraction(temp[3][2:]))
    elif temp[1] == "B:":
        button_b = (Fraction(temp[2][2:-1]), Fraction(temp[3][2:]))
    else:
        prize = (10000000000000 + Fraction(temp[1][2:-1]), 10000000000000 + Fraction(temp[2][2:]))
        # mathematics, you can set up a system of two linear equations and solve for the coefficients. i solved the following system for a:
        # a * button_a.x + b * button_b.x = prize.x
        # a * button_a.y + b * button_b.y = prize.y
        # i use Fraction since floating point arithmetic :((((
        a = (prize[0] - prize[1] * (button_b[0] / button_b[1])) / (button_a[0] - button_a[1] * (button_b[0] / button_b[1]))
        if a.denominator == 1:
            b = (prize[0] - a * button_a[0]) / button_b[0]
            if b.denominator == 1:
                total += int(a) * 3 + int(b)

print(total)

tools.stop_clock()