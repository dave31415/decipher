from params import data_dir
from translate import Translator


def read_ciphered_text():
    """
    :return: full string of the encoded text file, lowercase
    """
    filename = "encoded-en.txt"
    # filename = "encoded-en-smaller-15.txt"
    return open("%s/%s" % (data_dir, filename), 'rU').read().lower()


def read_corpus_line_by_line():
    """
    :return: generator to lines of corpus text, stripped of
             endlines and lowercased
    """
    filename = "corpus-en.txt"
    with open("%s/%s" % (data_dir, filename), 'rU') as file_pointer:
        for line in file_pointer:
            yield line.strip().lower()


def write_translation_solution(translate):
    """
    Writes the translation solution to the desired file and format
    :param translate: the solved-for translate object
    :return: None
    """
    filename = "%s/%s" % (data_dir, "solved_translation.txt")
    with open(filename, 'w') as file_pointer:
        for ciphered_letter, deciphered_letter in translate.iteritems():
            output_line = "%s -> %s\n" % (ciphered_letter, deciphered_letter)
            file_pointer.write(output_line)


def write_deciphered_text(translate):
    """
    Writes the deciphered text to the desired file and format
    :param translate: the solved-for translate object
    :return: None
    """
    ciphered_text = read_ciphered_text()
    deciphered_text = translate(ciphered_text)
    filename = "%s/%s" % (data_dir, "deciphered.txt")
    open(filename, 'w').write(deciphered_text)


def write_solution(translate):
    """
    Writes the deciphered text and the solution to files
    :param translate: the solved-for translate object
    :return: None
    """
    write_translation_solution(translate)
    write_deciphered_text(translate)


def read_translation_solution():
    """
    Reads the translation solution back into a Translate object
    :return: Translate object
    """
    translate = Translator()
    filename = "%s/%s" % (data_dir, "solved_translation.txt")
    for line in open(filename, 'rU').readlines():
        ciphered_letter, deciphered_letter = line.strip().split(' -> ')
        translate[ciphered_letter] = deciphered_letter
    return translate



