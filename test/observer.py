import unittest

class BasicPublisher(unittest.TestCase):
    pass

def test_publisher_suite():
    print("### Starting test_publisher_suite")
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BasicPublisher))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()

    runner.run(test_publisher_suite())
