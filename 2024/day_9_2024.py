import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()
line = tools.get_line_input("2024/inputs/day_9_2024.txt")

data = []

is_data = True
id = 0
for char in line:
    data.extend([id if is_data else -1] * int(char))
    if is_data:
        id += 1
    is_data = not is_data

while data[-1] == -1:
    data.pop()

cursor = 0
while -1 in data:
    if cursor >= len(data):
        break
    if data[cursor] == -1:
        data[cursor] = data.pop()
        while data[-1] == -1:
            data.pop()
    cursor += 1

print(sum(ind * i for ind, i in enumerate(data)))

tools.stop_clock()

smart_data = []
is_data = True
id = 0
for char in line:
    if char != "0":
        smart_data.append((id if is_data else -1, int(char)))
    if is_data: id += 1
    is_data = not is_data

looking = len(smart_data) - 1
while looking >= 0:
    for cursor in range(looking):
        if smart_data[cursor][0] == -1 and smart_data[cursor][1] >= smart_data[looking][1]:
            size_diff = smart_data[cursor][1] - smart_data[looking][1]
            smart_data[cursor] = (smart_data[looking][0], smart_data[looking][1])
            smart_data[looking] = (-1, smart_data[looking][1])
            if size_diff != 0:
                smart_data.insert(cursor + 1, (-1, size_diff))
                looking += 1
            break
    looking -= 1
    while smart_data[looking][0] == -1:
        looking -= 1
total = 0
index = 0
for thing in smart_data:
    if thing[0] != -1:
        total += sum((i * thing[0] for i in range(index, index + thing[1])))
    index += thing[1]

print(total)

tools.stop_clock()