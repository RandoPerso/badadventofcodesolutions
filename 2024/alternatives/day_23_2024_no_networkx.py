import aoctools
from copy import deepcopy
from functools import cache

tools = aoctools.aoc_tools()

tools.start_clock()
lines = tools.get_array_input("2024/inputs/day_23_2024.txt")

connections = {}
for line in lines:
    computers = line.split("-")
    if computers[0] in connections:
        connections[computers[0]].add(computers[1])
    else:
        connections[computers[0]] = {computers[1]}
    if computers[1] in connections:
        connections[computers[1]].add(computers[0])
    else:
        connections[computers[1]] = {computers[0]}

triangles = []
for computer in connections:
    if computer[0] != "t":
        continue
    for partner in connections[computer]:
        mutuals = connections[partner] & connections[computer]
        for mutual in mutuals:
            if {computer, partner, mutual} not in triangles:
                triangles.append({computer, partner, mutual})

print(len(triangles))

tools.stop_clock()

frontier = {(computer,) for computer in connections}
while len(frontier) > 1:
    new_frontier = set()
    for clique in frontier:
        clique_set = set(clique)
        for partner in connections[clique[0]]:
            if partner in clique_set:
                continue
            passing = True
            for computer in clique:
                if partner not in connections[computer]:
                    passing = False
                    break
            if passing:
                new_clique = list(clique) + [partner]
                new_clique.sort()
                new_clique = tuple(new_clique)
                new_frontier.add(new_clique)
    frontier = new_frontier

print(",".join(frontier.pop()))

tools.stop_clock()