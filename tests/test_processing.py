"""Unittests for gray.processing."""

import pathlib
import re

import pytest

from gray import main, processing


class TestCompilePatterns:

    def test_no_patterns(self):
        assert processing._compile_patterns('', None) == []

    def test_valid_res(self):
        assert processing._compile_patterns('.', 'x') == [re.compile('.'), re.compile('x')]

    def test_invalid_re(self):
        with pytest.raises(processing.ConfigurationError):
            processing._compile_patterns('(?:', None)


def test_is_excluded(subtests):
    default_excludes = re.compile(main.DEFAULT_EXCLUDES)
    cases = (
        ('no exclude', pathlib.PurePosixPath('.git'), [], False),
        ('.git exclude', pathlib.PurePosixPath('.git'), [default_excludes], True),
        ('subdir exclude', pathlib.PurePosixPath('sub/dir/.git'), [default_excludes], True),
        ('windows include', pathlib.PureWindowsPath(r'windows\foo'), [default_excludes], False),
        ('windows exclude', pathlib.PureWindowsPath(r'windows\.git'), [default_excludes], True),
    )
    for name, path, excludes, expected in cases:
        with subtests.test(name=name):
            assert processing._is_excluded(path, excludes) is expected
