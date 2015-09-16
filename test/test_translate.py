import unittest
from unittest import TestCase
from translate import Translator

from params import unknown_letter


class TestTranslator(TestCase):
    def setUp(self):
        self.trans = Translator()
        self.trans['a'] = 'x'
        self.trans['b'] = 'y'
        self.trans['c'] = 'z'

    def test_translate_known(self):
        self.assertEquals(self.trans('a'), 'x')
        self.assertEquals(self.trans['c'], 'z')
        self.assertEquals(self.trans['a'], 'x')

    def test_translate_unknown_but_in_alphabet(self):
        self.assertEquals(self.trans('h'), unknown_letter)

    def test_translate_unknown_but_not_in_alphabet(self):
        self.assertEquals(self.trans('G'), 'G')
        self.assertEquals(self.trans('$'), '$')

    def test_translate_full_string(self):
        self.assertEquals(self.trans('aG$zb_7k'), 'xG$_y_7_')

    def test_clone(self):
        cloned = self.trans.clone()
        self.trans['a'] = 'g'
        self.assertEquals(cloned('a'), 'x')

if __name__ == "__main__":
    unittest.main()