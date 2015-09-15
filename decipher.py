import fileio
from word_count import build_word_count_from_corpus, word_list_to_fragment_lookup
from word_count import process_word
from alphabet import alphabet
from letter_matrix import make_pair_counter, normalize_pair_counts
from translate import Translator, true_translation_dictionary
import math
import time


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


def get_normalized_paircounts(ciphered_words, translate, word_count,
                              fragment_lookup):
    pair_counts = make_pair_counter()
    for ciphered_word in ciphered_words:
        update_paircounts(ciphered_word, translate, word_count, fragment_lookup, pair_counts)
    total_counts = 0.0
    for pair_key, counts in pair_counts.iteritems():
        total_counts += counts
    #print "total matching word count: %s" % total_counts
    normalize_pair_counts(pair_counts, niter=100)
    return pair_counts


def get_maximum_likelihood_values(pair_counts, ciphered_text):
    true_translation = true_translation_dictionary()
    max_like = {}
    for ciphered_letter in alphabet:
        like_max = 0.0
        for deciphered_letter in alphabet:
            pair_key = (ciphered_letter, deciphered_letter)
            like = pair_counts[pair_key]
            if like > like_max:
                like_max = like
                occurrence = ciphered_text.count(ciphered_letter)
                correct = true_translation[ciphered_letter] == deciphered_letter
                max_like[ciphered_letter] = (deciphered_letter, like, occurrence, correct)
    return max_like


def get_translation_guess_from_max_like(max_like, occurrence_min=5, top=10):
    items = [item for item in max_like.items() if item[1][2] >= occurrence_min]
    items_sorted = sorted(items, key=lambda x: -x[1][1])
    items_top = items_sorted[0: top]
    #for item in items_top:
    #    print item
    return {k: v[0] for k, v in items_top}


def get_paircounts_translation_iteratively(ciphered_words, translate, word_count,
                                           fragment_lookup, ciphered_text,
                                           iterations=30, top_start=10):
    pair_counts, entropy, max_like = None, None, None
    for iteration in xrange(iterations):

        pair_counts = get_normalized_paircounts(ciphered_words, translate, word_count,
                                                fragment_lookup)
        entropy = sum([-i*math.log(i) for i in pair_counts.values()])
        print "\t\titer: %s, entropy: %s" % (iteration, entropy)

        max_like = get_maximum_likelihood_values(pair_counts, ciphered_text)
        om = 5-iteration/5.0
        top = int(top_start + iteration)
        print "occurrence_min: %s, top: %s" % (om, top)
        translation_guess = get_translation_guess_from_max_like(max_like,
                                                                occurrence_min=om, top=top)
        for k, v in translation_guess.iteritems():
            if k in ciphered_text:
                translate[k] = v
        num_trans, un_matched_ciphered_letters = number_of_translated_words(translate, word_count, ciphered_text)
        print "num matched words: %s" % num_trans

    return pair_counts, entropy, max_like


def number_of_translated_words(translate, word_count, ciphered_text):
    ciphered_words = [process_word(word) for word in ciphered_text.split()]
    deciphered_words = [translate(word) for word in ciphered_words]

    matched_words = [word for word in deciphered_words if word in word_count]
    n_matched_words = len(matched_words)
    all_words = len(deciphered_words)
    print "n matched_words: %s, all_words: %s" % (n_matched_words, all_words)
    un_matched_words = [word for word in deciphered_words if word not in word_count]

    un_matched_ciphered_words = [word for word in ciphered_words if translate(word) not in word_count]

    print "matched words"
    print matched_words
    print
    print "un-matched words"
    print un_matched_words

    unmatched_string = ' '.join(un_matched_ciphered_words)
    un_matched_ciphered_letters = sorted(list({letter for letter in unmatched_string if letter in alphabet}))

    print "num unmatched ciphered letters: %s" % len(un_matched_ciphered_letters)
    print un_matched_ciphered_letters
    return n_matched_words, un_matched_ciphered_letters


def modify_each_letter(translate, word_count, ciphered_text):
    num_max, un_matched_ciphered_letters = number_of_translated_words(translate, word_count, ciphered_text)
    for ciphered_letter in un_matched_ciphered_letters:
        for deciphered_letter in alphabet:
            translate_copy = translate.clone()
            translate_copy[ciphered_letter] = deciphered_letter
            print "%s->%s" % (ciphered_letter, deciphered_letter)
            num, unmatched_letters = number_of_translated_words(translate_copy, word_count, ciphered_text)
            if num > num_max:
                print "New best, num_words matched: %s" %num
                translate[ciphered_letter] = deciphered_letter
                num_max = num
            else:
                print "num_words match: %s <= num_max: %s" % (num, num_max)


def decipher_encrypted_file():
    #try to keep memory usage < 1 GB
    start = time.time()
    quick = False
    cheat = False
    true_translation = true_translation_dictionary()
    if quick:
        print "using 'quick' parameters"
        word_length_max = 5
        frequency_min = 200
    else:
        word_length_max = 9
        frequency_min = 20

    print 'building word counter'
    word_count = build_word_count_from_corpus()
    print "words in word_count: %s" % len(word_count)
    #compress it a bit
    word_count_smaller = {word: count for word, count in word_count.iteritems()
                          if len(word) <= word_length_max and count >= frequency_min}
    print "words in shortened word_count: %s" % len(word_count_smaller)
    print "word_length_max: %s, frequency_min: %s" % (word_length_max, frequency_min)
    print 'building fragment lookup'
    fragment_lookup = word_list_to_fragment_lookup(word_count_smaller.keys())
    print "number of fragments: %s" % len(fragment_lookup)
    print "reading and processing encrypted file"
    ciphered_text = fileio.read_ciphered_text()
    ciphered_words = [process_word(word) for word in ciphered_text.split()]
    translate = Translator()
    if cheat:
        for xx in xrange(10):
            print "cheating"
        if True:
            translate['y'] = 'y'
            translate['i'] = 'p'
        else:
            n_cheat = 5
            import random
            items = true_translation.items()
            random.shuffle(items)
            for key, value in true_translation.items()[0:n_cheat]:
                print 'cheating: %s-> %s' % (key, value)
                translate[key] = value

    n_iter = 30
    pair_counts = get_paircounts_translation_iteratively(ciphered_words, translate, word_count,
                                           fragment_lookup, ciphered_text, iterations=n_iter)

    results = []
    for ciphered_letter in alphabet:
        # delete each and try again to fix incorrect matches
        print "deleted letter: %s" % ciphered_letter
        if ciphered_letter not in translate:
            continue
        del translate[ciphered_letter]
        pair_counts, entropy, max_like = \
            get_paircounts_translation_iteratively(ciphered_words, translate, word_count,
                                                   fragment_lookup, ciphered_text,
                                                   iterations=n_iter, top_start=20)
        results.append((max_like, entropy))
        print translate(ciphered_text)

    print '\n------------\n'

    pair_count_items = [(pair_key, count) for pair_key, count in pair_counts.items()
                        if pair_key[0] in ciphered_text]
    pairs_sorted = sorted(pair_count_items, key=lambda x: -x[1])
    pairs_top = pairs_sorted[0:100]
    for i, pair in enumerate(pairs_top):
        correct = pair[0][1] == true_translation[pair[0][0]]
        print i+1, pair, correct

    print translate(ciphered_text)

    if True:
        print 'print modiying each letter to maximize number of words'
        modify_each_letter(translate, word_count, ciphered_text)

    print 'Final solution\n-------------------\n'
    for k, v in translate.items():
        if k in ciphered_text:
            print k, v, (v == true_translation[k])

    max_like = get_maximum_likelihood_values(pair_counts, ciphered_text)

    finish = time.time()
    runtime = finish - start
    print "runtime: %0.1f seconds" % runtime
    return pair_counts, max_like, translate, word_count

if __name__ == "__main__":
    declipher_encrypted_file()