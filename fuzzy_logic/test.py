import unittest
import random

from FuzzySet import FuzzyVector


class FuzzyVectorTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_vector_creation(self):
        # Test creation works
        try:
            FuzzyVector([1, 0, 0.2, 0.4])
        except Exception:
            self.fail('Unexpected failure creating FIT vector')

        # Test if value is greater than 1 or less than 0 raises ValueError
        self.assertRaises(ValueError, FuzzyVector, ([1.5, 0.9]))
        self.assertRaises(ValueError, FuzzyVector, ([0.5, -0.5]))

    def test_set_operations(self):
        X = FuzzyVector([1 for _ in range(10)])
        O = FuzzyVector([0 for _ in range(10)])

        A = FuzzyVector([0.5, 0.2, 1, 0.4])
        B = FuzzyVector([0.3, 0.15, 0.6, 0])


if __name__ == '__main__':
    unittest.main()
