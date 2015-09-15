# some utilities for dealing with a simple matrix which
# is just a dictionary with keys like ('a','y'), for all letter
# pairs, avoids the need for numpy and numpy matrices

#TODO: add tests, docstrings for these

from alphabet import alphabet
from collections import Counter
from logger import logger


def make_pair_counter():
    #make a counter, but initialize with a very small number
    epsilon = 1e-2
    pair_count = Counter()
    for encrypted_letter in alphabet:
        for letter in alphabet:
            pair_key = (encrypted_letter, letter)
            pair_count[pair_key] = epsilon
    return pair_count


def normalize_rows(pair_count):
    max_margin_error = 0.0
    for encrypted_letter in alphabet:
        total = 0.0
        for letter in alphabet:
            pair_key = (encrypted_letter, letter)
            count = pair_count[pair_key]
            total += count
        margin_error = abs(total-1.0)
        max_margin_error = max(max_margin_error, margin_error)
        for letter in alphabet:
            pair_key = (encrypted_letter, letter)
            pair_count[pair_key] /= total
    logger.debug("Max row margin error: %s" % max_margin_error)


def normalize_cols(pair_count):
    max_margin_error = 0.0
    for letter in alphabet:
        total = 0.0
        for encrypted_letter in alphabet:
            pair_key = (encrypted_letter, letter)
            count = pair_count[pair_key]
            total += count
        margin_error = abs(total-1.0)
        max_margin_error = max(max_margin_error, margin_error)
        for encrypted_letter in alphabet:
            pair_key = (encrypted_letter, letter)
            pair_count[pair_key] /= total
    logger.debug("Max row margin error: %s" % max_margin_error)


def normalize_pair_counts(pair_count, niter=100):
    # use the Sinkhorn-Knopp algorithm to convert
    # the pair_counts into a doubly stochastic matrix
    for iteration in xrange(niter):
        logger.debug("normalize iteration: %s" % iteration)
        normalize_rows(pair_count)
        normalize_cols(pair_count)
    normalize_rows(pair_count)