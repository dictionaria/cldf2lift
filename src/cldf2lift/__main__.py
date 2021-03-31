#!/usr/bin/env python3

from collections import OrderedDict
from xml.etree import ElementTree as ET

from pycldf import Dataset


def form(parent, lang, text):
    xml_form = ET.SubElement(parent, 'form', lang=lang)
    xml_text = ET.SubElement(xml_form, 'text')
    xml_text.text = text
    return xml_text


def main():

    # load cldf data

    cldf = Dataset.from_metadata('tests/test_data/Dictionary-metadata.json')
    # TODO add proper 'lang' attribute (wants two-letter isocode?)
    lang = 'und-Latn'

    entries = cldf['EntryTable']
    senses = OrderedDict()
    for sense in cldf['SenseTable']:
        entry_id = sense.get('Entry_ID')
        # TODO proper error handling
        assert entry_id, 'invalid sense'
        assert sense.get('ID') and sense.get('Description'), 'invalid sense'
        if entry_id not in senses:
            senses[entry_id] = []
        senses[entry_id].append(sense)

    # generate lift xml

    lift = ET.Element('lift', lang=lang)
    for entry in entries:
        entry_id = entry.get('ID')
        lx = entry.get('Headword')
        ps = entry.get('Part_Of_Speech')
        # TODO proper error handling
        assert entry_id and lx, 'invalid entry'
        xml_entry = ET.SubElement(lift, 'entry', id=entry_id)
        xml_lexunit = ET.SubElement(xml_entry, 'lexical-unit')
        form(xml_lexunit, lang, lx)

        for sense in senses[entry_id]:
            sense_id = sense['ID']
            de = sense['Description']
            xml_sense_id = '{}-{}'.format(entry_id, sense_id)
            xml_sense = ET.SubElement(xml_entry, 'sense', id=xml_sense_id)
            ET.SubElement(xml_sense, 'grammatical-info', type=ps)
            xml_de = ET.SubElement(xml_sense, 'definition')
            form(xml_de, 'en', de)

        va = entry.get('Variant_Form')
        if va:
            xml_va = ET.SubElement(xml_entry, 'variant')
            form(xml_va, lang, va)

    print(str(
        ET.tostring(lift, encoding='UTF-8', xml_declaration=True),
        encoding='utf-8'))


if __name__ == '__main__':
    main()
