import unittest

class BasicMemory(unittest.TestCase):
    def test_first_test(self):
        self.assertTrue(True)

def test_memory_suite():
    print("### Starting test_memory_suite")
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BasicMemory))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()

    runner.run(test_memory_suite())
