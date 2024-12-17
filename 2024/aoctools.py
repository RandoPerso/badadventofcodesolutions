import time
import numpy as np


class aoc_tools():
    def __init__(self):
        self.clock = 0
        self.dirs = ((1, 0), (0, 1), (-1, 0), (0, -1))

    def get_array_input(self, path) -> list[str]:
        with open(path) as f:
            temp = []
            for line in f:
                temp.append(line.strip())
        return temp

    def get_raw_array_input(self, path) -> list[str]:
        with open(path) as f:
            temp = []
            for line in f:
                temp.append(line)
        return temp

    def get_line_input(self, path) -> str:
        with open(path) as f:
            temp = f.read()
        return temp
    
    def get_one_line_input(self, path) -> str:
        with open(path) as f:
            temp = []
            for line in f:
                temp.append(line.strip())
        return "".join(temp)

    def start_clock(self):
        self.clock = time.time()
    
    def start_clock_ns(self):
        self.clock = time.perf_counter_ns()

    def stop_clock(self):
        print(f"Your slow code took {time.time() - self.clock} seconds")
    
    def stop_clock_ns(self):
        print(f"Your slow code took {time.perf_counter_ns() - self.clock} nanoseconds")

    def safe_search(self, array: list, item) -> int:
        try:
            return array.index(item)
        except ValueError:
            return -1

    def rot_array_cc(self, array) -> list:
        return np.rot90(np.array(array), 1).tolist()

    def rot_array_cc_n(self, array, n) -> list:
        return np.rot90(np.array(array), n).tolist()
    
    def in_bounds(self, pos, max_x, max_y) -> bool:
        if pos[1] >= max_y or pos[1] < 0:
            return False
        if pos[0] >= max_x or pos[0] < 0:
            return False
        return True
    
    def tup_add(self, x, y) -> tuple:
        return tuple(x[i] + y[i] for i in range(len(x)))
