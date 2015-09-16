import unittest
from unittest import TestCase
import letter_matrix
from params import alphabet
import random


class TestNormalize(TestCase):
    def setUp(self):
        self.tol = 1e-9
        self.matrix = letter_matrix.make_pair_counter()
        random.seed(45444)
        for letter_row in alphabet:
            for letter_col in alphabet:
                pair_key = (letter_row, letter_col)
                self.matrix[pair_key] = 500.0*random.random()
        letter_matrix.normalize_pair_counts(self.matrix)

    def test_normalize_row(self):
        for letter_row in alphabet:
            total = 0.0
            for letter_col in alphabet:
                pair_key = (letter_row, letter_col)
                total += self.matrix[pair_key]
            self.assertTrue(abs(total-1.0) < self.tol)

    def test_normalize_col(self):
        for letter_col in alphabet:
            total = 0.0
            for letter_row in alphabet:
                pair_key = (letter_row, letter_col)
                total += self.matrix[pair_key]
            self.assertTrue(abs(total-1.0) < self.tol)



if __name__ == "__main__":
    unittest.main()