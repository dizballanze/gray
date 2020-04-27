from argparse import Namespace
from pathlib import Path

from add_trailing_comma import fix_file
from configargparse import Namespace

from gray.formatters.base import BaseFormatter


class AddTrailingCommaFormatter(BaseFormatter):

    def __init__(self, arguments: Namespace):
        min_version = arguments.min_python_version
        self._args = Namespace(
            py35_plus=(min_version >= (3, 5)),
            py36_plus=(min_version >= (3, 6)),
            exit_zero_even_if_changed=True,
        )

    def process(self, file_path: Path):
        fix_file(str(file_path), self._args)
