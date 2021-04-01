from collections import defaultdict
from xml.etree import ElementTree as ET


def extract_cldf_data(cldf):
    senses = defaultdict(list)
    for sense in cldf['SenseTable']:
        entry_id = sense.get('Entry_ID')
        # TODO proper error handling
        assert entry_id, 'invalid sense'
        assert sense.get('ID') and sense.get('Description'), 'invalid sense'
        senses[entry_id].append(sense)

    entries = [e for e in cldf['EntryTable'] if e.get('ID') in senses]

    examples = defaultdict(list)
    for example in cldf['ExampleTable']:
        # TODO proper error handling
        assert example.get('ID'), 'invalid example'
        assert example.get('Primary_Text'), 'invalid example'
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
        entry_id = entry.get('ID')
        lx = entry.get('Headword')
        ps = entry.get('Part_Of_Speech')
        # TODO proper error handling
        assert entry_id and lx, 'invalid entry'
        xml_entry = ET.SubElement(lift, 'entry', id=entry_id)
        xml_lexunit = ET.SubElement(xml_entry, 'lexical-unit')
        _form(xml_lexunit, language, lx)

        for sense in senses[entry_id]:
            sense_id = sense['ID']
            de = sense['Description']
            xml_sense_id = '{}-{}'.format(entry_id, sense_id)
            xml_sense = ET.SubElement(xml_entry, 'sense', id=xml_sense_id)
            ET.SubElement(xml_sense, 'grammatical-info', type=ps)
            xml_de = ET.SubElement(xml_sense, 'definition')
            _form(xml_de, metalanguage, de)

            for example in (examples.get(sense_id) or ()):
                xv = example['Primary_Text']
                xml_ex = ET.SubElement(xml_sense, 'example')
                _form(xml_ex, language, xv)

                # TODO alt_translation{1,2}
                # TODO glosses?
                xe = example.get('Translated_Text')
                if xe:
                    xml_xe = ET.SubElement(xml_ex, 'translation')
                    _form(xml_xe, metalanguage, xe)

        va = entry.get('Variant_Form')
        if va:
            xml_va = ET.SubElement(xml_entry, 'variant')
            _form(xml_va, language, va)

    return ET.ElementTree(lift)
