from argparse import Namespace
from pathlib import Path

from unify import format_file

from gray.formatters.base import BaseFormatter


class UnifyFormatter(BaseFormatter):

    def process(self, file_path: Path):
        args = Namespace(
            in_place=True,
            quote='"',
        )
        format_file(str(file_path), args, None)
