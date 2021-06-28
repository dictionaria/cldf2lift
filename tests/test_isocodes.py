import pytest
import cldf2lift


def test_convert_three_letter_isocode_to_two_letters():
    assert cldf2lift.iso3_to_iso2('eng') == 'en'


def test_keep_three_letter_isocode_if_there_is_no_two_letter_code():
    assert cldf2lift.iso3_to_iso2('www') == 'www'


def test_keep_unkown_isocodes_intact():
    assert cldf2lift.iso3_to_iso2('xxxx') == 'xxxx'


def test_there_might_be_null_pointers():
    assert cldf2lift.iso3_to_iso2(None) is None
