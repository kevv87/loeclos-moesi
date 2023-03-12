import unittest
import code.processors as processors

class SimpleTest(unittest.TestCase):
    def test_lib_works(self):
        self.assertTrue(True)

    def test_processors_file_exists(self):
        self.assertTrue(processors)

if __name__ == "__main__":
    unittest.main()
