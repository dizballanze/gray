from pathlib import Path

from isort import SortImports

from gray.formatters.base import BaseFormatter


class SortImportsFormatter(BaseFormatter):

    def process(self, file_path: Path):
        settings = {
            "quite": True,
            "check": False,
            "sections": [
                "FUTURE", "STDLIB", "THIRDPARTY", "FIRSTPARTY", "LOCALFOLDER",
            ],
            "line_length": 80,
            "indent": "    ",
            "multi_line_output": 5,
            "length_sort": 0,
            "default_section": "FIRSTPARTY",
            "virtual_env": "env",
            "include_trailing_comma": 1,
            "lines_after_imports": 2,
        }
        SortImports(
            file_path=str(file_path),
            **settings,
        )
