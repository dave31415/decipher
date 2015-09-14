from readers import read_corpus_line_by_line
from collections import Counter


def add_word_count_to_counter(string, counter):
    """
    :param string: any string
    :param counter: an existing Counter object to be added to
    :return:
    """

    for word in string.split():
        counter[word] += 1


def build_word_count_from_corpus(lines_max=100000000):
    word_counter = Counter()
    for line_num, line in enumerate(read_corpus_line_by_line()):
        add_words_count_to_counter(line, word_counter)
        if line_num > lines_max:
            return word_counter




