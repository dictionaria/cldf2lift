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
    entries, senses, examples = cldf2lift.extract_cldf_data(cldf)
    lift = cldf2lift.make_lift(
        entries, senses, examples,
        'und', 'en', 'es', 'de')

    lift_str = ET.tostring(lift.getroot(), encoding='unicode')
    with open(testdata_dir / 'lift-export.lift', encoding='utf-8') as f:
        expected = f.read()
    assert lift_str == expected
