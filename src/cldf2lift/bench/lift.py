"""
Convert CLDF dataset into the Lexicon Interchange FormaT (LIFT).
"""

import cldf2lift

import sys

from cldfbench.cli_util import with_dataset, add_dataset_spec
from pycldf import iter_datasets


def register(parser):
    add_dataset_spec(parser)
    parser.add_argument(
        '-o', '--output', metavar='FILENAME',
        help='Output file [default: ./<sid>.lift]')
    # TODO get 2-letter isocodes from md.json + magic
    parser.add_argument(
        '-l', '--language', metavar='LANG', default='und',
        help='ISO 639-1 code of the language [default: und]')
    parser.add_argument(
        '--meta-language', metavar='LANG', default='en',
        help='ISO 639-1 code of the primary meta language [default: en]')
    parser.add_argument(
        '--meta-language-2', metavar='LANG', default=None,
        help='ISO 639-1 code of the secondary meta language [default: None]')
    parser.add_argument(
        '--meta-language-3', metavar='LANG', default=None,
        help='ISO 639-1 code of the tertiary meta language [default: None]')


def lift(dataset, args):
    for cldf in iter_datasets(dataset.cldf_dir):
        break
    else:
        print(
            'error: no cldf dataset found in', str(dataset.cldf_dir),
            file=sys.stderr)
        return

    entries, senses, examples = cldf2lift.extract_cldf_data(cldf)
    lift = cldf2lift.make_lift(
        entries, senses, examples,
        args.language, args.meta_language, args.meta_language_2,
        args.meta_language_3)

    outfile = args.output if args.output else '{}.lift'.format(dataset.id)
    with open(outfile, 'wb') as f:
        lift.write(f, encoding='UTF-8')


def run(args):
    with_dataset(args, lift)
