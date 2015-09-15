import readers
from word_count import build_word_count_from_corpus, word_list_to_fragment_lookup
from alphabet import alphabet, unknown_letter


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


def declipher_encrypted_file():
    #try to keep memory usage < 1 GB
    quick = True
    if quick:
        print "using 'quick' parameters"
        word_length_max = 6
        frequency_min = 100
    else:
        word_length_max = 11
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
    translate = Translator()
    fragmented_text = translate(ciphered_text)

    #print ciphered_text
    #print
    #print fragmented_text

if __name__ == "__main__":
    declipher_encrypted_file()