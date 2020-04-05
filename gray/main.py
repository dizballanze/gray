import argparse
import logging
import os
from pathlib import Path

import configargparse
from prettylog import LogFormat, basic_config

from gray.formatters import FORMATTERS
from gray.processing import process
from gray.utils.args import parse_formatters


FORMATTERS_NAMES = ",".join(FORMATTERS.keys())

log = logging.getLogger(__name__)


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
        gray --log-level debug --formatters isort,unify ~/app
    """,
)

parser.add_argument(
    "paths", nargs="*", help="Paths to format", type=Path, default=(Path("."),),
)

group = parser.add_argument_group("Logging options")
group.add_argument(
    "--log-level",
    default="info",
    choices=("debug", "info", "warning", "error", "fatal"),
)
group.add_argument(
    "--log-format", choices=LogFormat.choices(), default="color",
)

group = parser.add_argument_group("Formatters options")
group.add_argument(
    "-f",
    "--formatters",
    help="Enabled formatters separated by comma",
    type=parse_formatters,
    default=FORMATTERS_NAMES,
)


def main():
    arguments = parser.parse_args()
    basic_config(
        level=arguments.log_level,
        log_format=arguments.log_format,
        buffered=False,
        date_format=None,
    )
    process(arguments)


if __name__ == "__main__":
    main()
