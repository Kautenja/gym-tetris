"""A script to run the test cases in the package."""
import os
import unittest


if __name__ == '__main__':
    package = os.path.dirname(os.path.abspath(__file__))
    suite = unittest.defaultTestLoader.discover(package)
    unittest.runner.TextTestRunner().run(suite)
