import unittest
from test.test_processors import test_processors_suite

class TestLib(unittest.TestCase):
    def test_lib_should_work(self):
        self.assertTrue(True)

def test_lib_suite():
    print("### Starting test_lib_suite")
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestLib))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()

    runner.run(test_lib_suite())
    runner.run(test_processors_suite())
