import importlib
import io

import sys


def create_lexemes(input_path, output_path, language):
    pattern_module = importlib.import_module('pattern.text.%s' % language)
    lexeme = getattr(pattern_module, 'lexeme')
    verbs = [v.strip() for v in io.open(input_path, 'r', encoding='utf-8')]

    with io.open(output_path, 'w', encoding='utf-8') as f:
        for verb in verbs:
            lexemes = ','.join(lexeme(verb))
            f.write('%s;%s\n' % (verb, lexemes))


if __name__ == '__main__':
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    lang = sys.argv[3]
    create_lexemes(input_file_path, output_file_path, lang)
