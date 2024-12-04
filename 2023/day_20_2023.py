import aoctools
from copy import deepcopy
from sympy.ntheory.modular import crt

tools = aoctools.aoc_tools()

tools.start_clock()

lines = tools.get_array_input("2023/inputs/day_20_2023.txt")

def parse_line(line):
    temp = line.split()
    type = temp[0][0]
    name = temp[0][1:]
    outputs = "".join(temp[2:]).split(",")
    if type == "%":
        return {name: [type, 0, outputs]}
    elif type == "&":
        special_ones.append(name)
        return {name: [type, {}, outputs]}
    else:
        broadcaster.extend(outputs)
        return {}

modules = {}
special_ones = []
broadcaster = []

for line in lines:
    modules.update(parse_line(line))

for module in modules.keys():
    for connected in modules[module][2]:
        if connected in special_ones:
            modules[connected][1][module] = 0

for connected in broadcaster:
    if connected in special_ones:
        modules[connected][1][module] = 0

safe_modules = deepcopy(modules)

signals = []
total = [0, 0]

def send_signal(name, connections, type):
    for i in connections:
        signals.append((name, type, i))
        total[type] += 1

for i in range(1000):
    total[0] += 1
    send_signal("broadcaster", broadcaster, 0)
    while signals:
        next_signal = signals.pop(0)
        name = next_signal[2]
        if name not in modules.keys():
            continue
        if modules[name][0] == "%":
            if next_signal[1] == 0:
                modules[name][1] = (modules[name][1] + 1) % 2
                send_signal(name, modules[name][2], modules[name][1])
        else:
            received = next_signal[0]
            modules[name][1][received] = next_signal[1]
            if 0 not in modules[name][1].values():
                send_signal(name, modules[name][2], 0)
            else:
                send_signal(name, modules[name][2], 1)

print(total[0] * total[1])

tools.stop_clock()

"""modules = safe_modules

def send_signal2(name, connections, type):
    for i in connections:
        signals.append((name, type, i))

signals = []

total = 0
running = True
while running:
    total += 1
    send_signal2("broadcaster", broadcaster, 0)
    while signals:
        next_signal = signals.pop(0)
        name = next_signal[2]
        if name == "rx" and next_signal[1] == 0:
            running = False
            break
        if name not in modules.keys():
            continue
        if modules[name][0] == "%":
            if next_signal[1] == 0:
                modules[name][1] = (modules[name][1] + 1) % 2
                send_signal2(name, modules[name][2], modules[name][1])
        else:
            received = next_signal[0]
            modules[name][1][received] = next_signal[1]
            if 0 not in modules[name][1].values():
                send_signal2(name, modules[name][2], 0)
            else:
                send_signal2(name, modules[name][2], 1)

print(total)"""

modules = safe_modules

def send_signal2(name, connections, type):
    for i in connections:
        signals.append((name, type, i))

rx_connector = "gf"
very_special = {}
time_at = {}

for module in modules:
    if rx_connector in modules[module][2]:
        very_special[module] = 0
        time_at[module] = 0

signals = []

total = 0
running = True
while running:
    total += 1
    send_signal2("broadcaster", broadcaster, 0)
    while signals:
        next_signal = signals.pop(0)
        name = next_signal[2]
        if name not in modules.keys():
            continue
        if modules[name][0] == "%":
            if next_signal[1] == 0:
                modules[name][1] = (modules[name][1] + 1) % 2
                send_signal2(name, modules[name][2], modules[name][1])
        else:
            received = next_signal[0]
            modules[name][1][received] = next_signal[1]
            if 0 not in modules[name][1].values():
                send_signal2(name, modules[name][2], 0)
            else:
                if name in very_special.keys():
                    very_special[name] = total - time_at[name]
                    time_at[name] = total
                send_signal2(name, modules[name][2], 1)
    if total % 10000 == 0:
        break

required = crt(list(very_special.values()), [very_special[k] - (total % very_special[k]) for k in time_at.keys()])

print(total + required[0])

tools.stop_clock()