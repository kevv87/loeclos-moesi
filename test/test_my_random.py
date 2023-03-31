import unittest
import math
from code.my_random import poisson_random_numbers

class MyRandom(unittest.TestCase):
    def test_random_numbers_stay_within_limits(self):
        print("###test_random_numbers_stay_within_limits")
        min_number = 1
        max_number = 3
        random_numbers = poisson_random_numbers(1000, 2, min_number=1, max_number=3)
        for x in random_numbers:
            self.assertTrue(min_number <= x <= max_number)

    def test_generated_random_numbers_follow_poisson_distribution(self):
        print("###test_poisson_distribution")
        lambd = 2
        n = 100000
        random_numbers = poisson_random_numbers(n, lambd, min_number=1, max_number=3)
        counts = [0, 0, 0]
        for x in random_numbers:
            counts[x-1] += 1
        expected_counts = [math.floor(lambd), math.floor(lambd), math.ceil(lambd)]
        for i in range(3):
            self.assertAlmostEqual(counts[i]/n, expected_counts[i]/sum(expected_counts), delta=0.1)

def test_random_suite():
    print("### Starting test_random_suite")
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(MyRandom))
    return suite
