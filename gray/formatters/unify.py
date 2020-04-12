from argparse import Namespace
from pathlib import Path

from configargparse import Namespace
from unify import format_file

from gray.formatters.base import BaseFormatter


class UnifyFormatter(BaseFormatter):

    _quote: str

    def __init__(self, arguments: Namespace):
        self._quote = arguments.quote

    def process(self, file_path: Path):
        args = Namespace(
            in_place=True,
            quote=self._quote,
        )
        format_file(str(file_path), args, None)
