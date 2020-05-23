import sys
from argparse import Namespace
from pathlib import Path

from autoflake import fix_file

from gray.formatters.base import BaseFormatter


class AutoflakeFormatter(BaseFormatter):

    def __init__(self, arguments: Namespace):
        self._args = Namespace(
            ignore_init_module_imports=arguments.autoflake_ignore_init_module_imports,
            expand_star_imports=arguments.autoflake_expand_star_imports,
            remove_all_unused_imports=arguments.autoflake_remove_all_unused_imports,
            remove_duplicate_keys=arguments.autoflake_remove_duplicate_keys,
            remove_unused_variables=arguments.autoflake_remove_unused_variables,
            imports="",
            check=False,
            in_place=True,
        )

    def process(self, file_path: Path):
        fix_file(file_path, args=self._args, standard_out=sys.stdout)
