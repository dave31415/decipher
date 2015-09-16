# tools for analyzing current solution
from params import alphabet, unknown_letter
from logger import logger
from fileio import read_ciphered_text


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


def show_translation(translate):
    true_translation = true_translation_dictionary()
    for ciphered_letter in alphabet:
        solution = translate(ciphered_letter)
        truth = true_translation[ciphered_letter]
        if (solution == truth):
            correct = "True"
        else:
            correct = " -False-"

        logger.debug("Solution: %s -> %s,  Truth: %s -> %s   %s" %
                     (ciphered_letter, solution, ciphered_letter,
                      truth, correct))


def show_deciphered_text(translate):
    divider = "\n%s\n" % ("=" * 60)
    text = read_ciphered_text()
    deciphered_text = translate(text)
    logger.debug("%s\tDeciphered text%s" % (divider, divider))
    logger.debug("\n\n%s%s" % (deciphered_text, divider))
