#!/usr/bin/env python3

import cldf2lift

import argparse
import sys

from pycldf import Dataset


def main():
    arg_parser = argparse.ArgumentParser(
        description=cldf2lift.__doc__,
        formatter_class=argparse.RawTextHelpFormatter)
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
        help='ISO 639-1 code of the secondary meta language [default: None] (Dictionaria extension)')
    arg_parser.add_argument(
        '--meta-language-3', metavar='LANG', default=None,
        help='ISO 639-1 code of the tertiary meta language [default: None] (Dictionaria extension)')

    config = arg_parser.parse_args()

    cldf = Dataset.from_metadata(config.input_file)
    entries, senses, examples = cldf2lift.extract_cldf_data(cldf)
    lift = cldf2lift.make_lift(
        entries, senses, examples,
        config.language, config.meta_language, config.meta_language_2,
        config.meta_language_3)

    if config.output == '-':
        lift.write(
            sys.stdout, encoding='unicode')
    else:
        with open(config.output, 'wb') as f:
            lift.write(f, encoding='UTF-8')


if __name__ == '__main__':
    main()
