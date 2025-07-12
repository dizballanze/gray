"""Main processing module for Gray."""

import logging
import re
from multiprocessing import Process, Queue
from pathlib import Path
from typing import Iterator, List, Optional, Sequence, Union

from configargparse import Namespace
from rich.logging import RichHandler

from gray.formatters import FORMATTERS, BaseFormatter, CompositeFormatter


log = logging.getLogger(__name__)


def log_config(level: Union[str, int]):
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)
    handler = RichHandler(rich_tracebacks=True)
    handler.setFormatter(logging.Formatter("%(message)s", datefmt="[%X]"))
    logging.basicConfig(level=level, handlers=[handler])


class GrayError(Exception):
    """Base Error class for Gray."""
    exit_code = 1


class ConfigurationError(GrayError):
    """Raised on a configuration error."""
    exit_code = 2


class FormattingError(GrayError):
    """Raised when a formatting error occured."""


def _compile_patterns(exclude: Optional[str], extend: Optional[str]) -> List[re.Pattern]:
    """Compiles the exclude patterns.

    Args:
        exclude: The default exclusion regex.
        extend: Additional regex to exclude.
    Returns:
        A list of regex patterns.
    Raises:
        ConfigurationError: The regex patterns cannot be compiled.
    """
    compiled: List[re.Pattern] = []
    try:
        for pattern in (exclude, extend):
            if pattern:
                compiled.append(re.compile(pattern))
    except re.error as error:
        raise ConfigurationError(f"Invalid regex passed for exclusion: {error}")
    return compiled


def _is_excluded(path: Path, excludes: Optional[Sequence[re.Pattern]]) -> bool:
    """Returns True if the given path is in the exclusion list.

    Windows paths are treated as posix path to ensure the same exclusion
    patterns can be used as on other Unix based OSes.

    Args:
        path: The path to the file or directory to check for exclusion.
        excludes: Optional list of exclusion patterns.
    Returns:
        True if the path matches .
    """
    if not excludes:
        return False
    posix_path = str(path.as_posix())
    return any(exclude.match(posix_path) for exclude in excludes)


def is_venv(path: Path):
    return all((
        (path / "bin" / "python").exists(),
        (path / "pyvenv.cfg").is_file(),
    ))


def gen_filepaths(
        paths: Sequence[Path],
        process_venv: bool = True,
        excludes: Optional[Sequence[re.Pattern]] = None,
) -> Iterator[Path]:
    """Generates the paths to the files to be formatted.

    Args:
          paths: Paths to glob from.
          process_venv: If False skipp virtualenv directories. Defaults is True.
          excludes: Optional regex patterns of files and directories to exclude.
    Yields:
        Paths to the files to be formatter.
    """
    for path in paths:
        if path.is_file() and (path.suffix == ".py"):
            if _is_excluded(path, excludes):
                log.debug("Excluding %s", path)
                continue
            yield path
        elif path.is_dir():
            if _is_excluded(path, excludes):
                log.debug("Excluding %s", path)
                continue
            if not process_venv and is_venv(path):
                log.warning(
                    "%s looks like virtualenv directory. Skipping... ", path,
                )
                log.warning("Use --do-not-detect-venv flag to turn this off")
                continue
            yield from gen_filepaths(path.glob("*"), process_venv=process_venv, excludes=excludes)
        else:
            log.debug("Skipping %s", path)


def fade_file(file_path: Path, formatter: BaseFormatter):
    log.debug("Going to process file %s", file_path)
    formatter.process(file_path)
    log.info("\"%s\" file was processed", file_path)


def worker(
    tasks: Queue, result: Queue,
    formatter: BaseFormatter, log_level: int,
):
    # Logs for separate process should be configured again
    log_config(log_level)

    fname = tasks.get()

    while fname is not None:
        err = None
        try:
            fade_file(fname, formatter)
        except Exception as e:
            log.exception("Failed to reformat file \"%s\"", fname)
            err = e

        result.put_nowait((fname, err))
        fname = tasks.get()


def process(arguments: Namespace) -> None:
    """Configures and runs the formatters.

    Args:
        arguments: The configuration arguments.
    """
    excludes: List[re.Pattern] = _compile_patterns(arguments.exclude, arguments.extend_exclude)
    tasks = Queue()
    results = Queue()
    formatter = CompositeFormatter(
        *[FORMATTERS[k](arguments) for k in arguments.formatters],
    )

    processes = []
    log_level = getattr(logging, arguments.log_level.upper(), logging.INFO)
    for _ in range(arguments.pool_size):
        prc = Process(target=worker, args=(tasks, results, formatter, log_level))
        processes.append(prc)
        prc.start()

    tasks_map = set()
    for fname in gen_filepaths(arguments.paths, arguments.do_not_detect_venv, excludes):
        tasks_map.add(fname)
        tasks.put_nowait(fname)

    failed = False
    wrong_files = []

    try:
        while tasks_map:
            fname, exc = results.get()

            if exc:
                failed = True
                wrong_files.append(fname)
            tasks_map.remove(fname)

        if failed:
            for fname in wrong_files:
                log.error("Failed when processing \"%s\"", fname)

            raise FormattingError(
                "Formatting failed please check previous errors", wrong_files,
            )
    finally:
        for _ in range(arguments.pool_size):
            tasks.put(None)

        for prc in processes:
            prc.join()
