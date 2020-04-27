import logging
from multiprocessing import Process, Queue
from pathlib import Path
from typing import Iterator, Sequence

from configargparse import Namespace

from gray.formatters import FORMATTERS, BaseFormatter, CompositeFormatter


log = logging.getLogger(__name__)


class FormattingError(Exception):
    exit_code = 1


def is_venv(path: Path):
   return all((
       (path / "bin" / "python").exists(),
       (path / "pyvenv.cfg").is_file(),
   ))


def gen_filepaths(
        paths: Sequence[Path],
        process_venv: bool = True,
) -> Iterator[Path]:
    for path in paths:
        if path.is_file() and (path.suffix == ".py"):
            yield path
        elif path.is_dir():
            if is_venv(path) and not process_venv:
                log.warning(
                    "%s looks like virtualenv directory. Skipping... ", path,
                )
                log.warning("Use --do-not-detect-venv flag to turn this off")
                continue
            yield from path.glob("**/*.py")
        else:
            log.debug("Skipping %r", path)


def fade_file(file_path: Path, formatter: BaseFormatter):
    log.debug("Going to process file %s", file_path)
    formatter.process(file_path)
    log.info("\"%s\" file was processed", file_path)


def worker(tasks: Queue, result: Queue, formatter: BaseFormatter):
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


def process(arguments: Namespace):
    tasks = Queue()
    results = Queue()
    formatter = CompositeFormatter(
        *[FORMATTERS[k](arguments) for k in arguments.formatters],
    )

    processes = []
    for _ in range(arguments.pool_size):
        prc = Process(target=worker, args=(tasks, results, formatter))
        processes.append(prc)
        prc.start()

    tasks_map = set()
    for fname in gen_filepaths(arguments.paths, arguments.do_not_detect_venv):
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
