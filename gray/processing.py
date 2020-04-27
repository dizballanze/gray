import logging
from multiprocessing import Process, Queue
from pathlib import Path
from typing import Iterator, Sequence

from configargparse import Namespace

from gray.formatters import FORMATTERS, BaseFormatter, CompositeFormatter


log = logging.getLogger(__name__)


class FormattingError(Exception):
    pass


def gen_filepaths(paths: Sequence[Path]) -> Iterator[Path]:
    for path in paths:
        if path.is_file() and (path.suffix == ".py"):
            yield path
        elif path.is_dir():
            yield from path.glob("**/*.py")
        else:
            log.debug("Skipping %r", path)


def fade_file(file_path: Path, formatter: BaseFormatter):
    log.info("Going to process file %s", file_path)
    formatter.process(file_path)
    log.info("%s file was processed", file_path)


def worker(tasks: Queue, result: Queue, formatter: BaseFormatter):
    fname = tasks.get()

    while fname is not None:
        err = None
        try:
            fade_file(fname, formatter)
        except Exception as e:
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
    for fname in gen_filepaths(arguments.paths):
        tasks_map.add(fname)
        tasks.put_nowait(fname)

    failed = False

    try:
        while tasks_map:
            fname, exc = results.get()

            if exc:
                failed = True
                log.error("Error when processing file %r: %r", fname, exc)

            tasks_map.remove(fname)

        if failed:
            raise FormattingError(
                "Formatting failed please check previous errors",
            )
    finally:
        for _ in range(arguments.pool_size):
            tasks.put(None)

        for process in processes:
            process.join()
