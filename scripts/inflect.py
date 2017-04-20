import io
import sys

from snowballstemmer.english_stemmer import EnglishStemmer
from snowballstemmer.french_stemmer import FrenchStemmer
from snowballstemmer.german_stemmer import GermanStemmer
from snowballstemmer.spanish_stemmer import SpanishStemmer


def get_stemmer(language):
    if language == 'en':
        return EnglishStemmer()
    if language == 'fr':
        return FrenchStemmer()
    if language == 'es':
        return SpanishStemmer()
    if language == 'de':
        return GermanStemmer()
    else:
        raise ValueError("No stemmer found for language %s" % language)


def create_inflections(input_path, output_path, stemmer):
    with io.open(input_path) as f:
        words = [word.strip() for word in f]

    stems = {word: stemmer.stemWord(word) for word in words}
    stems = [(word, stem) for word, stem in stems.iteritems()]
    stems = sorted(stems, key=lambda (w, _): w)
    with io.open(output_path, mode='w') as f:
        for word, stem in stems:
            if word == stem:
                continue
            f.write(u'%s;%s\n' % (word, stem))


if __name__ == '__main__':
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    lang = sys.argv[3]
    create_inflections(input_file_path, output_file_path, get_stemmer(lang))
