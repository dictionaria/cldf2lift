'''\
Convert a dictionary from the Cross Linguistic Data Formats (CLDF)
to the Lexicon Interchange FormaT (LIFT).

This program expects the following convention regarding the meta languages:

The *primary meta language* refers to the language used in the  `Description`
column of the `SenseTable`.

The *secondary meta language* refers to the language used in the
`alt_translation1` column of the `SenseTable`.

The *tertiary meta language* refers to the language used in the
`alt_translation2` column of the `SenseTable`.

Note 1: For all language codes, LIFT expects two-letter ISO 639-1 codes (e.g.
        `en` for English).  If such a code is not available for your language,
        fall back to its three-letter ISO 639-2/3 code.

Note 2: `alt_translation1` and `alt_translation2` are not part of the CLDF
        standard but rather a convention used by the Dictionaria project
        (dictionaria.clld.org).
'''

from collections import defaultdict
from xml.etree import ElementTree as ET


CLDF_ID = 'http://cldf.clld.org/v1.0/terms.rdf#id'
CLDF_LANG_ID = 'http://cldf.clld.org/v1.0/terms.rdf#languageReference'
CLDF_HEADWORD = 'http://cldf.clld.org/v1.0/terms.rdf#headword'
CLDF_POS = 'http://cldf.clld.org/v1.0/terms.rdf#partOfSpeech'

CLDF_DESC = 'http://cldf.clld.org/v1.0/terms.rdf#description'
CLDF_ENTRY_ID = 'http://cldf.clld.org/v1.0/terms.rdf#entryReference'

CLDF_PRIMARY = 'http://cldf.clld.org/v1.0/terms.rdf#primaryText'
CLDF_ANALYZED = 'http://cldf.clld.org/v1.0/terms.rdf#analyzedWord'
CLDF_GLOSS = 'http://cldf.clld.org/v1.0/terms.rdf#gloss'
CLDF_TRANS = 'http://cldf.clld.org/v1.0/terms.rdf#translatedText'
CLDF_METALANG_ID = 'http://cldf.clld.org/v1.0/terms.rdf#metaLanguageReference'
CLDF_COMMENT = 'http://cldf.clld.org/v1.0/terms.rdf#comment'


ENTRY_COLS = [
    CLDF_ID,
    CLDF_LANG_ID,
    CLDF_HEADWORD,
    CLDF_POS,
]
SENSE_COLS = [
    CLDF_ID,
    CLDF_DESC,
    CLDF_ENTRY_ID,
]
EXAMPLE_COLS = [
    CLDF_ID,
    CLDF_LANG_ID,
    CLDF_PRIMARY,
    CLDF_ANALYZED,
    CLDF_GLOSS,
    CLDF_TRANS,
    CLDF_METALANG_ID,
    CLDF_COMMENT,
]


def add_cli_args(arg_parser):
    # TODO get 2-letter isocodes from md.json + magic
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
        '--description-col-2', metavar='COLUMNNAME', default='alt_translation1',
        help='Column name for sense description in meta language 2 [default=alt_translation2]')
    arg_parser.add_argument(
        '--translation-col-2', metavar='COLUMNNAME', default='alt_translation1',
        help='Column name for example translation in meta language 2 [default=alt_translation2]')

    arg_parser.add_argument(
        '--meta-language-3', metavar='LANG', default=None,
        help='ISO 639-1 code of the tertiary meta language [default: None] (Dictionaria extension)')
    arg_parser.add_argument(
        '--description-col-3', metavar='COLUMNNAME', default='alt_translation2',
        help='Column name for sense description in meta language 3 [default=alt_translation2]')
    arg_parser.add_argument(
        '--translation-col-3', metavar='COLUMNNAME', default='alt_translation2',
        help='Column name for example translation in meta language 3 [default=alt_translation2]')

    arg_parser.add_argument(
        '--variant-col', metavar='COLUMNNAME', default='Variant_Form',
        help='Column name for variants [default=Variant_Form]')
    arg_parser.add_argument(
        '--sense-id-col', metavar='COLUMNNAME', default='Sense_IDs',
        help='Column name for references to sense in the example table [default=Sense_IDs]')


def extract_cldf_data(
    cldf,
    sn_alttrans_col1, ex_alttrans_col1,
    sn_alttrans_col2, ex_alttrans_col2,
    variant_col, sense_id_col
):
    sense_cols = [
        col
        for col in SENSE_COLS
        if cldf.get(('SenseTable', col))]
    sense_cols.extend(
        col
        for col in (sn_alttrans_col1, sn_alttrans_col2)
        if col and cldf.get(('SenseTable', col)))

    senses = defaultdict(list)
    for sense in cldf.iter_rows('SenseTable', *sense_cols):
        entry_id = sense.get(CLDF_ENTRY_ID)
        senses[entry_id].append(sense)

    entry_cols = [
        col
        for col in ENTRY_COLS
        if cldf.get(('EntryTable', col))]
    entry_cols.extend(
        col
        for col in (variant_col,)
        if col and cldf.get(('EntryTable', col)))
    entries = [
        e
        for e in cldf.iter_rows('EntryTable', *entry_cols)
        if e.get(CLDF_ID) in senses]

    if cldf.get('ExampleTable'):
        example_cols = [
            col
            for col in EXAMPLE_COLS
            if cldf.get(('ExampleTable', col))]
        example_cols.extend(
            col
            for col in (
                sense_id_col, ex_alttrans_col1, ex_alttrans_col2
            )
            if col and cldf.get(('ExampleTable', col)))

        examples = defaultdict(list)
        for example in cldf.iter_rows('ExampleTable', *example_cols):
            sense_ids = example.get(sense_id_col)
            for sense_id in sense_ids:
                examples[sense_id].append(example)
    else:
        examples = {}

    return entries, senses, examples


def _form(parent, lang, text):
    xml_form = ET.SubElement(parent, 'form', lang=lang)
    xml_text = ET.SubElement(xml_form, 'text')
    xml_text.text = text
    return xml_text


def make_lift(
    entries, senses, examples,
    language, metalanguage, alt_language_1, alt_language_2,
    sn_alttrans_col1, ex_alttrans_col1,
    sn_alttrans_col2, ex_alttrans_col2,
    variant_col
):
    lift = ET.Element('lift', lang=language)
    for entry in entries:
        entry_id = entry.get(CLDF_ID)
        lx = entry.get(CLDF_HEADWORD)
        ps = entry.get(CLDF_POS)
        xml_entry = ET.SubElement(lift, 'entry', id=entry_id)
        xml_lexunit = ET.SubElement(xml_entry, 'lexical-unit')
        _form(xml_lexunit, language, lx)

        for sense in senses[entry_id]:
            sense_id = sense[CLDF_ID]
            de = sense[CLDF_DESC]
            xml_sense_id = '{}-{}'.format(entry_id, sense_id)
            xml_sense = ET.SubElement(xml_entry, 'sense', id=xml_sense_id)
            if ps:
                ET.SubElement(xml_sense, 'grammatical-info', type=ps)
            xml_de = ET.SubElement(xml_sense, 'definition')
            _form(xml_de, metalanguage, de)
            if alt_language_1 and sense.get(sn_alttrans_col1):
                _form(xml_de, alt_language_1, sense[sn_alttrans_col1])
            if alt_language_2 and sense.get(sn_alttrans_col2):
                _form(xml_de, alt_language_2, sense[sn_alttrans_col2])

            for example in (examples.get(sense_id) or ()):
                xv = example[CLDF_PRIMARY]
                xml_ex = ET.SubElement(xml_sense, 'example')
                _form(xml_ex, language, xv)

                # TODO glosses?
                xe = example.get(CLDF_TRANS)
                if xe:
                    xml_xe = ET.SubElement(xml_ex, 'translation')
                    _form(xml_xe, metalanguage, xe)
                    if alt_language_1 and example.get(ex_alttrans_col1):
                        _form(xml_xe, alt_language_1, example[ex_alttrans_col1])
                    if alt_language_2 and example.get(ex_alttrans_col2):
                        _form(xml_xe, alt_language_2, example[ex_alttrans_col2])

        va = entry.get(variant_col)
        if va:
            xml_va = ET.SubElement(xml_entry, 'variant')
            _form(xml_va, language, va)

    return ET.ElementTree(lift)


def cldf2lift(
    cldf,
    language, metalanguage, alt_language_1, alt_language_2,
    sn_alttrans_col1, ex_alttrans_col1,
    sn_alttrans_col2, ex_alttrans_col2,
    variant_col, sense_id_col
):
    if not alt_language_1:
        sn_alttrans_col1 = None
        ex_alttrans_col1 = None
    if not alt_language_2:
        sn_alttrans_col2 = None
        sn_alttrans_col2 = None

    entries, senses, examples = extract_cldf_data(
        cldf,
        sn_alttrans_col1, ex_alttrans_col1,
        sn_alttrans_col2, ex_alttrans_col2,
        variant_col, sense_id_col)
    lift = make_lift(
        entries, senses, examples,
        language, metalanguage, alt_language_1, alt_language_2,
        sn_alttrans_col1, ex_alttrans_col1,
        sn_alttrans_col2, ex_alttrans_col2,
        variant_col)
    return lift
