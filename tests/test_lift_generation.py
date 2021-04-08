import cldf2lift

import pathlib
from xml.etree import ElementTree as ET

import pycldf
import pytest


@pytest.fixture
def testdata_dir():
    return pathlib.Path(__file__).parent / 'test_data'


def test_main(testdata_dir):
    cldf = pycldf.Dictionary.from_metadata(
        testdata_dir / 'Dictionary-metadata.json')
    lift = cldf2lift.cldf2lift(
        cldf,
        'und', 'en', 'es', 'de',
        'alt_translation1', 'alt_translation1',
        'alt_translation2', 'alt_translation2',
        'Variant_Form', 'Sense_IDs')

    lift_str = ET.tostring(lift.getroot(), encoding='unicode')
    with open(testdata_dir / 'lift-export.lift', encoding='utf-8') as f:
        expected = f.read()
    assert lift_str == expected
