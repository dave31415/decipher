data_dir = 'data'
from alphabet import alphabet


def read_encoded_text():
    """
    :return: full string of the encoded text file, lowercase
    """
    filename = "encoded-en.txt"
    return open("%s/%s" % (data_dir, filename), 'rU').read().lower()


def read_corpus_line_by_line():
    """
    :return: generator to lines of corpus text, stripped of
             endlines and lowercased
    """
    filename = "corpus-en.txt"
    with open("%s/%s" % (data_dir, filename), 'rU') as file:
        for line in file:
            yield line.strip().lower()



