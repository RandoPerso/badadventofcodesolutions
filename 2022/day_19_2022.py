import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()

bad_blue = tools.get_array_input("2022/inputs/day_19_2022.txt")
blueprints = []

def arr_add(x, y):
    for i in range(len(y)):
        x[i] += y[i]
    return x

def arr_sub(x, y):
    for i in range(len(y)):
        x[i] -= y[i]
    return x

def arr_min(x, y):
    for i in range(len(y)):
        if y[i] > x[i]:
            return False
    return True

def purchaseable(items, blueprints):
    temp = [False, False, False, False]
    for i in range(4):
        if arr_min(items, blueprints[i]):
            temp[i] = True
    return temp

for blueprint in bad_blue:
    temp = blueprint.split()
    blueprints.append([(int(temp[6]), 0, 0), (int(temp[12]), 0, 0), (int(temp[18]), int(temp[21]), 0), (int(temp[27]), 0, int(temp[30]))])
    blueprints[-1].append((max(int(temp[6]), int(temp[12]), int(temp[18]), int(temp[27])), int(temp[21]), int(temp[30]), -1))

"""total = 0

for index, blueprint in enumerate(blueprints):
    states = {"": [[1, 0, 0, 0], [0, 0, 0, 0], [False, False, False, False]]}
    for i in range(24):
        old_states = deepcopy(states)
        states = {}
        for state in old_states:
            for option in [-1, 0, 1, 2, 3]:
                if option == -1:
                    temp4 = purchaseable(old_states[state][1], blueprint)
                    if sum(temp4) == 4:
                        continue
                    states.update({state + " ": [old_states[state][0].copy(), arr_add(old_states[state][1].copy(), old_states[state][0]), temp4]})
                else:
                    if old_states[state][0][option] == blueprint[-1][option]:
                        continue
                    if old_states[state][2][option]:
                        continue
                    temp = arr_sub(old_states[state][1].copy(), blueprint[option])
                    if min(temp) >= 0:
                        temp2 = old_states[state][0].copy()
                        temp2[option] += 1
                        states.update({state + str(option): [temp2, arr_add(temp, old_states[state][0]), [False, False, False, False]]})
    geo_max = 0
    for i in states:
        if states[i][1][3] > geo_max:
            geo_max = states[i][1][3]
    total += (index + 1) * geo_max

print(total)
tools.stop_clock()"""

def predict(initial, current):
    temp = 0
    for i in range(32 - current):
        temp += initial
        initial += 1
    return temp

total = 1

for index, blueprint in enumerate(blueprints[:3]):
    states = {"": [[1, 0, 0, 0], [0, 0, 0, 0], [False, False, False, False]]}
    geo_max = 0
    geo_min = 0
    for i in range(32):
        old_states = deepcopy(states)
        states = {}
        for state in old_states:
            if old_states[state][0][0] == blueprint[3][0] and old_states[state][0][2] == blueprint[3][2]:
                if old_states[state][1][3] + predict(old_states[state][0][3], i) > geo_max:
                    geo_max = old_states[state][1][3] + predict(old_states[state][0][3] + 1, i)
                    continue
            if old_states[state][1][3] + predict(old_states[state][0][3] + 1, i) < geo_max:
                continue
            if old_states[state][1][3] + predict(old_states[state][0][3] + 1, i) < geo_min:
                continue
            for option in [-1, 0, 1, 2, 3]:
                if option == -1:
                    temp4 = purchaseable(old_states[state][1], blueprint)
                    if sum(temp4) == 4:
                        continue
                    states.update({state + " ": [old_states[state][0].copy(), arr_add(old_states[state][1].copy(), old_states[state][0]), temp4]})
                    if states[state + " "][1][3] > geo_min:
                        geo_min = states[state + " "][1][3]
                else:
                    if old_states[state][0][option] == blueprint[-1][option]:
                        continue
                    if old_states[state][2][option]:
                        continue
                    temp = arr_sub(old_states[state][1].copy(), blueprint[option])
                    if min(temp) >= 0:
                        temp2 = old_states[state][0].copy()
                        temp2[option] += 1
                        states.update({state + str(option): [temp2, arr_add(temp, old_states[state][0]), [False, False, False, False]]})
        print((i, len(states), geo_max, geo_min))
    for i in states:
        if states[i][1][3] > geo_max:
            geo_max = states[i][1][3]
    total *= geo_max

print(total)
tools.stop_clock()