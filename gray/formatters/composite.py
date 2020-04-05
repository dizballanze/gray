from pathlib import Path

from gray.formatters.base import BaseFormatter


class CompositeFormatter(BaseFormatter):
    _formatters: frozenset

    def __init__(self, *formatters):
        self._formatters = frozenset(formatters)

    def process(self, file_path: Path):
        for formatter in self._formatters:
            formatter.process(file_path)
