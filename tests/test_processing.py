"""Unittests for gray.processing."""

import pathlib
import re
import unittest

from gray import main
from gray import processing


class TestCompilePatterns(unittest.TestCase):

    def test_no_patterns(self):
        self.assertEqual([], processing._compile_patterns('', None))

    def test_valid_res(self):
        self.assertEqual([re.compile('.'), re.compile('x')], processing._compile_patterns('.', 'x'))

    def test_invalid_re(self):
        with self.assertRaises(processing.ConfigurationError):
            processing._compile_patterns('(?:', None)


class TestIsExcluded(unittest.TestCase):

    def test_is_excluded(self):
        default_excludes = re.compile(main.DEFAULT_EXCLUDES)
        cases = (
            ('no exclude', pathlib.PurePosixPath('.git'), [], False),
            ('.git exclude', pathlib.PurePosixPath('.git'), [default_excludes], True),
            ('subdir exclude', pathlib.PurePosixPath('sub/dir/.git'), [default_excludes], True),
            ('windows include', pathlib.PureWindowsPath(r'windows\foo'), [default_excludes], False),
            ('windows exclude', pathlib.PureWindowsPath(r'windows\.git'), [default_excludes], True),
        )
        for name, path, excludes, expected in cases:
            with self.subTest(name=name):
                self.assertIs(expected, processing._is_excluded(path, excludes))
