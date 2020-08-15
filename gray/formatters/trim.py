from argparse import Namespace
from pathlib import Path

from trim import trim_file

from gray.formatters.base import BaseFormatter


class TrimFormatter(BaseFormatter):

    def __init__(self, arguments: Namespace):
        self._trim_leading_newlines = arguments.trim_leading_newlines

    def process(self, file_path: Path):
        trim_file(file_path, leading=self._trim_leading_newlines)
