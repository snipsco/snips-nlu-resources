import importlib
import io
import sys

DEFAULT_ALIASES = [
    'inf',
    '1sg',
    '2sg',
    '3sg',
    '1pl',
    '2pl',
    '3pl',
    'part',
    '2sg!',
    '1pl!',
    '2pl!',
    'sg',
    '1sg->',
    '2sg->',
    '3sg->',
    '1pl->',
    '2pl->',
    '3pl->',
    '1sg?',
    '2sg?',
    '3sg?',
    '1pl?',
    '2pl?',
    '3pl?',
    '1sgp',
    '2sgp',
    '3sgp',
    '1ppl',
    '2ppl',
    '3ppl',
    'ppart',
    '1sgp+',
    '2sgp+',
    '3sgp+',
    '1ppl+',
    '2ppl+',
    '3ppl+',
    '1sgp?',
    '2sgp?',
    '3sgp?',
    '1ppl?',
    '2ppl?',
    '3ppl?',
    '1sgf',
    '2sgf',
    '3sgf',
    '1plf',
    '2plf',
    '3plf'
]


def create_conjugates(input_path, output_path, language, aliases):
    pattern_module = importlib.import_module('pattern.text.%s' % language)
    conjugate = getattr(pattern_module, 'conjugate')
    verbs = [v.strip() for v in io.open(input_path, 'r', encoding='utf-8')]

    with io.open(output_path, 'w', encoding='utf-8') as f:
        for verb in verbs:
            f.write('%s' % verb)
            conjugates = set()
            for alias in aliases:
                c = conjugate(verb, alias)
                if c is not None and c not in conjugates:
                    f.write(u';%s,%s' % (alias, c))
                    conjugates.add(c)
            f.write(u'\n')


if __name__ == '__main__':
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    lang = sys.argv[3]
    create_conjugates(input_file_path, output_file_path, lang, DEFAULT_ALIASES)
