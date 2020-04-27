import subprocess
from pathlib import Path

from gray.main import parser
from gray.processing import process


ROOT_DIR_CMD = ("git", "rev-parse", "--show-toplevel")
DIFF_CACHED_CMD = ("git", "diff", "--cached", "--name-only")
DIFF_NOT_CACHED_CMD = ("git", "diff", "--name-only")
ADD_CMD = ("git", "add")


def git_pre_commit(stop_on_modify=True):
    """
    Git pre commit hook handler. Runs gray on modified files.
    Return exit code.

    If stop_on_modify is True, returns exit code 1 that lets you check
    modifications done by gray.
    Otherwise, all unstaged changes in processed files
    will be added to the index.
    """
    root_dir = Path(command_lines(ROOT_DIR_CMD)[0])
    staged_files = command_lines(DIFF_CACHED_CMD)
    if not staged_files:
        return 0

    staged_files_fullpath = [str(root_dir / f) for f in staged_files]
    arguments = parser.parse_args(args=" ".join(staged_files_fullpath))
    process(arguments)

    modified_files = command_lines(DIFF_NOT_CACHED_CMD)
    diff = set(staged_files) & set(modified_files)
    if not diff:
        return 0

    if stop_on_modify:
        print("*" * 40)
        print(
            "Gray formattter. "
            "There are unstaged changes in the following files:",
        )
        for f in diff:
            print(f)
        print("*" * 40)
        return 1

    command_lines(ADD_CMD + tuple(diff))
    return 0


def command_lines(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, check=False)
    output = result.stdout.decode()
    return [line.strip() for line in output.splitlines()]
