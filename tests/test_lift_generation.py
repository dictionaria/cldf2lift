import cldf2lift

from io import StringIO
import pathlib
import shlex
from xml.etree import ElementTree as ET

from cldf2lift.__main__ import _main as cli_main
from cldfbench.__main__ import main as bench_main
import pycldf
import pytest


def _bench_main(cmd, **kw):
    bench_main(['--no-config'] + shlex.split(cmd), **kw)


@pytest.fixture
def testbench_dir():
    return pathlib.Path(__file__).parent / 'test_bench'


def test_main(testbench_dir):
    cldf = pycldf.Dictionary.from_metadata(
        testbench_dir / 'cldf' / 'Dictionary-metadata.json')
    lift = cldf2lift.cldf2lift(
        cldf,
        'und', 'en', 'es', 'de',
        'alt_translation1', 'alt_translation1',
        'alt_translation2', 'alt_translation2',
        'Variant_Form', 'Sense_IDs')

    # FIXME just testing the whole string output lacks finesse…
    lift_str = ET.tostring(lift.getroot(), encoding='unicode')
    with open(testbench_dir / 'lift-export.lift', encoding='utf-8') as f:
        expected = f.read()
    assert lift_str == expected


def test_cli(testbench_dir, tmp_path):
    cldf_file = testbench_dir / 'cldf' / 'Dictionary-metadata.json'
    lift_file = tmp_path / 'export.lift'
    cli_main([str(cldf_file), '-o', str(lift_file)])
    assert lift_file.exists()


def test_bench(testbench_dir, tmp_path):
    bench_file = testbench_dir / 'cldfbench_test_bench.py'
    lift_file = tmp_path / 'export.lift'
    _bench_main("lift.lift -o '{}' '{}'".format(lift_file, bench_file))
    assert lift_file.exists()
