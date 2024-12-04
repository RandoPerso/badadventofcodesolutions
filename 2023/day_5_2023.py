import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock()

lines = tools.get_array_input("2023/inputs/day_5_2023.txt")

seeds = [int(i) for i in lines[0].split()[1:]]

seed_soil = []
soil_fer = []
fer_wat = []
wat_lig = []
lig_tem = []
tem_hum = []
hum_loc = []

all = [seed_soil, soil_fer, fer_wat, wat_lig, lig_tem, tem_hum, hum_loc]

pointer = 1

for l in all:
    pointer += 2
    while len(lines[pointer].split()) == 3:
        l.append(tuple([int(i) for i in lines[pointer].split()]))
        pointer += 1
    l.sort(key=lambda a: a[1])

for l in all:
    for index, seed in enumerate(seeds):
        for pair in l:
            if seed >= pair[1] and seed < pair[1] + pair[2]:
                diff = seed - pair[1]
                seeds[index] = pair[0] + diff
                break

print(min(seeds))

tools.stop_clock()

old_seeds = [int(i) for i in lines[0].split()[1:]]

new_seeds = []

for i in range(int(len(old_seeds) / 2)):
    new_seeds.append((old_seeds[i * 2], old_seeds[i * 2 + 1]))

def handle_seed(seed_pair, current_index, current_list):
    if current_index == len(current_list):
        new_seeds.append(seed_pair)
        return
    pair = current_list[current_index]
    if seed_pair[0] < pair[1]:
        if seed_pair[0] + seed_pair[1] < pair[1]:
            new_seeds.append(seed_pair)
        else:
            new_seeds.append((seed_pair[0], pair[1] - seed_pair[0]))
            handle_seed((pair[1], seed_pair[1] - (pair[1] - seed_pair[0])), current_index, current_list)
    else:
        if seed_pair[0] > pair[1] + pair[2] - 1:
            handle_seed(seed_pair, current_index + 1, current_list)
        elif seed_pair[0] + seed_pair[1] <= pair[1] + pair[2] - 1:
            new_seeds.append((pair[0] + seed_pair[0] - pair[1], seed_pair[1]))
        else:
            new_seeds.append((pair[0] + seed_pair[0] - pair[1], pair[2] - (seed_pair[0] - pair[1])))
            handle_seed((pair[1] + pair[2], seed_pair[1] - pair[2] + (seed_pair[0] - pair[1])), current_index + 1, current_list)

for l in all:
    seeds = deepcopy(new_seeds)
    new_seeds = []
    for seed_pair in seeds:
        handle_seed(seed_pair, 0, l)

print(min(new_seeds, key=lambda a: a[0])[0])                

tools.stop_clock()
