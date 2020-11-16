from pathlib import Path

from configargparse import Namespace
from isort.api import sort_file

from gray.formatters.base import BaseFormatter


class SortImportsFormatter(BaseFormatter):

    def __init__(self, arguments: Namespace):
        self._settings = {
            "quiet": False,
            "verbose": False,
            "sections": [
                "FUTURE", "STDLIB", "THIRDPARTY", "FIRSTPARTY", "LOCALFOLDER",
            ],
            "line_length": arguments.isort_line_length,
            "indent": "    ",
            "multi_line_output": 5,
            "length_sort": 0,
            "default_section": "THIRDPARTY",
            "virtual_env": str(arguments.isort_virtual_env),
            "include_trailing_comma": arguments.isort_include_trailing_comma,
            "lines_after_imports": arguments.isort_lines_after_imports,
            "use_parentheses": True,
        }

    def process(self, file_path: Path):
        sort_file(
            filename=str(file_path),
            **self._settings,
        )
