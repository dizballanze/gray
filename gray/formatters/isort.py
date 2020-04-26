from pathlib import Path

from configargparse import Namespace
from isort import SortImports

from gray.formatters.base import BaseFormatter


class SortImportsFormatter(BaseFormatter):

    def __init__(self, arguments: Namespace):
        self._settings = {
            "quiet": False,
            "verbose": False,
            "check": False,
            "sections": [
                "FUTURE", "STDLIB", "THIRDPARTY", "FIRSTPARTY", "LOCALFOLDER",
            ],
            "line_length": arguments.isort_line_length,
            "indent": "    ",
            "multi_line_output": 5,
            "length_sort": 0,
            "default_section": "FIRSTPARTY",
            "virtual_env": str(arguments.isort_virtual_env),
            "include_trailing_comma": arguments.isort_include_trailing_comma,
            "lines_after_imports": arguments.isort_lines_after_imports,
        }

    def process(self, file_path: Path):
        SortImports(
            file_path=str(file_path),
            **self._settings,
        )
