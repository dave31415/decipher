from params import alphabet, parameters
from letter_matrix import make_pair_counter, normalize_pair_counts
from translate import true_translation_dictionary
import math
from logger import logger
import analyze


def all_possible_words(ciphered_word, translate, word_data):
    """
    :param ciphered_word: string
    :param translate: Translation object
    :param word_data: dictionary holding word count data
    :return: all possible words given the constraint of the
             partial Translation
    """
    deciphered_word = translate(ciphered_word)
    if deciphered_word in word_data['word_count']:
        possible_words = [deciphered_word]
    else:
        possible_words = word_data['fragment_lookup'][deciphered_word]
    return possible_words


def update_paircounts(translate, ciphered_word, word_data, pair_counts):
    """
    Updates the paircount in-place
    :param translate: Translation object
    :param ciphered_word: string
    :param word_data: dictionary holding word count data
    :param pair_counts: pair count dictionary
    :return: None
    """
    possible_words = all_possible_words(ciphered_word, translate, word_data)
    for possible_word in possible_words:
        for ciphered_letter, possible_letter in \
                zip(ciphered_word, possible_word):
            pair_key = (ciphered_letter, possible_letter)
            counts = word_data['word_count'][possible_word]
            pair_counts[pair_key] += counts


def get_normalized_paircounts(translate, input_data, word_data):
    """
    :param translate: Translation object
    :param input_data: dictionary holding the input data
    :param word_data: dictionary holding word count data
    :return: pair counts, normalized
    """
    pair_counts = make_pair_counter()
    for ciphered_word in input_data['ciphered_words']:
        update_paircounts(translate, ciphered_word, word_data, pair_counts)

    normalize_pair_counts(pair_counts)
    return pair_counts


def get_maximum_likelihood_values(pair_counts, input_data):
    """
    Get the maximum likelihood values from the pair_counts
    for each letter
    :param pair_counts: pair counts, normalized
    :param input_data: dictionary holding the input data
    :return: dictionary of maximum likelihood values
    """
    true_translation = true_translation_dictionary()
    max_like = {}
    for ciphered_letter in alphabet:
        like_max = 0.0
        for deciphered_letter in alphabet:
            pair_key = (ciphered_letter, deciphered_letter)
            like = pair_counts[pair_key]
            if like > like_max:
                like_max = like
                occurrence = input_data['ciphered_text'].count(ciphered_letter)
                correct = true_translation[
                    ciphered_letter] == deciphered_letter
                max_like[ciphered_letter] = (
                    deciphered_letter, like, occurrence, correct)
    return max_like


def get_most_likely_values(pair_counts, input_data):
    """
    Utility for getting a short list of likely values
    currently used for debugging only
    :param pair_counts: pair counts, normalized
    :param ciphered_text:
    :return:
    """
    true_translation = true_translation_dictionary()
    top = 4
    most_likely = {}
    for ciphered_letter in alphabet:
        letter_list = []
        for deciphered_letter in alphabet:
            pair_key = (ciphered_letter, deciphered_letter)
            like = pair_counts[pair_key]
            occurrence = input_data['ciphered_text'].count(ciphered_letter)
            correct = true_translation[ciphered_letter] == deciphered_letter
            letter_list.append((deciphered_letter, like, occurrence, correct))
        letter_list = sorted(letter_list, key=lambda x: -x[1])[0:top]
        most_likely[ciphered_letter] = letter_list
    for ciphered_letter in alphabet:
        letter_list = most_likely[ciphered_letter]
        correct = [item[3] for item in letter_list]
        print ciphered_letter, correct, True in correct

    return most_likely


def get_translation_guess_from_max_like(max_like, occurrence_min=5, top=10):
    """
    Update the translation using the best determined letters
    :param max_like: maximum likelihood dictionary
    :param occurrence_min: minimum occurrance of letter in ciphered text
                           to be considered
    :param top: choose this many of the best letters
    :return:
    """
    items = [item for item in max_like.items() if item[1][2] >= occurrence_min]
    items_sorted = sorted(items, key=lambda x: -x[1][1])
    items_top = items_sorted[0: top]
    return {k: v[0] for k, v in items_top}


def get_paircounts_translation_iteratively(translate, input_data, word_data):
    """
    Update the translation iteratively based on constrained letter frequency
    :param translate: Translation object
    :param input_data: dictionary holding the input data
    :param word_data: dictionary holding word count data
    :return:
    """
    # number of total iterations
    iterations = parameters['paircounts_solver_iterations']
    # number of highest likelihood letters to select to be fixed after the
    # first iterations. Increases by one letter thereafter.
    top_start = parameters['paircounts_solver_num_top_start']
    for iteration in xrange(iterations):

        pair_counts = get_normalized_paircounts(
            translate, input_data, word_data)
        entropy = sum([-i * math.log(i) for i in pair_counts.values()])
        logger.debug("\t\titer: %s, entropy: %s" % (iteration, entropy))

        max_like = get_maximum_likelihood_values(pair_counts, input_data)
        # parameters definition how occurence min starts our and
        # reduces with each iteration
        # idea is that you don't want to fix the letters that occur the least
        # too early in the process as they are probably least well determined
        om_start = parameters['paircounts_solver_occurrence_min_start']
        om_sub_per_iter = parameters[
            'paircounts_solver_occurrence_reduction_per_iteration']
        om = om_start - om_sub_per_iter
        top = int(top_start + iteration)
        logger.debug("occurrence_min: %s, top: %s" % (om, top))
        translation_guess = \
            get_translation_guess_from_max_like(max_like,
                                                occurrence_min=om, top=top)
        for k, v in translation_guess.iteritems():
            if k in input_data['ciphered_text']:
                translate[k] = v
        num_trans, un_matched_ciphered_letters = \
            number_of_translated_words(translate, input_data, word_data)
        logger.debug("num matched words: %s" % num_trans)
        if False:
            # for debugging
            analyze.show_translation(translate)
            analyze.show_deciphered_text(translate)


def number_of_translated_words(translate, input_data, word_data):
    """
    Get the number of translated words
    :param translate: Translation object
    :param input_data: dictionary holding the input data
    :param word_data: dictionary holding word count data
    :return: tuple (number of matched words, unmatched ciphered letters)
    """
    ciphered_words = input_data['ciphered_words']
    deciphered_words = [translate(word) for word in ciphered_words]

    matched_words = [
        word for word in deciphered_words if word in word_data['word_count']]
    n_matched_words = len(matched_words)
    all_words = len(deciphered_words)
    logger.debug("n matched_words: %s, all_words: %s" %
                 (n_matched_words, all_words))
    un_matched_ciphered_words = \
        [word for word in ciphered_words
         if translate(word) not in word_data['word_count']]

    unmatched_string = ' '.join(un_matched_ciphered_words)
    un_matched_ciphered_letters = sorted(
        list({letter for letter in unmatched_string if letter in alphabet}))

    logger.debug("num unmatched ciphered letters: %s" %
                 len(un_matched_ciphered_letters))
    return n_matched_words, un_matched_ciphered_letters


def modify_each_letter(translate, input_data, word_data):
    """
    Update translation by modifying each letter to see if it improves
    :param translate: Translation object
    :param input_data: dictionary holding the input data
    :param word_data: dictionary holding word count data
    :return:
    """
    num_max, un_matched_ciphered_letters = \
        number_of_translated_words(translate, input_data, word_data)
    for ciphered_letter in un_matched_ciphered_letters:
        for deciphered_letter in alphabet:
            translate_copy = translate.clone()
            translate_copy[ciphered_letter] = deciphered_letter
            logger.debug("%s->%s" % (ciphered_letter, deciphered_letter))
            num, unmatched_letters = \
                number_of_translated_words(
                    translate_copy, input_data, word_data)

            if num > num_max:
                logger.debug("New best, num_words matched: %s" % num)
                translate[ciphered_letter] = deciphered_letter
                num_max = num
            else:
                logger.debug("num_words match: %s <= num_max: %s" %
                             (num, num_max))
