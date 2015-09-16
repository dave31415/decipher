from word_count import build_word_count_from_corpus, word_list_to_fragment_lookup
from params import parameters
from fileio import read_ciphered_text
from word_count import process_word


def get_word_data():
    word_count = build_word_count_from_corpus()
    frequency_min = parameters['min_frequency_word_to_fragment']
    word_count_smaller = {word: count for word, count in word_count.iteritems()
                          if count >= frequency_min}
    fragment_lookup = word_list_to_fragment_lookup(word_count_smaller.keys())
    word_data = {'word_count': word_count, 'fragment_lookup': fragment_lookup}
    return word_data


def get_input_data():
    ciphered_text = read_ciphered_text()
    ciphered_words = [process_word(word) for word in ciphered_text.split()]

    input_data = {'ciphered_text': ciphered_text, 'ciphered_words': ciphered_words}

    return input_data
