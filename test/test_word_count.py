import unittest
from unittest import TestCase
from collections import Counter
from word_count import add_word_count_to_counter, process_word
from word_count import build_word_count_from_corpus


class TestAddWordCountToCounter(TestCase):
    def test_add_to_counter(self):
        counter = Counter()
        add_word_count_to_counter("  he-llo there:,   I said hello\n\n", counter)
        expected_counter = Counter()
        expected_counter['hello'] = 2
        expected_counter['there'] = 1
        expected_counter['i'] = 1
        expected_counter['said'] = 1
        self.assertEquals(counter, expected_counter)


class TestProcessWord(TestCase):
    def test_process_word_simple(self):
        self.assertEqual(process_word("hello"), "hello")

    def test_process_word_hyphen(self):
        self.assertEqual(process_word("hel-lo"), "hello")

    def test_process_word_other_stuff(self):
        for stuff in [';', '"', '.', ' ', '\xe2\x80\x94']:
            self.assertEqual(process_word("hel%slo" % stuff), "hello")

    def test_process_word_caps(self):
        self.assertEqual(process_word("hELLo"), "hello")


class BuildWordCountFromCorpus(TestCase):
    def test_build_word_count_from_corpus_two_lines(self):
        expected = [('of', 1),
                    ('ebook', 1),
                    ('carroll', 1),
                    ('alice', 1),
                    ('project', 1),
                    ('gutenberg', 1),
                    ('lewis', 1),
                    ('in', 1),
                    ('wonderland', 1),
                    ('the', 1),
                    ('by', 1)]
        word_count = build_word_count_from_corpus(lines_max=2)
        most_common = word_count.most_common()
        self.assertEquals(most_common, expected)


if __name__ == "__main__":
    unittest.main()