import readers
from word_count import build_word_count_from_corpus, word_list_to_fragment_lookup
from word_count import process_word
from alphabet import alphabet, unknown_letter
from collections import Counter


class Translator(dict):
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


def update_paircounts(ciphered_word, translate, word_count, fragment_lookup, pair_counts):
    deciphered_word = translate(ciphered_word)
    if deciphered_word in word_count:
        possible_words = [deciphered_word]
    else:
        possible_words = fragment_lookup[deciphered_word]

    for possible_word in possible_words:
        for ciphered_letter, possible_letter in zip(ciphered_word, possible_word):
            pair_key = (ciphered_letter, possible_letter)
            counts = word_count[possible_word]
            pair_counts[pair_key] += counts


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


def make_pair_counter():
    #make a counter, but initialize with a very small number
    pair_counts = Counter()
    epsilon = 1e-2
    pair_count = Counter()
    for encrypted_letter in alphabet:
        for letter in alphabet:
            pair_key = (encrypted_letter, letter)
            pair_count[pair_key] = epsilon
    return pair_count


def true_translation_dictionary():
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


def declipher_encrypted_file():
    #try to keep memory usage < 1 GB
    quick = False
    cheat = True
    true_translation = true_translation_dictionary()
    if quick:
        print "using 'quick' parameters"
        word_length_max = 3
        frequency_min = 1000
    else:
        word_length_max = 10
        frequency_min = 20

    print 'building word counter'
    word_count = build_word_count_from_corpus()
    print "words in word_count: %s" % len(word_count)
    #compress it a bit
    word_count = {word: count for word, count in word_count.iteritems()
                  if len(word) <= word_length_max and count >= frequency_min}
    print "words in shortened word_count: %s" % len(word_count)
    print "word_length_max: %s, frequency_min: %s" % (word_length_max, frequency_min)
    print 'building fragment lookup'
    fragment_lookup = word_list_to_fragment_lookup(word_count.keys())
    print "number of fragments: %s" % len(fragment_lookup)
    print "reading and processing encrypted file"
    ciphered_text = readers.read_encoded_text()
    ciphered_words = [process_word(word) for word in ciphered_text.split()]
    translate = Translator()
    if cheat:
        if False:
            translate['l'] = 'e'
            translate['c'] = 'a'
            translate['e'] = 'x'
            translate['x'] = 'f'
            translate['a'] = 'c'
            translate['h'] = 'i'
            translate['u'] = 't'
            translate['m'] = 'h'
        else:
            n_cheat = 5
            import random
            items = true_translation.items()
            random.shuffle(items)
            for key, value in true_translation.items()[0:n_cheat]:
                print 'cheating: %s-> %s' % (key, value)
                translate[key] = value

    pair_counts = make_pair_counter()
    for ciphered_word in ciphered_words:
        update_paircounts(ciphered_word, translate, word_count, fragment_lookup, pair_counts)
    total_counts = 0.0
    for pair_key, counts in pair_counts.iteritems():
        total_counts += counts
    print "total matching word count: %s" % total_counts
    normalize_pair_counts(pair_counts, niter=100)
    pair_count_items = [(pair_key, count) for pair_key, count in pair_counts.items()
                        if pair_key[0] in ciphered_text]
    pairs_sorted = sorted(pair_count_items, key=lambda x: -x[1])
    pairs_top = pairs_sorted[0:100]
    for i, pair in enumerate(pairs_top):
        correct = pair[0][1] == true_translation[pair[0][0]]
        print i+1, pair, correct
    return pair_counts, pairs_sorted


if __name__ == "__main__":
    declipher_encrypted_file()