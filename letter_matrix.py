# some utilities for dealing with a simple matrix which
# is just a dictionary with keys like ('a','y'), for all letter
# pairs, avoids the need for numpy and numpy matrices

from alphabet import alphabet
from collections import Counter


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
    for encrypted_letter in alphabet:
        total = 0.0
        for letter in alphabet:
            pair_key = (encrypted_letter, letter)
            count = pair_count[pair_key]
            total += count
        for letter in alphabet:
            pair_key = (encrypted_letter, letter)
            pair_count[pair_key] /= total


def normalize_cols(pair_count):
    for letter in alphabet:
        total = 0.0
        for encrypted_letter in alphabet:
            pair_key = (encrypted_letter, letter)
            count = pair_count[pair_key]
            total += count
        for encrypted_letter in alphabet:
            pair_key = (encrypted_letter, letter)
            pair_count[pair_key] /= total


def normalize_pair_counts(pair_count, niter=100):
    # use the Sinkhorn-Knopp algorithm to convert
    # the pair_counts into a doubly stochastic matrix
    for iteration in xrange(niter):
        normalize_rows(pair_count)
        normalize_cols(pair_count)
    normalize_rows(pair_count)