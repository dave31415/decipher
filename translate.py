from params import alphabet, unknown_letter


class Translator(dict):
    """
    a class that acts like a dictionary for holding letter to letter
    translations but has a 'call' method (i.e. round parens) which
    makes a more refined translation that converts known letters,
    converts others not in dictionary but in the alphabet to
    the 'unknown_letter' and returns every other character
    (e.g. punctuation) unchanged. 'call' can also be called on a
    string and it
    will convert each letter of string
    :return: Translator object
    """

    def __call__(self, key):
        assert isinstance(key, str)
        if len(key) > 1:
            # recursive call on each letter
            return ''.join([self.__call__(letter) for letter in key])
        if key in self:
            return self[key]

        if key in alphabet:
            # in alphabet but no translation yet
            # return 'unknown_letter'
            return unknown_letter

        # not in alphabet, leave as is
        return key

    def clone(self):
        # return a copy (without sharing references)
        trans = Translator()
        for key, value in self.iteritems():
            trans[key] = value
        return trans


def true_translation_dictionary():
    # correct translation, for debugging, testing etc
    translation_dict = {
        'a': 'c',
        'b': 'u',
        'c': 'a',
        'd': unknown_letter,
        'e': 'x',
        'f': 'm',
        'g': 'b',
        'h': 'i',
        'i': 'p',
        'j': 'n',
        'k': 'l',
        'l': 'e',
        'm': 'h',
        'n': 'o',
        'o': 'k',
        'p': 'g',
        'q': unknown_letter,
        'r': 's',
        's': 'd',
        't': unknown_letter,
        'u': 't',
        'v': 'v',
        'w': 'r',
        'x': 'f',
        'y': 'y',
        'z': 'w'
    }

    return translation_dict
