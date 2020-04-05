import logging

from configargparse import Namespace
from pathlib import Path
from types import MappingProxyType
from typing import Sequence, Iterator

from gray.formatters.add_trailing_comma import AddTrailingCommaFormatter
from gray.formatters.base import BaseFormatter
from gray.formatters.composite import CompositeFormatter
from gray.formatters.isort import SortImportsFormatter
from gray.formatters.pyupgrade import PyUpgradeFormatter
from gray.formatters.unify import UnifyFormatter


log = logging.getLogger(__name__)

FORMATTERS = MappingProxyType({
    "add-trailing-comma": AddTrailingCommaFormatter,
    "isort": SortImportsFormatter,
    "pyupgrade": PyUpgradeFormatter,
    "unify": UnifyFormatter,
})


def gen_filepaths(paths: Sequence[Path]) -> Iterator[Path]:
    for path in paths:
        if path.is_file():
            yield path
        elif path.is_dir():
            for file_path in path.glob("**/*.py"):
                yield file_path


def process(arguments: Namespace):
    for path in gen_filepaths(arguments.paths):
        fade_file(path, arguments.formatters)


def fade_file(file_path: Path, formatter: BaseFormatter):
    log.info("Going to process file %s", file_path)
    formatter.process(file_path)
    log.info("%s file was processed", file_path)
