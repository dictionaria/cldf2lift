import cldf2lift

import argparse
import sys

from cldfbench.cli_util import with_dataset, add_dataset_spec
from pycldf import iter_datasets


__doc__ = cldf2lift.__doc__


def register(parser):
    add_dataset_spec(parser)
    parser.add_argument(
        '-o', '--output', metavar='FILENAME', default=argparse.SUPPRESS,
        help='Output file [default: ./<sid>.lift]')
    cldf2lift.add_cli_args(parser)


def lift(dataset, args):
    for cldf in iter_datasets(dataset.cldf_dir):
        break
    else:  # pragma: nocover
        print(
            'error: no cldf dataset found in', str(dataset.cldf_dir),
            file=sys.stderr)
        return

    # invalid datasets toss a dozen lines of stack trace at the user
    try:
        cldf.validate()
    except ValueError as error:  # pragma: no cover
        print('Invalid CLDF dataset:', str(error), file=sys.stderr)
        return

    lift = cldf2lift.cldf2lift(
        cldf,
        args.language, args.meta_language, args.meta_language_2,
        args.meta_language_3,
        args.headword_column, args.description_col_2, args.translation_col_2,
        args.description_col_3, args.translation_col_3,
        args.variant_col, args.sense_id_col)

    outfile = args.output if args.output else '{}.lift'.format(dataset.id)
    with open(outfile, 'wb') as f:
        lift.write(f, encoding='UTF-8')


def run(args):  # pragma: no cover
    with_dataset(args, lift)
