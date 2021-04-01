#!/usr/bin/env python3

import cldf2lift

import argparse
import sys

from pycldf import Dataset

DESC = '''\
Convert a dictionary from the Cross Linguistic Data Formats (CLDF)
to the Lexicon Interchange FormaT (LIFT).

This program expects the following convention regarding the meta languages:

The *primary meta language* refers to the language used in the  `Description`
column of the `SenseTable`.

The *secondary meta language* refers to the language used in the
`alt_translation1` column of the `SenseTable`.

The *tertiary meta language* refers to the language used in the
`alt_translation2` column of the `SenseTable`.

Note: For all language codes, LIFT expects two-letter ISO 639-1 codes (e.g.
      `en` for English).  If such a code is not available for your language,
      fall back to its three-letter ISO 639-2/3 code.
'''


def main():
    arg_parser = argparse.ArgumentParser(description=DESC)
    arg_parser.add_argument(
        'input_file', metavar='CLDF-METADATA', help='CLDF metadata file')
    arg_parser.add_argument(
        '-o', '--output', metavar='FILENAME', default='-',
        help='Output file or `-` for standard output [default: -]')
    arg_parser.add_argument(
        '-l', '--language', metavar='LANG', default='und',
        help='ISO 639-1 code of the language [default: und]')
    arg_parser.add_argument(
        '--meta-language', metavar='LANG', default='en',
        help='ISO 639-1 code of the primary meta language [default: en]')
    arg_parser.add_argument(
        '--meta-language-2', metavar='LANG', default=None,
        help='ISO 639-1 code of the secondary meta language [default: None]')
    arg_parser.add_argument(
        '--meta-language-3', metavar='LANG', default=None,
        help='ISO 639-1 code of the tertiary meta language [default: None]')

    config = arg_parser.parse_args()

    cldf = Dataset.from_metadata(config.input_file)
    entries, senses, examples = cldf2lift.extract_cldf_data(cldf)
    lift = cldf2lift.make_lift(
        entries, senses, examples,
        config.language, config.meta_language)

    if config.output == '-':
        lift.write(sys.stdout, encoding='unicode', xml_declaration=True)
    else:
        with open(config.output, 'wb') as f:
            lift.write(f, encoding='UTF-8', xml_declaration=True)


if __name__ == '__main__':
    main()
