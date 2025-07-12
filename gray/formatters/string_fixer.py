from argparse import Namespace
from pathlib import Path
from typing import cast

from configargparse import Namespace
from string_fixer import Config, process_file

from gray.formatters.base import BaseFormatter


class StringFixerFormatter(BaseFormatter):

    _quote: str

    def __init__(self, arguments: Namespace):
        self._config = cast(
            Config, {
                "target": Path("./"),
                "dry_run": False,
                "output": None,
                "ignore": [],
                "include": None,
                "extends": None,
                "target_version": f"{arguments.min_python_version[0]}.{arguments.min_python_version[1]}",
                "prefer_least_escapes": True,
                "quote_style": arguments.string_fixer_quote,
            },
        )

    def process(self, file_path: Path):
        process_file(file_path, self._config, None)
