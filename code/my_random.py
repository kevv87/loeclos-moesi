import math
import random

def poisson_random_numbers(n, lambd=2, min_number=1, max_number=3):
    """
    Generates n random numbers following the Poisson distribution with parameter lambd.
    """
    result = []
    for i in range(n):
        found = False
        while not found:
            L = math.exp(-lambd)
            k = 0
            p = 1
            while p >= L:
                k = k + 1
                u = random.uniform(0, 1)
                p = p * u
            x = k - 1
            if min_number <= x <= max_number:
                result.append(k - 1)
                found = True
    return result
