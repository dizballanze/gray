from argparse import Namespace
from pathlib import Path

from pyupgrade import _fix_file

from gray.formatters.base import BaseFormatter


class PyUpgradeFormatter(BaseFormatter):

    def process(self, file_path: Path):
        args = Namespace(
            min_version=(3, 7),
            keep_percent_format=False,
            exit_zero_even_if_changed=True,
        )
        _fix_file(str(file_path), args)
