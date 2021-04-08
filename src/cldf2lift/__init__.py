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
    'Variant_Form',
]
SENSE_COLS = [
    CLDF_ID,
    CLDF_DESC,
    CLDF_ENTRY_ID,
    'alt_translation1',
    'alt_translation2',
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
    'Sense_IDs',
    'alt_translation1',
    'alt_translation2',
]


def extract_cldf_data(cldf):
    senses = defaultdict(list)
    for sense in cldf.iter_rows('SenseTable', *SENSE_COLS):
        entry_id = sense.get(CLDF_ENTRY_ID)
        # TODO proper error handling
        assert entry_id, 'invalid sense'
        assert sense.get(CLDF_ID), 'invalid sense'
        assert sense.get(CLDF_DESC), 'invalid sense'
        senses[entry_id].append(sense)

    entries = [
        e
        for e in cldf.iter_rows('EntryTable', *ENTRY_COLS)
        if e.get(CLDF_ID) in senses]

    examples = defaultdict(list)
    for example in cldf.iter_rows('ExampleTable', *EXAMPLE_COLS):
        # TODO proper error handling
        assert example.get(CLDF_ID), 'invalid example'
        assert example.get(CLDF_PRIMARY), 'invalid example'
        sense_ids = example.get('Sense_IDs')
        for sense_id in sense_ids:
            examples[sense_id].append(example)

    return entries, senses, examples


def _form(parent, lang, text):
    xml_form = ET.SubElement(parent, 'form', lang=lang)
    xml_text = ET.SubElement(xml_form, 'text')
    xml_text.text = text
    return xml_text


def make_lift(
    entries, senses, examples,
    language, metalanguage, alt_language_1, alt_language_2
):
    lift = ET.Element('lift', lang=language)
    for entry in entries:
        entry_id = entry.get(CLDF_ID)
        lx = entry.get(CLDF_HEADWORD)
        ps = entry.get(CLDF_POS)
        # TODO proper error handling
        assert entry_id and lx, 'invalid entry'
        xml_entry = ET.SubElement(lift, 'entry', id=entry_id)
        xml_lexunit = ET.SubElement(xml_entry, 'lexical-unit')
        _form(xml_lexunit, language, lx)

        for sense in senses[entry_id]:
            sense_id = sense[CLDF_ID]
            de = sense[CLDF_DESC]
            xml_sense_id = '{}-{}'.format(entry_id, sense_id)
            xml_sense = ET.SubElement(xml_entry, 'sense', id=xml_sense_id)
            ET.SubElement(xml_sense, 'grammatical-info', type=ps)
            xml_de = ET.SubElement(xml_sense, 'definition')
            _form(xml_de, metalanguage, de)
            if alt_language_1 and sense.get('alt_translation1'):
                _form(xml_de, alt_language_1, sense['alt_translation1'])
            if alt_language_2 and sense.get('alt_translation2'):
                _form(xml_de, alt_language_2, sense['alt_translation2'])

            for example in (examples.get(sense_id) or ()):
                xv = example[CLDF_PRIMARY]
                xml_ex = ET.SubElement(xml_sense, 'example')
                _form(xml_ex, language, xv)

                # TODO glosses?
                xe = example.get(CLDF_TRANS)
                if xe:
                    xml_xe = ET.SubElement(xml_ex, 'translation')
                    _form(xml_xe, metalanguage, xe)
                    if alt_language_1 and example.get('alt_translation1'):
                        _form(xml_xe, alt_language_1, example['alt_translation1'])
                    if alt_language_2 and example.get('alt_translation2'):
                        _form(xml_xe, alt_language_2, example['alt_translation2'])

        va = entry.get('Variant_Form')
        if va:
            xml_va = ET.SubElement(xml_entry, 'variant')
            _form(xml_va, language, va)

    return ET.ElementTree(lift)
