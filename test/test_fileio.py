import unittest
from unittest import TestCase
from fileio import read_ciphered_text, read_corpus_line_by_line


class TestReadEncodedText(TestCase):
    def setUp(self):
        self.text = read_ciphered_text()

    def test_length_is_correct(self):
        self.assertEquals(len(self.text), 810)

    def test_starts_with_expected_letters(self):
        start = "uml pknz nx njl"
        self.assertTrue(self.text.startswith(start))


class TestReadCorpus(TestCase):
    def setUp(self):
        self.stream = read_corpus_line_by_line()

    def test_content_of_first_three_lines(self):
        line = self.stream.next()
        self.assertTrue(line.endswith('carroll'))
        line = self.stream.next()
        self.assertEquals(line, '')
        expected = 'this ebook is for the use of anyone anywhere at no cost and with'
        line = self.stream.next()
        self.assertEquals(line, expected)


if __name__ == "__main__":
    unittest.main()