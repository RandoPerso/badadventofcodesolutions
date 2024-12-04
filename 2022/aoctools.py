import time
import numpy as np

class aoc_tools():
    def __init__(self):
        self.clock = 0
    
    def get_array_input(self, path):
        f = open(path)
        temp = []
        for line in f:
            temp.append(line.strip())
        f.close()
        return temp
    
    def get_raw_array_input(self, path):
        f = open(path)
        temp = []
        for line in f:
            temp.append(line)
        f.close()
        return temp

    def get_line_input(self, path):
        f = open(path)
        temp = f.read()
        f.close()
        return temp

    def start_clock(self):
        self.clock = time.time()
    
    def stop_clock(self):
        print(f"Your slow code took {time.time() - self.clock} seconds")
    
    def safe_search(self, array, item):
        if item not in array:
            return -1
        else:
            return array.index(item)
    
    def rot_array_cc(self, array):
        return np.rot90(np.array(array), 1).tolist()
    
    def rot_array_cc_n(self, array, n):
        return np.rot90(np.array(array), n).tolist()
