# main pipeline for running deciphering on file

import time
import fileio
from word_count import build_word_count_from_corpus, word_list_to_fragment_lookup
from word_count import process_word
from params import alphabet, parameters
from translate import Translator, true_translation_dictionary
import solve
from logger import logger
from word_data import get_input_data, get_word_data

def decipher_encrypted_file():
    if False:
        word_count = build_word_count_from_corpus()
        frequency_min = parameters['min_frequency_word_to_fragment']
        word_count_smaller = {word: count for word, count in word_count.iteritems()
                              if count >= frequency_min}
        fragment_lookup = word_list_to_fragment_lookup(word_count_smaller.keys())
        ciphered_text = fileio.read_ciphered_text()
        ciphered_words = [process_word(word) for word in ciphered_text.split()]

    input_data = get_input_data()
    word_data = get_word_data()


    translate = Translator()
    solve.get_paircounts_translation_iteratively(translate, input_data, word_data)
    for iter in xrange(parameters['num_iterations_modify_letters']):
        solve.modify_each_letter(translate, input_data, word_data)

    logger.info('Final solution\n-------------------\n')
    true_translation = true_translation_dictionary()
    for k, v in translate.items():
        if k in input_data['ciphered_text']:
            logger.info("%s, %s, %s" % (k, v, (v == true_translation[k])))

    logger.debug("Finished decipher")
    return translate

if __name__ == "__main__":
    start = time.time()
    translate_solution = decipher_encrypted_file()
    true_translation = true_translation_dictionary()
    ciphered_text = fileio.read_ciphered_text()
    success = True
    for letter in alphabet:
        if letter in ciphered_text:
            result = translate_solution(letter)
            expected = true_translation[letter]
            if result != expected:
                print "Incorect: letter=%s, expected=%s, result=%s" % (letter, expected, result)
                success = False
    assert success
    fileio.write_solution(translate_solution)
    finish = time.time()
    runtime = finish - start
    logger.info("Success")
    logger.info("runtime: %0.1f seconds" % runtime)