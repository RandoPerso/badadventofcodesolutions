import aoctools
from copy import deepcopy
from functools import cache

tools = aoctools.aoc_tools()

tools.start_clock()
lines = tools.get_array_input("2024/inputs/day_25_2024.txt")

locks = set()
keys = set()

new = True
is_lock = False
for index, line in enumerate(lines):
    if new:
        if line == "#####":
            is_lock = True
        else:
            is_lock = False
        combo = [-1, -1, -1, -1, -1]
        new = False
        top = index
        continue
    if line == "":
        new = True
        if is_lock:
            locks.add(tuple(combo))
        else:
            keys.add(tuple(combo))
        continue
    searching = "." if is_lock else "#"
    for pos, char in enumerate(line):
        if char == searching and combo[pos] == -1:
            combo[pos] = index - top

if is_lock:
    locks.add(tuple(combo))
else:
    keys.add(tuple(combo))

total = 0
for lock in locks:
    for key in keys:
        works = 1
        for i in range(5):
            if lock[i] > key[i]:
                works = 0
                break
        total += works

print(total)

tools.stop_clock()