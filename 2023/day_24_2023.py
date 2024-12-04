import aoctools
from copy import deepcopy
from sympy import Ray, Point, solve
from sympy.abc import a, b, c, d, e, f, g, h, j

tools = aoctools.aoc_tools()

tools.start_clock()

lines = tools.get_array_input("2023/inputs/day_24_2023.txt")

stones = []

for line in lines:
    temp = line.replace(",", "")
    temp2 = temp.split()
    stones.append((tuple(int(i) for i in temp2[:3]), tuple(int(i) for i in temp2[4:])))

paths = []
for stone in stones:
    paths.append(Ray(Point(stone[0][0], stone[0][1]), Point(stone[0][0] + stone[1][0], stone[0][1] + stone[1][1])))

"""MIN_SEARCH = 7
MAX_SEARCH = 27"""

MIN_SEARCH = 200000000000000
MAX_SEARCH = 400000000000000

total = 0

for index in range(len(paths)):
    for index2 in range(index + 1, len(paths)):
        intersections = paths[index].intersection(paths[index2])
        if intersections:
            if MIN_SEARCH <= intersections[0].x and MIN_SEARCH <= intersections[0].y and MAX_SEARCH >= intersections[0].x and MAX_SEARCH >= intersections[0].y:
                total += 1

print(total)

tools.stop_clock()

temp = solve(
    [
        a + b * g - stones[0][0][0] - stones[0][1][0] * g,
        c + d * g - stones[0][0][1] - stones[0][1][1] * g,
        e + f * g - stones[0][0][2] - stones[0][1][2] * g,
        a + b * h - stones[1][0][0] - stones[1][1][0] * h,
        c + d * h - stones[1][0][1] - stones[1][1][1] * h,
        e + f * h - stones[1][0][2] - stones[1][1][2] * h,
        a + b * j - stones[2][0][0] - stones[2][1][0] * j,
        c + d * j - stones[2][0][1] - stones[2][1][1] * j,
        e + f * j - stones[2][0][2] - stones[2][1][2] * j,
    ],
    [a, b, c, d, e, f, g, h, j],
    dict=True
)[0]

print(temp[a] + temp[c] + temp[e])

tools.stop_clock()