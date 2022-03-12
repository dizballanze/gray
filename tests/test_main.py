"""Unittests for gray.main."""

import pathlib

from gray import main


def test_defaults():
    parser = main.get_parser()
    arguments = parser.parse_args([])
    assert (pathlib.PosixPath("."),) == arguments.paths
    assert main.DEFAULT_EXCLUDES == arguments.exclude
    assert arguments.extend_exclude is None
    assert arguments.pool_size == 8
    assert arguments.do_not_detect_venv is False
