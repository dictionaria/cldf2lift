#!/usr/bin/env python3

from collections import OrderedDict
from xml.etree import ElementTree as ET

from pycldf import Dataset


def main():
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

    lift = ET.Element('lift', attrib={'lang': lang})
    for entry in entries:
        entry_id = entry.get('ID')
        lx = entry.get('Headword')
        ps = entry.get('Part_Of_Speech')
        # TODO proper error handling
        assert entry_id and lx, 'invalid entry'
        xml_entry = ET.SubElement(lift, 'entry', attrib={'id': entry_id})
        xml_lexunit = ET.SubElement(xml_entry, 'lexical-unit')
        xml_form = ET.SubElement(xml_lexunit, 'form', attrib={'lang': lang})
        xml_text = ET.SubElement(xml_form, 'text')
        xml_text.text = lx

        for sense in senses[entry_id]:
            sense_id = sense['ID']
            de = sense['Description']
            xml_sense_id = '{}-{}'.format(entry_id, sense_id)
            xml_sense = ET.SubElement(
                xml_entry, 'sense', attrib={'id': xml_sense_id})
            ET.SubElement(xml_sense, 'grammatical-info', attrib={'type': ps})
            xml_de = ET.SubElement(xml_sense, 'definition')
            xml_de_form = ET.SubElement(xml_de, 'form', attrib={'lang': 'en'})
            xml_de_text = ET.SubElement(xml_de_form, 'text')
            xml_de_text.text = de

    print(str(
        ET.tostring(lift, encoding='UTF-8', xml_declaration=True),
        encoding='utf-8'))


if __name__ == '__main__':
    main()
