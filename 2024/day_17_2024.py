import aoctools
from copy import deepcopy

tools = aoctools.aoc_tools()

tools.start_clock_ns()
lines = tools.get_array_input("2024/inputs/day_17_2024_help.txt")

registers = [0, 0, 0]
for index, line in enumerate(lines):
    if index < 3:
        registers[index] = int(line.split()[2])
    if index == 4:
        raw = [int(i) for i in line.split()[1].split(",")]

instructions = []
"""for i in range(len(raw)):
    if i % 2 == 1:
        continue
    instructions.append([raw[i], raw[i + 1]])"""
instructions = raw.copy()

def get_operand(x):
    if x < 4:
        return x
    if x < 7:
        return registers[x - 4]

output = ""
pointer = 0
while pointer < len(instructions):
    instruction = (instructions[pointer], instructions[pointer + 1])
    match instruction[0]:
        case 0:
            registers[0] = registers[0] // (2 ** get_operand(instruction[1]))
        case 1:
            registers[1] = registers[1] ^ instruction[1]
        case 2:
            registers[1] = get_operand(instruction[1]) % 8
        case 3:
            if registers[0] != 0:
                pointer = instruction[1]
                continue
        case 4:
            registers[1] = registers[1] ^ registers[2]
        case 5:
            output += f"{get_operand(instruction[1]) % 8},"
        case 6:
            registers[1] = registers[0] // (2 ** get_operand(instruction[1]))
        case 7:
            registers[2] = registers[0] // (2 ** get_operand(instruction[1]))
    pointer += 2

print(output[:-1])

tools.stop_clock_ns()

"""def get_operand(x, reg):
    if x < 4:
        return x
    if x < 7:
        return reg[x - 4]

def run(x):
    registers = [x, 0, 0]
    output = 0
    pointer = 0
    while pointer < len(instructions):
        instruction = (instructions[pointer], instructions[pointer + 1])
        match instruction[0]:
            case 0:
                registers[0] = registers[0] // (2 ** get_operand(instruction[1], registers))
            case 1:
                registers[1] = registers[1] ^ instruction[1]
            case 2:
                registers[1] = get_operand(instruction[1], registers) % 8
            case 3:
                if registers[0] != 0:
                    pointer = instruction[1]
                    continue
            case 4:
                registers[1] = registers[1] ^ registers[2]
            case 5:
                if output == len(instructions):
                    return False
                if get_operand(instruction[1], registers) % 8 == instructions[output]:
                    output += 1
                else:
                    return False
            case 6:
                registers[1] = registers[0] // (2 ** get_operand(instruction[1], registers))
            case 7:
                registers[2] = registers[0] // (2 ** get_operand(instruction[1], registers))
        pointer += 2
    if output != len(instructions):
        return False
    return True"""

"""index = 1
while True:
    if run(index):
        print(index)
        break
    index += 1"""

"""index = 1
passing = False
while not passing:
    a = index
    pointer = 0
    while True:
        if pointer == len(instructions):
            if a == 0:
                passing = True
            break
        if (((a & 7) ^ 5 ^ (a >> (a & 7 ^ 1)))) & 7 != instructions[pointer]:
            break
        a = a >> 3
        pointer += 1
    index += 1
print(index)"""

correct = {0}

for index in range(15, -1, -1):
    correct = {i << 3 for i in correct}
    new_correct = set()
    success = False
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for h in correct:
                    testing = h | int(f"{i}{j}{k}", 2)
                    # the boolean expression below is specific to my input.
                    # good luck with your input if are using this to solve aoc problems!
                    if (testing & 7 ^ 5 ^ (testing >> (testing & 7 ^ 1))) & 7 == instructions[index]:
                        success = True
                        new_correct.add(testing)
    if not success:
        print("oh no")
    correct = new_correct

print(min(correct))

tools.stop_clock_ns()