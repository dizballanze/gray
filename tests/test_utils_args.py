"""Unittests for gray.utils.args."""


import pytest

import gray.utils.args as utils_args


def test_parse_formatters_empty():
    assert utils_args.parse_formatters("") == []
    assert utils_args.parse_formatters(" ,, ") == []


def test_parse_formatters_success():
    expected = ["isort", "string_fixer"]
    assert utils_args.parse_formatters("isort,string_fixer") == expected
    assert utils_args.parse_formatters("isort, string_fixer,") == expected


def test_parse_formatters_error():
    with pytest.raises(ValueError):
        utils_args.parse_formatters("fake_formatter")


def test_parse_bool_true(subtests):
    cases = (True, "YES", "TRUE", "T", "Y", "1")
    for case in cases:
        with subtests.test(case):
            assert utils_args.parse_bool(case)


def test_parse_bool_false(subtests):
    cases = (False, "NO", "FALSE", "F", "N", "0")
    for case in cases:
        with subtests.test(case):
            assert not utils_args.parse_bool(case)


def test_parse_frozenset_empty():
    assert utils_args.parse_frozenset("") == frozenset()
    assert utils_args.parse_frozenset(" ,, ") == frozenset()


def test_parse_frozenset_success():
    expected = frozenset({"bar", "foo"})
    assert utils_args.parse_frozenset("foo,bar") == expected
    assert utils_args.parse_frozenset(" foo,, bar") == expected
