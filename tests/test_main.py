"""Unittests for gray.main."""

import pathlib
import unittest

from gray import main


class TestGetParser(unittest.TestCase):

    def test_defaults(self):
        parser = main.get_parser()
        arguments = parser.parse_args([])
        self.assertEqual((pathlib.PosixPath('.'),), arguments.paths)
        self.assertEqual(main.DEFAULT_EXCLUDES, arguments.exclude)
        self.assertIsNone(arguments.extend_exclude)
        self.assertEqual(8, arguments.pool_size)
        self.assertFalse(arguments.do_not_detect_venv)

