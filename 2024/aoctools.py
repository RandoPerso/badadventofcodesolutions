import time
import numpy as np


class aoc_tools():
    def __init__(self):
        self.clock = 0

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

    def stop_clock(self):
        print(f"Your slow code took {time.time() - self.clock} seconds")

    def safe_search(self, array: list, item) -> int:
        try:
            return array.index(item)
        except ValueError:
            return -1

    def rot_array_cc(self, array) -> list:
        return np.rot90(np.array(array), 1).tolist()

    def rot_array_cc_n(self, array, n) -> list:
        return np.rot90(np.array(array), n).tolist()
