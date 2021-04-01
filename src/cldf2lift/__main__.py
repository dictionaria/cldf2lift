#!/usr/bin/env python3

from pycldf import Dataset
import cldf2lift


def main():

    infile = 'tests/test_data/Dictionary-metadata.json'
    outfile = 'tests/test_data/lift-export.lift'
    # TODO add proper 'lang' attribute (wants two-letter isocode?)
    lang = 'und-Latn'
    metalanguage = 'en'

    cldf = Dataset.from_metadata(infile)
    entries, senses, examples = cldf2lift.extract_cldf_data(cldf)
    lift = cldf2lift.make_lift(entries, senses, examples, lang, metalanguage)

    with open(outfile, 'wb') as f:
        lift.write(f, encoding='UTF-8', xml_declaration=True)


if __name__ == '__main__':
    main()
