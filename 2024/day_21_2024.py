import aoctools
from copy import deepcopy
from functools import cache

tools = aoctools.aoc_tools()

tools.start_clock()
lines = tools.get_array_input("2024/inputs/day_21_2024.txt")

def numerical_conv(x):
    if x == "A":
        return (2, 3)
    elif x == "0":
        return (1, 3)
    else:
        return ((int(x) - 1) % 3, 2 - ((int(x) - 1) // 3))

def directional_conv(x):
    match x:
        case "^":
            return (1, 0)
        case "A":
            return (2, 0)
        case "<":
            return (0, 1)
        case "v":
            return (1, 1)
        case ">":
            return (2, 1)

def directional_decode(x):
    match x:
        case (1, 0):
            return "^"
        case (2, 0):
            return "A"
        case (0, 1):
            return "<"
        case (1, 1):
            return "v"
        case (2, 1):
            return ">"

def numerical_decode(x):
    match x:
        case (2, 3):
            return "A"
        case (1, 3):
            return 0
        case _:
            return x[0] - 3 * x[1] + 7

def directional_parse(x):
    output = []
    position = directional_conv("A")
    for char in x:
        match char:
            case "A":
                output.append(directional_decode(position))
            case _:
                position = tools.tup_add(position, tools.dirs[">v<^".index(char)])
    return output

def next_layer(x):
    meta_meta_output = set()
    position = directional_conv("A")
    for line in x:
        meta_output = {""}
        for char in line:
            new_pos = directional_conv(char)
            if new_pos[0] > position[0]:
                x_char = ">"
            else:
                x_char = "<"
            if new_pos[1] > position[1]:
                y_char = "v"
            else:
                y_char = "^"
            horizontal = x_char * abs(new_pos[0] - position[0])
            vertical = y_char * abs(new_pos[1] - position[1])
            new_meta_output = set()
            if position[0] == 0:
                for output in meta_output:
                    new_meta_output.add(output + horizontal + vertical + "A")
            elif new_pos[0] == 0:
                for output in meta_output:
                    new_meta_output.add(output + vertical + horizontal + "A")
            else:
                for output in meta_output:
                    new_meta_output.add(output + horizontal + vertical + "A")
                    new_meta_output.add(output + vertical + horizontal + "A")
            meta_output = new_meta_output
            position = new_pos
        meta_meta_output = meta_meta_output.union(meta_output)
    return meta_meta_output

"""a = {"^^>A"}
b = {">^^A"}
print(a)
print(next_layer(a))
print(next_layer(next_layer(a)))
print(b)
print(next_layer(b))
print(next_layer(next_layer(b)))"""

# quit()

total = 0
for line in lines:
    sub_total = 0
    meta_first = {""}
    position = numerical_conv("A")
    for char in line:
        new_pos = numerical_conv(char)
        if new_pos[0] > position[0]:
            x_char = ">"
        else:
            x_char = "<"
        horizontal = x_char * abs(new_pos[0] - position[0])
        if new_pos[1] > position[1]:
            y_char = "v"
        else:
            y_char = "^"
        vertical = y_char * abs(new_pos[1] - position[1])
        new_meta_first = set()
        if position[1] == 3 and new_pos[0] == 0:
            for first in meta_first:
                new_meta_first.add(first + vertical + horizontal + "A")
        elif new_pos[1] == 3 and position[0] == 0:
            for first in meta_first:
                new_meta_first.add(first + horizontal + vertical + "A")
        else:
            for first in meta_first:
                new_meta_first.add(first + vertical + horizontal + "A")
                new_meta_first.add(first + horizontal + vertical + "A")
        meta_first = new_meta_first
        position = new_pos
    second = next_layer(meta_first)
    third = next_layer(second)
    minimal = 100
    for attempt in third:
        if len(attempt) < minimal:
            minimal = len(attempt)
    total += minimal * int(line[:-1])
        
print(total)

tools.stop_clock()

"""total = 0
for line in lines:
    sub_total = 0
    meta_first = {""}
    position = numerical_conv("A")
    last = 0
    for char in line:
        new_pos = numerical_conv(char)
        if new_pos[0] > position[0]:
            x_char = ">"
        else:
            x_char = "<"
        horizontal = x_char * abs(new_pos[0] - position[0])
        if new_pos[1] > position[1]:
            y_char = "v"
        else:
            y_char = "^"
        vertical = y_char * abs(new_pos[1] - position[1])
        new_meta_first = set()
        if position[1] == 3 and new_pos[0] == 0:
            for first in meta_first:
                new_meta_first.add(first + vertical + horizontal + "A")
        elif new_pos[1] == 3 and position[0] == 0:
            for first in meta_first:
                new_meta_first.add(first + horizontal + vertical + "A")
        else:
            for first in meta_first:
                new_meta_first.add(first + vertical + horizontal + "A")
                new_meta_first.add(first + horizontal + vertical + "A")
        meta_first = new_meta_first
        position = new_pos
        current = meta_first
        for i in range(25):
            next = next_layer(current)
            minimal = 9999999999999
            for attempt in next:
                if len(attempt) < minimal:
                    minimal = len(attempt)
            current = set()
            for attempt in next:
                if len(attempt) < (minimal + 1):
                    current.add(attempt)
            print(i, len(current))
        last += len(current[0])
    total += last * int(line[:-1])
        
print(total)"""

@cache
def how_many(a, b, r):
    if a == b or r == 0:
        return 1
    position = directional_conv(a)
    new_pos = directional_conv(b)
    if new_pos[0] > position[0]:
        x_char = ">"
    else:
        x_char = "<"
    if new_pos[1] > position[1]:
        y_char = "v"
    else:
        y_char = "^"
    if new_pos[1] == position[1]:
        return how_many("A", x_char, r-1) + (abs(new_pos[0] - position[0]) - 1) + how_many(x_char, "A", r-1)
    elif new_pos[0] == position[0]:
        return how_many("A", y_char, r-1) + (abs(new_pos[1] - position[1]) - 1) + how_many(y_char, "A", r-1)
    elif new_pos[0] == 0:
        return how_many("A", y_char, r-1) + (abs(new_pos[1] - position[1]) - 1) + how_many(y_char, x_char, r-1) + (abs(new_pos[0] - position[0]) - 1) + how_many(x_char, "A", r-1)
    elif position[0] == 0:
        return how_many("A", x_char, r-1) + (abs(new_pos[0] - position[0]) - 1) + how_many(x_char, y_char, r-1) + (abs(new_pos[1] - position[1]) - 1) + how_many(y_char, "A", r-1)
    else:
        return min(
            how_many("A", y_char, r-1) + (abs(new_pos[1] - position[1]) - 1) + how_many(y_char, x_char, r-1) + (abs(new_pos[0] - position[0]) - 1) + how_many(x_char, "A", r-1),
            how_many("A", x_char, r-1) + (abs(new_pos[0] - position[0]) - 1) + how_many(x_char, y_char, r-1) + (abs(new_pos[1] - position[1]) - 1) + how_many(y_char, "A", r-1)
        )

total = 0
for line in lines:
    sub_total = 0
    meta_first = {""}
    position = numerical_conv("A")
    for char in line:
        new_pos = numerical_conv(char)
        if new_pos[0] > position[0]:
            x_char = ">"
        else:
            x_char = "<"
        horizontal = x_char * abs(new_pos[0] - position[0])
        if new_pos[1] > position[1]:
            y_char = "v"
        else:
            y_char = "^"
        vertical = y_char * abs(new_pos[1] - position[1])
        new_meta_first = set()
        if position[1] == 3 and new_pos[0] == 0:
            for first in meta_first:
                new_meta_first.add(first + vertical + horizontal + "A")
        elif new_pos[1] == 3 and position[0] == 0:
            for first in meta_first:
                new_meta_first.add(first + horizontal + vertical + "A")
        else:
            for first in meta_first:
                new_meta_first.add(first + vertical + horizontal + "A")
                new_meta_first.add(first + horizontal + vertical + "A")
        meta_first = new_meta_first
        position = new_pos
    minimal = 99999999999999999999999999
    for test in meta_first:
        attempt = "A" + test
        running = 0
        for i in range(len(attempt) - 1):
            running += how_many(attempt[i], attempt[i + 1], 25)
        if running < minimal:
            minimal = running
    total += minimal * int(line[:-1])

print(total)

tools.stop_clock()