# some utilities for dealing with a simple matrix defined as
# a dictionary with keys like ('a','y'), for all letter pairs
# avoids the need for numpy dependency


from params import alphabet, parameters
from collections import Counter
from logger import logger


def make_pair_counter():
    """
    :return: a counter object populated with small default value
             for each letter
    """
    epsilon = parameters['pair_counter_epsilon']
    pair_count = Counter()
    for encrypted_letter in alphabet:
        for letter in alphabet:
            pair_key = (encrypted_letter, letter)
            pair_count[pair_key] = epsilon
    return pair_count


def normalize_rows(pair_count):
    """
    :param pair_count: a pair count object, a Counter with tuples for keys
           like ('a','b') for each pair of letters
    :return: normalized along the row direction
    """
    max_margin_error = 0.0
    for encrypted_letter in alphabet:
        total = 0.0
        for letter in alphabet:
            pair_key = (encrypted_letter, letter)
            count = pair_count[pair_key]
            total += count
        margin_error = abs(total - 1.0)
        max_margin_error = max(max_margin_error, margin_error)
        for letter in alphabet:
            pair_key = (encrypted_letter, letter)
            pair_count[pair_key] /= total
    logger.debug("Max row margin error: %s" % max_margin_error)


def normalize_cols(pair_count):
    """
    :param pair_count: a pair count object, a Counter with tuples for keys
           like ('a','b') for each pair of letters
    :return: normalized along the col direction
    """
    max_margin_error = 0.0
    for letter in alphabet:
        total = 0.0
        for encrypted_letter in alphabet:
            pair_key = (encrypted_letter, letter)
            count = pair_count[pair_key]
            total += count
        margin_error = abs(total - 1.0)
        max_margin_error = max(max_margin_error, margin_error)
        for encrypted_letter in alphabet:
            pair_key = (encrypted_letter, letter)
            pair_count[pair_key] /= total
    logger.debug("Max row margin error: %s" % max_margin_error)


def normalize_pair_counts(pair_count):
    """
    use the Sinkhorn-Knopp algorithm to convert
    the pair_counts into a doubly stochastic matrix
    :param pair_count: a pair count object, a Counter with tuples for keys
           like ('a','b') for each pair of letters
    :return: normalized along both the row,col direction
    """
    niter = parameters['normalization_iterations']
    for iteration in xrange(niter):
        logger.debug("normalize iteration: %s" % iteration)
        normalize_rows(pair_count)
        normalize_cols(pair_count)
    normalize_rows(pair_count)
