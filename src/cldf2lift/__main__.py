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
    cldf2lift.add_cli_args(arg_parser)

    config = arg_parser.parse_args()

    cldf = Dataset.from_metadata(config.input_file)
    entries, senses, examples = cldf2lift.extract_cldf_data(
        cldf,
        config.description_col_2, config.translation_col_2,
        config.description_col_3, config.translation_col_3,
        config.variant_col, config.sense_id_col)
    lift = cldf2lift.make_lift(
        entries, senses, examples,
        config.language, config.meta_language, config.meta_language_2,
        config.meta_language_3,
        config.description_col_2, config.translation_col_2,
        config.description_col_3, config.translation_col_3,
        config.variant_col)

    if config.output == '-':
        lift.write(
            sys.stdout, encoding='unicode')
    else:
        with open(config.output, 'wb') as f:
            lift.write(f, encoding='UTF-8')


if __name__ == '__main__':
    main()
