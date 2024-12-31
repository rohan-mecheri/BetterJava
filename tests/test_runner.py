"""
test_runner.py - Runs all tests for BetterJava (unit and integration).
"""

import unittest

def run_all_tests():
    loader = unittest.TestLoader()
    suite = loader.discover("tests")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if not result.wasSuccessful():
        exit(1)
    exit(0)

if __name__ == "__main__":
    run_all_tests()