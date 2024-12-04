import aoctools
import math

tools = aoctools.aoc_tools()

tools.start_clock()

wind = tools.get_line_input("2022/inputs/day_17_2022.txt").strip()

max_height = 0

blocks = (((0, 0), (1, 0), (2, 0), (3, 0)), ((1, 2), (0, 1), (2, 1), (1, 0)), ((0, 0), (1, 0), (2, 2), (2, 0), (2, 1)), ((0, 0), (0, 1), (0, 2), (0, 3)), ((0, 1), (1, 1), (0, 0), (1, 0)))
blockize = (3, 2, 2, 0, 1)

ram_explosion = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)]

blockdex = 0
windex = 0
skipped = 0
notes = []
iter = 0
while iter < 6900 + 1600:
    if iter % 1725 == 0:
        print((max_height, iter, windex))
    offset = [2, 4 + max_height]
    falling = True
    while falling:
        offset[0] += [-1, 1][["<", ">"].index(wind[windex])]
        if offset[0] < 0:
            offset[0] += 1
        if offset[0] + blockize[blockdex] > 6:
            offset[0] -= 1
        for point in blocks[blockdex]:
            if (point[0] + offset[0], point[1] + offset[1]) in ram_explosion:
                offset[0] -= [-1, 1][["<", ">"].index(wind[windex])]
                break
        windex = (windex + 1) % len(wind)
        offset[1] -= 1
        for point in blocks[blockdex]:
            if (point[0] + offset[0], point[1] + offset[1]) in ram_explosion:
                for toint in blocks[blockdex]:
                    if toint[1] + offset[1] + 1 > max_height:
                        max_height = toint[1] + offset[1] + 1
                    ram_explosion.append((toint[0] + offset[0], toint[1] + offset[1] + 1))
                falling = False
                break
    blockdex = (blockdex + 1) % 5
    iter += 1

print(max_height + (579_710_140 * 2734))
tools.stop_clock()