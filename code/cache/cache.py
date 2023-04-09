from code.cache.constants import *

class CacheBlock():
    def __init__(self, number):
        self.number = number
        self.state = MoesiStates.I
        self.data = 0
        self.mem_address = 0

class Cache():
    def __init__(self):
        self.contents = [CacheBlock(0), CacheBlock(1), CacheBlock(2), CacheBlock(3)]

    def run_substitution_policy(self, subset):
        i = 0
        modified = []
        owned = []
        exclusive = []
        shared = []
        invalid = []
        
        for block in subset:
            if block.state == MoesiStates.M:
                modified.append(i)
            elif block.state == MoesiStates.O:
                owned.append(i)
            elif block.state == MoesiStates.E:
                exclusive.append(i)
            elif block.state == MoesiStates.S:
                shared.append(i)
            elif block.state == MoesiStates.I:
                invalid.append(i)
            i += 1

        if len(invalid) > 0:
            return invalid[0]
        elif len(shared) > 0:
            return shared[0]
        elif len(exclusive) > 0:
            return exclusive[0]
        elif len(modified) > 0:
            return modified[0]
        elif len(owned) > 0:
            return owned[0]

    def find_idx_to_replace(self, operation):
        set_to_replace = operation.address % 2
        set_size = len(self.contents) / 2

        subset_from = int(set_to_replace * set_size)
        subset_to = int((set_to_replace + 1) * set_size)
        subset = self.contents[subset_from : subset_to]
        offset = self.run_substitution_policy(subset)

        idx_to_replace = int(set_to_replace * set_size + offset)

        return idx_to_replace

    def write(self, operation):
        idx_to_replace = self.find_idx_to_replace(operation)
        
        self.contents[idx_to_replace].data = operation.data
        self.contents[idx_to_replace].mem_address = operation.address
        self.contents[idx_to_replace].state = MoesiStates.M

    def read(self, operation):
        found = False

        for block in self.contents:
            if block.mem_address == operation.address:
                found = True
                break

        if found:
            return block.data
        #TODO: If not found, is miss and should fetch it and then replace it in
        # the cache

