import aoctools
from copy import deepcopy
from functools import cache
import random

tools = aoctools.aoc_tools()

tools.start_clock()
lines = tools.get_array_input("2023/inputs/day_25_2023.txt")

connections: dict[str, set] = {}
for line in lines:
    components = line.split()
    if components[0][:-1] in connections:
        connections[components[0][:-1]].update(components[1:])
    else:
        connections[components[0][:-1]] = set(components[1:])
    for component in components[1:]:
        if component in connections:
            connections[component].add(components[0][:-1])
        else:
            connections[component] = {components[0][:-1]}

all_components = list(connections.keys())
usage_count = {}
failed = True
while failed:
    for i in range(10):
        start = random.choice(all_components)
        end = random.choice(all_components)
        while start == end:
            end = random.choice(all_components)
        frontier = {start}
        visited = set()
        came_from = {}
        searching = True
        while searching:
            new_frontier = set()
            visited.update(frontier)
            for location in frontier:
                for new in connections[location]:
                    if new in visited:
                        continue
                    if new == end:
                        searching = False
                    new_frontier.add(new)
                    came_from[new] = location
            frontier = new_frontier
        pointer = end
        while pointer != start:
            if frozenset({pointer, came_from[pointer]}) in usage_count:
                usage_count[frozenset({pointer, came_from[pointer]})] += 1
            else:
                usage_count[frozenset({pointer, came_from[pointer]})] = 1
            pointer = came_from[pointer]
    start = random.choice(all_components)
    frontier = {start}
    visited = set()
    most_used = sorted(usage_count, key=usage_count.get, reverse=True)[:3]
    while frontier:
        new_frontier = set()
        visited.update(frontier)
        for location in frontier:
            for new in connections[location]:
                if frozenset({new, location}) in most_used:
                    continue
                if new in visited:
                    continue
                new_frontier.add(new)
        frontier = new_frontier
    if len(visited) != len(all_components):
        failed = False
        print(len(visited) * (len(all_components) - len(visited)))

tools.stop_clock()