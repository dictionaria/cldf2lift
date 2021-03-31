#!/usr/bin/env python3

import sys
from xml.etree import ElementTree as ET

from pycldf import Dataset


def main():
    cldf = Dataset.from_metadata('tests/test_data/Dictionary-metadata.json')
    lift = ET.Element('lift')
    print(str(ET.tostring(
        lift,
        encoding='UTF-8',
        xml_declaration=True), encoding='utf-8'))


if __name__ == '__main__':
    main()
