from argparse import Namespace
from pathlib import Path

from add_trailing_comma import fix_file

from gray.formatters.base import BaseFormatter


class AddTrailingCommaFormatter(BaseFormatter):

    def process(self, file_path: Path):
        args = Namespace(
            py35_plus=True,
            py36_plus=True,
            exit_zero_even_if_changed=True,
        )
        fix_file(str(file_path), args)
