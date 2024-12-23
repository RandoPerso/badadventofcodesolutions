import aoctools
from copy import deepcopy
from functools import cache
import networkx

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

new_connections = networkx.Graph()

new_connections.add_nodes_from(connections)
for computer in connections:
    new_connections.add_edges_from([(computer, i) for i in connections[computer]])

maximal = 0
maximal_computers = []
cliques = networkx.node_clique_number(new_connections)
for computer in cliques:
    if cliques[computer] > maximal:
        maximal = cliques[computer]
        maximal_computers = [computer]
    elif cliques[computer] == maximal:
        maximal_computers.append(computer)

maximal_computers.sort()
print(",".join(maximal_computers))

tools.stop_clock()