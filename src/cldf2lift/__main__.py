#!/usr/bin/env python3


from xml.etree import ElementTree as ET

from pycldf import Dataset


def main():
    cldf = Dataset.from_metadata('tests/test_data/Dictionary-metadata.json')
    lift = ET.Element('lift')
    print(ET.tostring(lift))


if __name__ == '__main__':
    main()
