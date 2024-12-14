import aoctools
from copy import deepcopy
from fractions import Fraction

tools = aoctools.aoc_tools()

tools.start_clock()
lines = tools.get_array_input("2024/inputs/day_14_2024.txt")

"""
HEIGHT = 7
WIDE = 11
"""

HEIGHT = 103
WIDE = 101

MIDDLE_WIDE = int((WIDE - 1) / 2)
MIDDLE_HEIGHT = int((HEIGHT - 1) / 2)

tl = 0
tr = 0
bl = 0
br = 0
for line in lines:
    temp = line.split()
    temp1 = temp[0].split(",")
    position = (int(temp1[0][2:]), int(temp1[1]))
    temp2 = temp[1].split(",")
    velocity = (int(temp2[0][2:]), int(temp2[1]))
    final_location = ((position[0] + velocity[0] * 100) % WIDE, (position[1] + velocity[1] * 100) % HEIGHT)
    if final_location[0] == MIDDLE_WIDE or final_location[1] == MIDDLE_HEIGHT:
        continue
    if final_location[0] < MIDDLE_WIDE:
        if final_location[1] < MIDDLE_HEIGHT:
            tl += 1
        else:
            bl += 1
    else:
        if final_location[1] < MIDDLE_HEIGHT:
            tr += 1
        else:
            br += 1

print(tl * tr * bl * br)

tools.stop_clock()

def tup_add(x, y):
    return ((x[0] + y[0]) % WIDE, (x[1] + y[1]) % HEIGHT)

robots = []
for line in lines:
    temp = line.split()
    temp1 = temp[0].split(",")
    position = (int(temp1[0][2:]), int(temp1[1]))
    temp2 = temp[1].split(",")
    velocity = (int(temp2[0][2:]), int(temp2[1]))
    robots.append([position, velocity])

output = open("2024/inputs/day_14_out.txt", "w")

#original = deepcopy(robots)
# cycle in 10403

counter = 0
for i in range(10404):
    counter += 1
    image = set()
    for index, robot in enumerate(robots):
        robots[index][0] = tup_add(robot[0], robot[1])
        image.add(robots[index][0])
    """
    if robots == original:
        print(counter)
        break
    continue
    """
    # ok so i manually searched through all the states so this was just me suffering while moving through the states thousands by thousands until i realized i can just find the loop length
    if i < 6000:
        continue
    output.write(str(counter) + "\n")
    for y in range(HEIGHT):
        for x in range(WIDE):
            if (x, y) in image:
                output.write("#")
            else:
                output.write(".")
        output.write("\n")

tools.stop_clock()