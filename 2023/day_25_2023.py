import aoctools
import networkx

tools = aoctools.aoc_tools()

tools.start_clock()

lines = tools.get_array_input("2023/inputs/day_25_2023.txt")

"""nodes = {}
edges = []

sys.setrecursionlimit(3000)

for line in lines:
    temp = line.split()
    nodes[temp[0][:3]] = set(temp[1:])
    for edge in nodes[temp[0][:3]]:
        edges.append([temp[0][:3], edge])

for edge in edges:
    if edge[1] not in nodes:
        nodes[edge[1]] = set()
    nodes[edge[1]].add(edge[0])"""

"""special = {}

for node in nodes:
    if len(nodes[node]) == 1:
        special.add(node)

for edge in edges:
    if edge[0] in special or edge[1] in special:
        edges.remove(edge)"""

"""def dfs(node, nodes, visited):
    visited.add(node)
    for neighbor in nodes[node]:
        if neighbor not in visited:
            dfs(neighbor, nodes, visited)
    frontier = [node]
    while frontier:
        temp = frontier.pop()
        visited.add(temp)
        for neighbor in nodes[temp]:
            if neighbor not in visited:
                frontier.append(neighbor)"""

"""def count(nodes):
    visited = set()
    counter = 0
    for node in nodes:
        if node not in visited:
            counter += 1
            if counter > 2:
                break
            dfs(node, nodes, visited)
    return counter

running = True

for edge1 in edges:
    for edge2 in edges:
        for edge3 in edges:
            if edge1 == edge2 or edge2 == edge3 or edge1 == edge3:
                continue
            edges_2 = [edge1, edge2, edge3]
            failed = False
            for edge in edges_2:
                if edge[0] in special or edge[1] in special:
                    failed = True
                    break
            if failed:
                continue
            new_nodes = deepcopy(nodes)
            for edge in edges_2:
                temp = list(edge)
                new_nodes[temp[0]].remove(temp[1])
                new_nodes[temp[1]].remove(temp[0])
            if count(new_nodes) == 2:
                visited = set()
                counts = []
                for node in new_nodes:
                    if node not in visited:
                        counts.append(len(visited))
                        dfs(node, new_nodes, visited)
                print(counts[1] * (len(visited) - counts[1]))
                running = False
                break
        if not running:
            break
    if not running:
        break"""

full_graph = networkx.Graph()

for line in lines:
    temp = line.split()
    name = temp[0][:3]
    full_graph.add_edges_from([(name, i) for i in temp[1:]])

temp = networkx.minimum_edge_cut(full_graph)

full_graph.remove_edges_from(temp)

temp2 = list(networkx.connected_components(full_graph))
print(len(temp2[0]) * len(temp2[1]))

"""edges = [i for i in full_graph.edges]
running = True

for i in range(len(edges)):
    for j in range(i + 1, len(edges)):
        for k in range(j + 1, len(edges)):
            new_graph = full_graph.copy()
            new_graph.remove_edges_from([edges[i], edges[j], edges[k]])
            if not networkx.is_connected(new_graph):
                temp = list(networkx.connected_components(new_graph))
                print(len(temp[0]) * len(temp[1]))
                running = False
                break
        if not running:
            break
    if not running:
        break"""

tools.stop_clock()
