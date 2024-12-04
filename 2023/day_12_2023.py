import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()

lines = tools.get_array_input("2023/inputs/day_12_2023.txt")

patterns = []
groups = []

for line in lines:
    patterns.append(list(line.split()[0]))
    groups.append([int(i) for i in line.split()[1].split(",")])

def check(full, partial):
    if len(partial) > len(full):
        return False
    for i in range(len(partial)):
        if partial[i] != full[i]:
            if i == len(partial) - 1 and partial[i] <= full[i]:
                pass
            else:
                return False
    return True

def get_groups(pattern):
    temp = []
    temp2 = 0
    for char in pattern:
        if char == "?":
            if temp2 > 0:
                temp.append(temp2)
                temp2 = 0
            break
        elif char == "." and temp2 != 0:
            temp.append(temp2)
            temp2 = 0
        elif char == "#":
            temp2 += 1
    if temp2 > 0:
        temp.append(temp2)
    return temp

total = 0

# cached_values = []

for i in range(len(patterns)):
    possible = [patterns[i].copy()]
    group = groups[i].copy()
    for j in range(len(possible[0])):
        if len(possible) == 0:
            break
        if possible[0][j] == "?":
            old = deepcopy(possible)
            possible = []
            for k in old:
                k[j] = "."
                if check(group, get_groups(k)):
                    possible.append(k.copy())
                k[j] = "#"
                if check(group, get_groups(k)):
                    possible.append(k.copy())
    for j in range(len(possible) - 1, -1, -1):
        if group != get_groups(possible[j]):
            possible.pop(j)
    total += len(possible)
    # cached_values.append(len(possible))

print(total)

tools.stop_clock()

"""total = 0

for i in range(len(patterns)):
    possible = [((patterns[i].copy() + ["?"]) * 5)[:-1]]
    group = groups[i].copy() * 5
    for j in range(len(possible[0])):
        if len(possible) == 0:
            break
        if possible[0][j] == "?":
            old = deepcopy(possible)
            possible = []
            for k in old:
                k[j] = "."
                if check(group, get_groups(k)):
                    possible.append(k.copy())
                k[j] = "#"
                if check(group, get_groups(k)):
                    possible.append(k.copy())
    for j in range(len(possible) - 1, -1, -1):
        if group != get_groups(possible[j]):
            possible.pop(j)
    total += len(possible)

print(total)"""

def check2(full, partial):
    for i in range(len(partial)):
        if i == len(full):
            if i == len(partial) - 1 and partial[i] == 0:
                return True
            else:
                return False
        if partial[i] != full[i]:
            if i == len(partial) - 1 and partial[i] <= full[i]:
                pass
            else:
                return False
    return True

def get_groups2(pattern):
    temp = get_groups(pattern)
    """if temp == []:
        return []"""
    if pattern[-1] == ".":
        temp += [0]
    """if temp == []:
        temp = [0]"""
    return temp

def combine(partial, remain):
    r_group = get_groups2(remain)
    # print(partial, remain, r_group)
    if partial[-1] == 0:
        temp = partial[:-1] + r_group
    elif remain[0] == ".":
        temp = partial + r_group
    else:
        temp = partial[:-1] + [partial[-1] + r_group[0]] + r_group[1:]
    """if remain[-1] == ".":
        temp += [0]"""
    # print("temp", temp)
    return temp

total = 0

for i in range(len(patterns)):
    possible = {(0,): 1}
    group = groups[i].copy() * 5
    pattern = ((patterns[i].copy() + ["?"]) * 5)[:-1] + ["."]
    last_checked = -1
    for j in range(len(pattern)):
        # print(possible)
        if len(possible) == 0:
            raise Exception("what")
            break
        if pattern[j] == "?":
            #print(possible)
            old = deepcopy(possible)
            possible = {}
            for k in list(old.keys()):
                # print(pattern[last_checked + 1:j])
                if check2(group, combine(list(k), pattern[last_checked + 1:j] + ["."])):
                    temp = tuple(combine(list(k), pattern[last_checked + 1:j] + ["."]))
                    possible.update({temp: possible.get(temp, 0) + old[k]})
                if check2(group, combine(list(k), pattern[last_checked + 1:j] + ["#"])):
                    temp = tuple(combine(list(k), pattern[last_checked + 1:j] + ["#"]))
                    possible.update({temp: possible.get(temp, 0) + old[k]})
            last_checked = j
    old = deepcopy(possible)
    possible = {}
    for k in list(old.keys()):
        # print(pattern[last_checked + 1:j])
        if check2(group, combine(list(k), pattern[last_checked + 1:])):
            temp = tuple(combine(list(k), pattern[last_checked + 1:]))
            possible.update({temp: possible.get(temp, 0) + old[k]})
    # print(possible)
    # print(possible.get(tuple(group + [0]), 0))
    # print(group)
    total += possible.get(tuple(group + [0]), 0)
    #print(possible)
    #print(total)
    #raise Exception("a")

print(total)

tools.stop_clock()
