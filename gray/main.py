"""Main module of gray."""

import argparse
import logging
import os
import sys
from pathlib import Path

import configargparse

from gray.formatters import FORMATTERS, OPTIONAL_FORMATTERS
from gray.processing import GrayError, log_config, process
from gray.utils.args import parse_bool, parse_formatters, parse_frozenset


FORMATTERS_NAMES = ",".join(
    x for x in sorted(FORMATTERS.keys()) if x not in OPTIONAL_FORMATTERS
)
OPTIONAL_FORMATTERS_NAMES = ",".join(OPTIONAL_FORMATTERS)
DEFAULT_EXCLUDES = (
    r"(.*/)?(\.direnv|\.eggs|\.git|\.hg|\.mypy_cache|\.nox|\.tox|\.venv|venv"
    r"|\.svn|_build|buck-out|build|dist|__pypackages__)$"
)
log = logging.getLogger(__name__)


def get_parser() -> configargparse.ArgumentParser:
    parser = configargparse.ArgumentParser(
        add_env_var_help=False,
        allow_abbrev=False,
        auto_env_var_prefix="GRAY_",
        description="Less uncompromising Python code formatter.",
        default_config_files=[
            os.path.join(os.path.expanduser("~"), ".gray"),
            "/etc/gray.conf",
            "./gray.conf",
        ],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        ignore_unknown_config_file_keys=True,
        usage="""
            gray myapp.py
            gray myproj/ tests/
            gray --log-level debug --formatters isort,string_fixer ~/app
        """,
    )

    parser.add_argument(
        "paths", nargs="*", help="Paths to format", type=Path,
        default=(Path("."),),
    )

    parser.add_argument(
        "--exclude", type=str,
        help="A regular expression matching files and directories that should"
            " be excluded from formatting. Passing an explicit empty value"
            " means not paths get excluded. Use '/' as directory separator,"
            f" including on Windows. [default: {DEFAULT_EXCLUDES}]",
        default=DEFAULT_EXCLUDES,
    )

    parser.add_argument(
        "--extend-exclude", type=str,
        help="An additional regular expression to use besides --exclude. This"
            " allows to keep the default regex from --exclude.",
    )

    parser.add_argument(
        "--pool-size",
        help="process pool size",
        type=int,
        default=8,
    )

    parser.add_argument(
        "--do-not-detect-venv",
        help="Don't try to detect virtualenv",
        action="store_true",
    )

    group = parser.add_argument_group("Logging options")
    group.add_argument(
        "--log-level",
        default="info",
        choices=("debug", "info", "warning", "error", "fatal"),
    )

    group = parser.add_argument_group("Formatters options")
    group.add_argument(
        "-f",
        "--formatters",
        help="Enabled formatters separated by comma"
            f" (optional: {OPTIONAL_FORMATTERS_NAMES})",
        type=parse_formatters,
        default=FORMATTERS_NAMES,
    )
    group.add_argument(
        "--min-python-version",
        help="Minimum python version to support",
        default=(sys.version_info.major, sys.version_info.minor),
        type=lambda x: tuple(int(d) for d in x.split(".")),
    )

    group = parser.add_argument_group("pyupgrade options")
    group.add_argument(
        "--pyupgrade-keep-percent-format",
        help="Do not upgrade percent formatted strings to f-strings",
        type=parse_bool,
        default=False,
    )
    group.add_argument(
        "--pyupgrade-keep-mock",
        help="Disable rewrite of mock imports",
        type=parse_bool,
        default=False,
    )
    group.add_argument(
        "--pyupgrade-keep-runtime-typing",
        help="Disable pep 585 typing rewrites",
        type=parse_bool,
        default=False,
    )

    group = parser.add_argument_group("string_fixer options")
    group.add_argument(
        "--string-fixer-quote",
        help="preferred quote",
        default="double",
        choices=("single", "double"),
    )

    group = parser.add_argument_group("isort options")
    group.add_argument(
        "--isort-profile",
        help="Base profile type to use for configuration.",
        type=str,
    )
    group.add_argument(
        "--isort-line-length",
        help="The max length of an import line"
            " (used for wrapping long imports)",
        type=int,
        default=80,
    )
    group.add_argument(
        "--isort-wrap-length",
        help="Specifies how long lines that are wrapped should be, if not set"
            " line_length is used. NOTE: wrap_length must be LOWER than or"
            " equal to line_length",
        type=int,
    )
    group.add_argument(
        "--isort-multi-line-output",
        help="Multi line output (0-grid, 1-vertical, 2-hanging, 3-vert-hanging,"
            " 4-vert-grid, 5-vert-grid-grouped, 6-deprecated-alias-for-5,"
            " 7-noqa, 8-vertical-hanging-indent-bracket,"
            " 9-vertical-prefix-from-module-import,"
            " 10-hanging-indent-with-parentheses).",
        type=int,
        default=5,
    )
    group.add_argument(
        "--isort-known-third-party",
        help="Force isort to recognize a module as being part of a third party"
            " library.",
        type=parse_frozenset,
    )
    group.add_argument(
        "--isort-known-first-party",
        help="Force isort to recognize a module as being part of the current"
            " python project.",
        type=parse_frozenset,
    )
    group.add_argument(
        "--isort-known-local-folder",
        help="Force isort to recognize a module as being a local folder."
            " Generally, this is reserved for relative imports"
            " (from . import module).",
        type=parse_frozenset,
    )
    group.add_argument(
        "--isort-virtual-env",
        help="virtual env path",
        type=Path,
        default=os.environ.get("VIRTUAL_ENV", "env"),
    )
    group.add_argument(
        "--isort-include-trailing-comma",
        help="Includes a trailing comma on multi line imports that include"
            " parentheses.",
        type=parse_bool,
        default=True,
    )
    group.add_argument(
        "--isort-lines-after-imports",
        help="empty lines after imports",
        type=int,
        default=2,
    )
    group.add_argument(
        "--isort-skip-gitignore",
        help="Treat project as a git repository and ignore files listed in"
            " .gitignore.",
        type=parse_bool,
        default=True,
    )
    group.add_argument(
        "--isort-use-parentheses",
        help="Use parentheses for line continuation on length limit instead of"
            " slashes. **NOTE**: This is separate from wrap modes, and only"
            " affects how individual lines that are too long get continued, not"
            " sections of multiple imports..",
        type=parse_bool,
        default=True,
    )
    group.add_argument(
        "--isort-length-sort",
        help="Sort imports by their string length.",
        type=parse_bool,
        default=False,
    )
    group.add_argument(
        "--isort-add-imports",
        help="Adds the specified import lines to all files,"
            " automatically determining correct placement.",
        type=parse_frozenset,
    )
    group.add_argument(
        "--isort-remove-imports",
        help="Removes the specified imports from all files.",
        type=parse_frozenset,
    )

    group = parser.add_argument_group("autoflake options")
    group.add_argument(
        "--autoflake-ignore-init-module-imports",
        type=parse_bool,
        default=True,
    )
    group.add_argument(
        "--autoflake-expand-star-imports",
        type=parse_bool,
        default=False,
    )
    group.add_argument(
        "--autoflake-remove-all-unused-imports",
        type=parse_bool,
        default=True,
    )
    group.add_argument(
        "--autoflake-remove-duplicate-keys",
        type=parse_bool,
        default=True,
    )
    group.add_argument(
        "--autoflake-remove-unused-variables",
        type=parse_bool,
        default=True,
    )

    group.add_argument(
        "--autoflake-remove-rhs-for-unused-variables",
        action="store_true",
        help="remove RHS of statements when removing unused variables (unsafe)",
    )

    group = parser.add_argument_group("trim options")
    group.add_argument(
        "--trim-leading-newlines",
        type=parse_bool,
        default=True,
    )

    group = parser.add_argument_group("fixit options")
    group.add_argument(
        "--fixit-redundant-fstrings",
        type=parse_bool,
        default=True,
    )
    group.add_argument(
        "--fixit-redundant-lambdas",
        type=parse_bool,
        default=True,
    )
    group.add_argument(
        "--fixit-redundant-list-comprehensions",
        type=parse_bool,
        default=True,
    )
    group.add_argument(
        "--fixit-to-comprehensions",
        type=parse_bool,
        default=True,
    )
    group.add_argument(
        "--fixit-to-literals",
        type=parse_bool,
        default=True,
    )
    group.add_argument(
        "--fixit-to-fstrings",
        type=parse_bool,
        default=True,
    )

    group = parser.add_argument_group("black options")
    group.add_argument(
        "--black-line-length",
        help="How many characters per line to allow.",
        type=int,
        default=88,
    )
    group.add_argument(
        "--black-skip-magic-trailing-comma",
        help="Don't use trailing commas as a reason to split lines.",
        type=parse_bool,
        default=False,
    )
    group.add_argument(
        "--black-skip-string-normalization",
        help="Don't normalize string quotes or prefixes.",
        type=parse_bool,
        default=False,
    )
    return parser


def main():
    parser = get_parser()
    arguments = parser.parse_args()
    log_config(arguments.log_level)

    try:
        process(arguments)
    except GrayError as e:
        exit(e.exit_code)


if __name__ == "__main__":
    main()
