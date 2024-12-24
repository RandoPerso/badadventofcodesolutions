import aoctools
from copy import deepcopy
from functools import cache
from itertools import permutations

tools = aoctools.aoc_tools()

tools.start_clock()
lines = tools.get_array_input("2024/inputs/day_24_2024.txt")

setup = True
wires = {}
gates = {}
for line in lines:
    if setup:
        if line == "":
            setup = False
            continue
        temp = line.split()
        wires[temp[0][:-1]] = int(temp[1])
    else:
        temp = line.split()
        gates[temp[4]] = (temp[0], temp[1], temp[2])

initial_gates = gates.copy()
initial_wires = wires.copy()

while gates:
    removal = set()
    for gate in gates:
        if gates[gate][0] in wires and gates[gate][2] in wires:
            a = wires[gates[gate][0]]
            b = wires[gates[gate][2]]
            match gates[gate][1]:
                case "OR":
                    wires[gate] = a or b
                case "AND":
                    wires[gate] = a and b
                case "XOR":
                    wires[gate] = a ^ b
            removal.add(gate)
    for gate in removal:
        gates.pop(gate)

total = 0
for wire in wires:
    if wire[0] == "z" and wires[wire] == True:
        total += 2 ** int(wire[1:])

print(total)

tools.stop_clock()

"""all_wires = list(initial_gates.keys())

def run(wires: dict, gates: dict, swaps: list):
    while gates:
        removal = set()
        for gate in gates:
            if gates[gate][0] in wires and gates[gate][2] in wires:
                a = wires[gates[gate][0]]
                b = wires[gates[gate][2]]
                match gates[gate][1]:
                    case "OR":
                        output = a or b
                    case "AND":
                        output = a and b
                    case "XOR":
                        output = a ^ b
                if gate in swaps:
                    if swaps.index(gate) % 2 == 0:
                        wires[swaps[swaps.index(gate) + 1]] = output
                    else:
                        wires[swaps[swaps.index(gate) - 1]] = output
                else:
                    wires[gate] = output
                removal.add(gate)
        for gate in removal:
            gates.pop(gate)
    total = 0
    for wire in wires:
        if wire[0] == "z" and wires[wire] == True:
            total += 2 ** int(wire[1:])
    return total

actual_sum = 0
for wire in initial_wires:
    if wires[wire] == True:
        actual_sum += 2 ** int(wire[1:])

for swaps in permutations(all_wires, 8):
    if run(initial_wires.copy(), initial_gates.copy(), swaps) == actual_sum:
        new = swaps.copy()
        new.sort()
        print(",".join(new))"""

for gate in initial_gates:
    initial_gates[gate] = set(initial_gates[gate])

list_gates = list(initial_gates.keys())
list_values = list(initial_gates.values())

def get_gate(gate):
    return list_gates[list_values.index(gate)]

# WARNING: this implementation is scuffed, and you will probably need to do some manual work
# for my input, it only gave me 7 of the 8 incorrect wires.
# i had to trace down the last one.

incorrect = set()
for digit in range(45):
    if digit < 10:
        digit = f"0{digit}"
    else:
        digit = str(digit)
    if digit == "00":
        if initial_gates["z00"] != {"x00", "y00", "XOR"}:
            incorrect.add("z00")
        carry = get_gate({"x00", "y00", "AND"})
    elif digit == "45":
        pass
    else:
        """
        half = get_gate({f"x{digit}", f"y{digit}", "XOR"})
        if initial_gates[f"z{digit}"] != {half, carry, "XOR"}:
            # ok there is an error here. either half is wrong, carry is wrong, or output is wrong
            if {half, carry, "XOR"} in list_values:
                # ok so clearly something is afoot right so
                incorrect.append(f"z{digit}")
            else:
                # ok carry is wrong or output is wrong right
        new_carry = get_gate({f"x{digit}", f"y{digit}", "AND"})"""
        half = get_gate({f"x{digit}", f"y{digit}", "XOR"})
        output_gate: set = initial_gates[f"z{digit}"]
        bad_carry = False
        bad_half = False
        if carry not in output_gate:
            bad_carry = True
        if half not in output_gate:
            bad_half = True
        if (bad_carry and bad_half):
            # i will assume eric is kind and benevolent
            incorrect.add(f"z{digit}")
            incorrect.add(get_gate({half, carry, "XOR"}))
        else:
            if bad_carry:
                incorrect.add(carry)
                carry = (output_gate - {"XOR", half}).pop()
            if bad_half:
                incorrect.add(half)
                half = (output_gate - {"XOR", carry}).pop()
        if {half, carry, "AND"} not in list_values:
            # ok there is a mistake here uh
            raise Exception("bro how could you")
        half_carry = get_gate({half, carry, "AND"})
        other_half_carry = get_gate({f"x{digit}", f"y{digit}", "AND"})
        if {half_carry, other_half_carry, "OR"} not in list_values:
            # ok so half_carry or other_half carry is wrong.
            # i will assume eric is kind and benevolent
            for index, test in enumerate(list_values):
                if half_carry in test:
                    # i will assume eric is kind and benevolent
                    if "OR" in test:
                        carry = list_gates[index]
                        incorrect.add(other_half_carry)
                        break
                if other_half_carry in test:
                    # i will assume eric is kind and benevolent
                    if "OR" in test:
                        carry = list_gates[index]
                        incorrect.add(half_carry)
                        break
        else:
            carry = get_gate({half_carry, other_half_carry, "OR"})

incorrect = list(incorrect)
incorrect.sort()

print("DISCLAIMER: output may be missing gates")
print(",".join(incorrect))

tools.stop_clock()