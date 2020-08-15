from argparse import Namespace
from pathlib import Path

from configargparse import Namespace
from pyupgrade import _fix_file

from gray.formatters.base import BaseFormatter


class PyUpgradeFormatter(BaseFormatter):

    def __init__(self, arguments: Namespace):
        min_version = arguments.min_python_version

        if min_version < (3, 6):
            min_version = (3,)

        if min_version > (3, 7):
            min_version = (3, 7)

        self._args = Namespace(
            min_version=min_version,
            keep_percent_format=arguments.pyupgrade_keep_percent_format,
            exit_zero_even_if_changed=True,
        )

    def process(self, file_path: Path):
        _fix_file(str(file_path), self._args)
