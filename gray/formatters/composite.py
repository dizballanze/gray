from pathlib import Path

from gray.formatters.base import BaseFormatter


class CompositeFormatter(BaseFormatter):
    # Use a list to guarantee order preserving, which can be important to
    # ensure that the formatters are going to behave consistently.
    _formatters: tuple

    def __init__(self, *formatters):
        self._formatters = tuple(formatters)

    def process(self, file_path: Path):
        for formatter in self._formatters:
            formatter.process(file_path)
