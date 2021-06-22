"""Unittests for gray.utils.args."""

import pathlib
import unittest
from unittest import mock
import gray.formatters as formatters
import gray.utils.args as utils_args


class TestArgs(unittest.TestCase):
    """Test the args module."""

    def test_parse_formatters_empty(self):
        self.assertEqual([], utils_args.parse_formatters(""))
        self.assertEqual([], utils_args.parse_formatters(" ,, "))

    def test_parse_formatters_success(self):
        expected = ['isort', 'unify']
        received = utils_args.parse_formatters("isort,unify")
        self.assertEqual(expected, received)
        received = utils_args.parse_formatters("isort, unify,")
        self.assertEqual(expected, received)

    def test_parse_formatters_error(self):
        with self.assertRaises(ValueError):
            utils_args.parse_formatters("fake_formatter")

    def test_parse_bool_true(self):
        cases = (True, "YES", "TRUE", "T", "Y", "1")
        for case in cases:
            with self.subTest(case):
                self.assertIs(True, utils_args.parse_bool(case))

    def test_parse_bool_false(self):
        cases = (False, "NO", "FALSE", "F", "N", "0")
        for case in cases:
            with self.subTest(case):
                self.assertIs(False, utils_args.parse_bool(case))

    def test_parse_frozenset_empty(self):
        self.assertEqual(frozenset(), utils_args.parse_frozenset(""))
        self.assertEqual(frozenset(), utils_args.parse_frozenset(" ,, "))

    def test_parse_frozenset_success(self):
        self.assertEqual(
            frozenset({'bar', 'foo'}), utils_args.parse_frozenset("foo,bar"))
        self.assertEqual(
            frozenset({'bar', 'foo'}), utils_args.parse_frozenset(" foo,, bar"))