import unittest
from unittest import TestCase
from collections import Counter
from word_count import add_word_count_to_counter


class TestAddWordCountToCounter(TestCase):
    def test_add_to_counter(self):
        counter = Counter()
        add_word_count_to_counter("  hello there,   I said hello\n\n", counter)
        expected_counter = Counter()
        expected_counter['hello'] = 2
        expected_counter['there,'] = 1
        expected_counter['I'] = 1
        expected_counter['said'] = 1
        self.assertEquals(counter, expected_counter)


if __name__ == "__main__":
    unittest.main()