import cldf2lift

import pathlib
import shlex
from xml.etree import ElementTree as ET


from cldfbench.__main__ import main as bench_main
import pycldf
import pytest


def _bench_main(cmd, **kw):
    bench_main(['--no-config'] + shlex.split(cmd), **kw)


@pytest.fixture
def testdata_dir():
    return pathlib.Path(__file__).parent / 'test_bench'


def test_main(testdata_dir):
    cldf = pycldf.Dictionary.from_metadata(
        testdata_dir / 'cldf' / 'Dictionary-metadata.json')
    lift = cldf2lift.cldf2lift(
        cldf,
        'und', 'en', 'es', 'de',
        'alt_translation1', 'alt_translation1',
        'alt_translation2', 'alt_translation2',
        'Variant_Form', 'Sense_IDs')

    # FIXME just testing the whole string output lacks finesse…
    lift_str = ET.tostring(lift.getroot(), encoding='unicode')
    with open(testdata_dir / 'lift-export.lift', encoding='utf-8') as f:
        expected = f.read()
    assert lift_str == expected


def test_bench(testdata_dir, tmp_path):
    bench_file = testdata_dir / 'cldfbench_test_bench.py'
    lift_file = tmp_path / 'export.lift'
    _bench_main(
        'lift.lift'
        ' --meta-language-2 es'
        ' --meta-language-3 de'
        " -o '{}' '{}'".format(lift_file, bench_file))
    assert lift_file.exists()
