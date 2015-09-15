import time
import fileio
from word_count import build_word_count_from_corpus, word_list_to_fragment_lookup
from word_count import process_word
from alphabet import alphabet
from translate import Translator, true_translation_dictionary
import solve
from logger import logger


def decipher_encrypted_file():
    logger.debug("Starting decipher")
    true_translation = true_translation_dictionary()

    word_length_max = 9
    frequency_min = 20

    logger.debug('building word counter')
    word_count = build_word_count_from_corpus()
    logger.debug("words in word_count: %s" % len(word_count))
    #compress it a bit
    word_count_smaller = {word: count for word, count in word_count.iteritems()
                          if len(word) <= word_length_max and count >= frequency_min}
    logger.debug("words in shortened word_count: %s" % len(word_count_smaller))
    logger.debug("word_length_max: %s, frequency_min: %s" % (word_length_max, frequency_min))
    logger.debug("building fragment lookup")
    fragment_lookup = word_list_to_fragment_lookup(word_count_smaller.keys())
    logger.debug("number of fragments: %s" % len(fragment_lookup))
    logger.debug("reading and processing encrypted file")
    ciphered_text = fileio.read_ciphered_text()
    ciphered_words = [process_word(word) for word in ciphered_text.split()]
    translate = Translator()
    solve.get_paircounts_translation_iteratively(
        ciphered_words, translate, word_count, fragment_lookup,
        ciphered_text, iterations=30)

    logger.debug('modifying each letter to maximize number of words')
    solve.modify_each_letter(translate, word_count, ciphered_text)

    logger.info('Final solution\n-------------------\n')
    for k, v in translate.items():
        if k in ciphered_text:
            logger.info("%s, %s, %s" % (k, v, (v == true_translation[k])))

    logger.debug("Finished decipher")
    return translate

if __name__ == "__main__":
    start = time.time()
    translate_solution = decipher_encrypted_file()
    true_translation = true_translation_dictionary()
    for letter in alphabet:
        assert translate_solution(letter) == true_translation[letter]
    fileio.write_solution(translate_solution)
    finish = time.time()
    runtime = finish - start
    logger.info("Success")
    logger.info("runtime: %0.1f seconds" % runtime)