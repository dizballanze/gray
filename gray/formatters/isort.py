"""Handle the isort formatter."""

from pathlib import Path

from configargparse import Namespace
from isort.api import sort_file

from gray.formatters.base import BaseFormatter


class SortImportsFormatter(BaseFormatter):
    """Sort imports through isort."""

    def __init__(self, arguments: Namespace):
        self._settings = {
            "quiet": False,
            "verbose": False,
            "sections": [
                "FUTURE", "STDLIB", "THIRDPARTY", "FIRSTPARTY", "LOCALFOLDER",
            ],
            "line_length": arguments.isort_line_length,
            "indent": "    ",
            "multi_line_output": arguments.isort_multi_line_output,
            "length_sort": arguments.isort_length_sort,
            "default_section": "THIRDPARTY",
            "virtual_env": str(arguments.isort_virtual_env),
            "include_trailing_comma": arguments.isort_include_trailing_comma,
            "lines_after_imports": arguments.isort_lines_after_imports,
            "use_parentheses": arguments.isort_use_parentheses,
        }
        # We do not override further isort defaults here.
        if arguments.isort_profile:
            self._settings["profile"] = arguments.isort_profile
        if arguments.isort_wrap_length:
            self._settings["wrap_length"] = arguments.isort_wrap_length
        if arguments.isort_known_third_party:
            self._settings["known_third_party"] = (
                arguments.isort_known_third_party
            )
        if arguments.isort_known_first_party:
            self._settings["known_first_party"] = (
                arguments.isort_known_first_party
            )
        if arguments.isort_known_local_folder:
            self._settings["known_local_folder"] = (
                arguments.isort_known_local_folder
            )
        if arguments.isort_skip_gitignore:
            self._settings["skip_gitignore"] = arguments.isort_skip_gitignore
        if arguments.isort_add_imports:
            self._settings["add_imports"] = arguments.isort_add_imports
        if arguments.isort_remove_imports:
            self._settings["remove_imports"] = arguments.isort_remove_imports

    def process(self, file_path: Path):
        """Process the given file through isort."""
        sort_file(
            filename=str(file_path),
            **self._settings,
        )
