"""Black formatter for Gray."""

from argparse import Namespace
from pathlib import Path

import black
from configargparse import Namespace

from gray.formatters.base import BaseFormatter


class BlackFormatter(BaseFormatter):
    """Black formatter class."""

    def __init__(self, arguments: Namespace):
        self._args = Namespace(
            line_length=arguments.black_line_length,
            skip_magic_trailing_comma=arguments.black_skip_magic_trailing_comma,
            skip_string_normalization=arguments.black_skip_string_normalization,
        )
        self._mode = black.Mode(
            line_length=self._args.line_length,
            magic_trailing_comma=not self._args.skip_magic_trailing_comma,
            string_normalization=not self._args.skip_string_normalization,
        )

    def process(self, file_path: Path):
        # Black does not provide an official public API yet:
        # https://github.com/psf/black/issues/779
        black.reformat_one(
            file_path,
            fast=False,
            write_back=black.WriteBack.YES,
            mode=self._mode,
            report=black.Report(),
        )
