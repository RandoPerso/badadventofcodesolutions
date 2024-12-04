import aoctools
from copy import deepcopy
from queue import PriorityQueue

tools = aoctools.aoc_tools()

tools.start_clock()

lines = [list(i) for i in tools.get_array_input("2023/inputs/day_17_2023.txt")]

def tup_add(tup1, tup2):
   return (tup1[0] + tup2[0], tup1[1] + tup2[1])

def get_neighbors(location):
    things = []
    for ind, i in enumerate([(1, 0), (0, 1), (-1, 0), (0, -1)]):
        temp = tup_add(location, i)
        if temp[0] < 0 or temp[1] < 0 or temp[0] >= len(lines[0]) or temp[1] >= len(lines):
            continue
        temp2 = 1
        if location[2] == ind:
            if location[3] >= 3:
                continue
            else:
                temp2 = location[3] + 1
        things.append((temp + (ind, temp2)))
    return things

def get_cost(location):
    return int(lines[location[1]][location[0]])

def heuristic(goal, next):
    return abs(next[0] - goal[0]) + abs(next[1] - goal[1])

# WOO COPY PASTED!!!
start = (0, 0, -1, -1)

frontier = PriorityQueue()
frontier.put(start, 0)
# came_from = dict()
cost_so_far = dict()
# came_from[start] = None
cost_so_far[start] = 0

goal = (len(lines[0]) - 1, len(lines) - 1)

while not frontier.empty():
    current = frontier.get()

    if current[:2] == goal:
        print(cost_so_far[current])
        continue
   
    for next in get_neighbors(current):
        new_cost = cost_so_far[current] + get_cost(next)
        if next not in cost_so_far or new_cost < cost_so_far[next]:
            cost_so_far[next] = new_cost
            priority = new_cost + heuristic(goal, next)
            frontier.put(next, priority)
            # came_from[next] = current

"""temp = goal
while temp != (0, 0):
    print(temp, cost_so_far[temp])
    temp = came_from[temp]"""

tools.stop_clock()

def get_neighbors2(location):
    things = []
    for ind, i in enumerate([(1, 0), (0, 1), (-1, 0), (0, -1)]):
        temp = tup_add(location, i)
        if temp[0] < 0 or temp[1] < 0 or temp[0] >= len(lines[0]) or temp[1] >= len(lines):
            continue
        temp2 = 1
        if location[2] == ind:
            if location[3] >= 10:
                continue
            else:
                temp2 = location[3] + 1
        elif location[2] != -1 and location[2] % 2 == ind % 2:
            continue
        elif location[2] != -1:
            if location[3] < 4:
                continue
        things.append((temp + (ind, temp2)))
    return things

# WOO COPY PASTED!!!
start = (0, 0, -1, -1)

frontier = PriorityQueue()
frontier.put(start, 0)
came_from = dict()
cost_so_far = dict()
came_from[start] = None
cost_so_far[start] = 0

goal = (len(lines[0]) - 1, len(lines) - 1)

while not frontier.empty():
    current = frontier.get()

    if current[:2] == goal:
        if current[3] < 4:
            continue
        print(cost_so_far[current])
        continue
   
    for next in get_neighbors2(current):
        new_cost = cost_so_far[current] + get_cost(next)
        if next not in cost_so_far or new_cost < cost_so_far[next]:
            cost_so_far[next] = new_cost
            priority = new_cost + heuristic(goal, next)
            frontier.put(next, priority)
            came_from[next] = current

tools.stop_clock()
