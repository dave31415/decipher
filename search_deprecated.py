import math
from collections import defaultdict
from params import alphabet
from analyze import true_translation_dictionary


def update_log_prob(ciphered_word, translate, word_data, log_prob):
    epsilon = 0.05
    deciphered_word = translate(ciphered_word)
    possible_words = word_data['fragment_lookup'][deciphered_word]
    for possible_word in possible_words:
        for ciphered_letter, possible_letter in zip(ciphered_word, possible_word):
            pair_key = (ciphered_letter, possible_letter)
            counts = word_data['word_count'][possible_word]
            log_prob[pair_key] += math.sqrt(epsilon + counts)


def get_log_prob(translate, input_data, word_data):
    log_prob = defaultdict(float)
    for ciphered_word in input_data['ciphered_words']:
        update_log_prob(ciphered_word, translate, word_data, log_prob)
    return log_prob


def get_maximum_likelihood(log_prob, input_data):
    true_translation = true_translation_dictionary()
    max_like = {}
    for ciphered_letter in alphabet:
        log_like_max = -1e12
        for deciphered_letter in alphabet:
            pair_key = (ciphered_letter, deciphered_letter)
            log_like = log_prob[pair_key]
            if log_like > log_like_max:
                log_like_max = log_like
                occurrence = input_data['ciphered_text'].count(ciphered_letter)
                correct = true_translation[ciphered_letter] == deciphered_letter
                max_like[ciphered_letter] = (deciphered_letter, log_like, occurrence, correct)
    return max_like











