#!/usr/bin/env python3

import sys
from xml.etree import ElementTree as ET

from pycldf import Dataset


def main():
    cldf = Dataset.from_metadata('tests/test_data/Dictionary-metadata.json')
    # TODO add proper 'lang' attribute (wants two-letter isocode?)
    lang = 'und-Latn'

    lift = ET.Element('lift', attrib={'lang': lang})
    for entry in cldf['EntryTable']:
        id_ = entry.get('ID')
        lx = entry.get('Headword')
        ps = entry.get('Part_Of_Speech')
        # TODO proper error handling
        assert id_ and lx, 'invalid entry'
        xml_entry = ET.SubElement(lift, 'entry', attrib={'id': id_})
        xml_lexunit = ET.SubElement(xml_entry, 'lexical-unit')
        ET.SubElement(xml_lexunit, 'form', text=lx, attrib={'lang': lang})

    print(str(
        ET.tostring(lift, encoding='UTF-8', xml_declaration=True),
        encoding='utf-8'))


if __name__ == '__main__':
    main()
