import aoctools

tools = aoctools.aoc_tools()

tools.start_clock()

lines = tools.get_array_input("2015/inputs/day_5_2015.txt")

total = 0

for string in lines:
    if sum([string.count(i) for i in "aeiou"]) < 3:
        continue
    if "ab" in string or "cd" in string or "pq" in string or "xy" in string:
        continue
    for index in range(len(string) - 1):
        if string[index] == string[index + 1]:
            total += 1
            break

print(total)

tools.stop_clock()

total = 0

for string in lines:
    truthy = False
    for index in range(len(string) - 3):
        for i in range(index + 2, len(string) - 1):
            if string[index:index+2] == string[i:i+2]:
                truthy = True
                break
        if truthy:
            for j in range(len(string) - 2):
                if string[j] == string[j + 2]:
                    total += 1
                    break
            break

print(total)

tools.stop_clock()
