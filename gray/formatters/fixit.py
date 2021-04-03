from argparse import Namespace
from pathlib import Path

from fixit.rule_lint_engine import lint_file_and_apply_patches
from fixit.rules.no_redundant_fstring import NoRedundantFStringRule
from fixit.rules.no_redundant_lambda import NoRedundantLambdaRule
from fixit.rules.no_redundant_list_comprehension import (
    NoRedundantListComprehensionRule
)
from fixit.rules.rewrite_to_comprehension import RewriteToComprehensionRule
from fixit.rules.rewrite_to_literal import RewriteToLiteralRule
from fixit.rules.use_fstring import UseFstringRule

from gray.formatters.base import BaseFormatter


class FixitFormatter(BaseFormatter):

    def __init__(self, arguments: Namespace):
        self._rules = []
        if arguments.fixit_redundant_fstrings:
            self._rules.append(NoRedundantFStringRule)
        if arguments.fixit_redundant_lambdas:
            self._rules.append(NoRedundantLambdaRule)
        if arguments.fixit_redundant_list_comprehensions:
            self._rules.append(NoRedundantListComprehensionRule)
        if arguments.fixit_to_comprehensions:
            self._rules.append(RewriteToComprehensionRule)
        if arguments.fixit_to_literals:
            self._rules.append(RewriteToLiteralRule)

    def process(self, file_path: Path):
        report = lint_file_and_apply_patches(
            file_path,
            file_path.read_bytes(),
            rules=self._rules,
        )
        file_path.write_bytes(report.patched_source)
