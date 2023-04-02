import unittest
from test.test_processors import test_processors_suite
from test.test_my_random import test_random_suite
from test.test_memory import test_memory_suite
from test.test_bus import test_bus_suite
from test.test_observer import test_publisher_suite, test_subscriber_suite

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
    runner.run(test_random_suite())
    runner.run(test_memory_suite())
    runner.run(test_bus_suite())
    runner.run(test_subscriber_suite())
    runner.run(test_publisher_suite())
