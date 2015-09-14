from readers import read_corpus_line_by_line
from collections import Counter
import re
from itertools import combinations
from alphabet import unknown_letter

regex_expression = re.compile('[^a-z]')


def add_word_count_to_counter(string, counter):
    """
    :param string: any string
    :param counter: an existing Counter object to be added to
    :return:
    """

    for word in string.split():
        add_word = process_word(word)
        if add_word:
            counter[add_word] += 1


def process_word(word):
    """
    :param word: string
    :return: string lower case with non-alphabetical letters removed
    """
    #remove non-alphabetical characters
    result = regex_expression.sub('', word.lower())
    return result


def build_word_count_from_corpus(lines_max=None):
    """
    :param lines_max: maximum lines to consider, default is all
    :return: Counter object with count of all processed words
    """
    word_counter = Counter()
    for line_num, line in enumerate(read_corpus_line_by_line()):
        if line_num >= lines_max:
            return word_counter
        add_word_count_to_counter(line, word_counter)
    return word_counter


def word_to_list_of_all_fragments(word):
    """
    :param word: string
    :return: list of all strings with any number of letters of input
             string replaced with the unknown letter symbol
    """
    word_as_list = list(word)
    fragment_list = []
    n_letters = len(word)
    for n in xrange(n_letters):
        for combo in combinations(range(n_letters), n+1):
            word_as_list_copy = [w for w in word_as_list]
            for num in combo:
                word_as_list_copy[num] = unknown_letter
            obscured_word = ''.join(word_as_list_copy)
            fragment_list.append(obscured_word)
    return fragment_list
