import aoctools

tools = aoctools.aoc_tools()

tools.start_clock()

lines = tools.get_array_input("2015/inputs/day_6_2015.txt")

for i in range(len(lines)):
    temp = lines[i].split()
    if temp[0] == "turn":
        temp.pop(0)
    temp.pop(2)
    temp[1] = tuple(int(i) for i in temp[1].split(","))
    temp[2] = tuple(int(i) for i in temp[2].split(","))
    lines[i] = temp

enabled = set()

for line in lines:
    if line[0] == "on":
        for i in range(line[1][0], line[2][0] + 1):
            for j in range(line[1][1], line[2][1] + 1):
                enabled.add((i, j))
    elif line[0] == "off":
        for i in range(line[1][0], line[2][0] + 1):
            for j in range(line[1][1], line[2][1] + 1):
                try:
                    enabled.remove((i, j))
                except KeyError:
                    pass
    else:
        for i in range(line[1][0], line[2][0] + 1):
            for j in range(line[1][1], line[2][1] + 1):
                if (i, j) in enabled:
                    enabled.remove((i, j))
                else:
                    enabled.add((i, j))

print(len(enabled))

tools.stop_clock()

lights = {(i, j): 0 for i in range(1000) for j in range(1000)}

for line in lines:
    if line[0] == "on":
        for i in range(line[1][0], line[2][0] + 1):
            for j in range(line[1][1], line[2][1] + 1):
                lights[(i, j)] += 1
    elif line[0] == "off":
        for i in range(line[1][0], line[2][0] + 1):
            for j in range(line[1][1], line[2][1] + 1):
                lights[(i, j)] -= 1
                if lights[(i, j)] < 0:
                    lights[(i, j)] = 0
    else:
        for i in range(line[1][0], line[2][0] + 1):
            for j in range(line[1][1], line[2][1] + 1):
                lights[(i, j)] += 2

print(sum(lights.values()))

tools.stop_clock()
