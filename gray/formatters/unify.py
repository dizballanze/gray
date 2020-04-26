from argparse import Namespace
from pathlib import Path

from configargparse import Namespace
from unify import format_file

from gray.formatters.base import BaseFormatter


class UnifyFormatter(BaseFormatter):

    _quote: str

    def __init__(self, arguments: Namespace):
        self._args = Namespace(
            in_place=True,
            quote=arguments.unify_quote,
        )

    def process(self, file_path: Path):
        format_file(str(file_path), self._args, None)
