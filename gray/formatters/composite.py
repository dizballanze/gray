from pathlib import Path

from gray.formatters.base import BaseFormatter


class CompositeFormatter(BaseFormatter):
    # Use a list to guarantee order preserving, which can be important to
    # ensure that the formatters are going to behave consistently.
    _formatters: list

    def __init__(self, *formatters):
        self._formatters = list(formatters)

    def process(self, file_path: Path):
        for formatter in self._formatters:
            formatter.process(file_path)
