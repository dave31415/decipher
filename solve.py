from word_count import process_word
from params import alphabet, parameters
from letter_matrix import make_pair_counter, normalize_pair_counts
from translate import true_translation_dictionary
import math
from collections import Counter
from logger import logger


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
            #can change the scaling
            pair_counts[pair_key] += counts


def get_normalized_paircounts(ciphered_words, translate, word_count,
                              fragment_lookup):
    pair_counts = make_pair_counter()
    for ciphered_word in ciphered_words:
        update_paircounts(ciphered_word, translate, word_count, fragment_lookup, pair_counts)
    total_counts = 0.0
    for pair_key, counts in pair_counts.iteritems():
        total_counts += counts
    normalize_pair_counts(pair_counts)
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
    return {k: v[0] for k, v in items_top}


def get_paircounts_translation_iteratively(ciphered_words, translate, word_count,
                                           fragment_lookup, ciphered_text):
    # number of total iterations
    iterations = parameters['paircounts_solver_iterations']
    # number of highest likelihood letters to select to be fixed after the
    # first iterations. Increases by one letter thereafter.
    top_start = parameters['paircounts_solver_num_top_start']
    for iteration in xrange(iterations):

        pair_counts = get_normalized_paircounts(ciphered_words, translate, word_count,
                                                fragment_lookup)
        entropy = sum([-i*math.log(i) for i in pair_counts.values()])
        logger.debug("\t\titer: %s, entropy: %s" % (iteration, entropy))

        max_like = get_maximum_likelihood_values(pair_counts, ciphered_text)
        # parameters definition how occurence min starts our and
        # reduces with each iteration
        # idea is that you don't want to fix the letters that occur the least
        # too early in the process as they are probably least well determined
        om_start = parameters['paircounts_solver_occurrence_min_start']
        om_sub_per_iter = parameters['paircounts_solver_occurrence_reduction_per_iteration']
        om = om_start - om_sub_per_iter
        top = int(top_start + iteration)
        logger.debug("occurrence_min: %s, top: %s" % (om, top))
        translation_guess = get_translation_guess_from_max_like(max_like,
                                                                occurrence_min=om, top=top)
        for k, v in translation_guess.iteritems():
            if k in ciphered_text:
                translate[k] = v
        num_trans, un_matched_ciphered_letters = number_of_translated_words(translate, word_count, ciphered_text)
        logger.debug("num matched words: %s" % num_trans)


def analyze_letters(matched_words, un_matched_words):
    #debugging utility
    matched_counter = Counter()
    un_matched_counter = Counter()
    for letter in ''.join(matched_words):
        matched_counter[letter] += 1
    for letter in ''.join(un_matched_words):
        un_matched_counter[letter] += 1

    alpha = 5.0
    prior = 2.0
    prob_wrong = {}
    logger.debug("Prob that letters are wrong")
    for letter in alphabet:
        ratio = (alpha + matched_counter[letter])/(alpha + un_matched_counter[letter])
        prob_wrong[letter] = 1.0/(1.0 + ratio*prior)
    for letter, p_wrong in sorted(prob_wrong.items(), key=lambda x: -x[1]):
        logger.debug("%s, prob_wrong=%s" % (letter, p_wrong))

    logger.debug('most common matched letters')
    logger.debug(matched_counter.most_common().__repr__())
    logger.debug('most common un_matched letters')
    logger.debug(un_matched_counter.most_common().__repr__())


def number_of_translated_words(translate, word_count, ciphered_text):
    ciphered_words = [process_word(word) for word in ciphered_text.split()]
    deciphered_words = [translate(word) for word in ciphered_words]

    matched_words = [word for word in deciphered_words if word in word_count]
    n_matched_words = len(matched_words)
    all_words = len(deciphered_words)
    logger.debug("n matched_words: %s, all_words: %s" % (n_matched_words, all_words))
    un_matched_words = [word for word in deciphered_words if word not in word_count]
    un_matched_ciphered_words = [word for word in ciphered_words if translate(word) not in word_count]

    if True:
        logger.debug("matched words")
        logger.debug("%s\n" % matched_words.__repr__())
        logger.debug("un-matched words")
        logger.debug("%s\n" % un_matched_words.__repr__())
        analyze_letters(matched_words, un_matched_words)

    unmatched_string = ' '.join(un_matched_ciphered_words)
    un_matched_ciphered_letters = sorted(list({letter for letter in unmatched_string if letter in alphabet}))

    logger.debug("num unmatched ciphered letters: %s" % len(un_matched_ciphered_letters))
    return n_matched_words, un_matched_ciphered_letters


def modify_each_letter(translate, word_count, ciphered_text):
    num_max, un_matched_ciphered_letters = number_of_translated_words(translate, word_count, ciphered_text)
    for ciphered_letter in un_matched_ciphered_letters:
        for deciphered_letter in alphabet:
            translate_copy = translate.clone()
            translate_copy[ciphered_letter] = deciphered_letter
            logger.debug("%s->%s" % (ciphered_letter, deciphered_letter))
            num, unmatched_letters = number_of_translated_words(translate_copy, word_count, ciphered_text)
            if num > num_max:
                logger.debug("New best, num_words matched: %s" %num)
                translate[ciphered_letter] = deciphered_letter
                num_max = num
            else:
                logger.debug("num_words match: %s <= num_max: %s" % (num, num_max))