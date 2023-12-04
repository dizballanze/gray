from argparse import Namespace
from pathlib import Path


try:
    from fixit.rule_lint_engine import lint_file_and_apply_patches
    from fixit.rules.no_redundant_fstring import (
        NoRedundantFStringRule as NoRedundantFString,
    )
    from fixit.rules.no_redundant_lambda import (
        NoRedundantLambdaRule as NoRedundantLambda,
    )
    from fixit.rules.no_redundant_list_comprehension import (
        NoRedundantListComprehensionRule as NoRedundantListComprehension,
    )
    from fixit.rules.rewrite_to_comprehension import (
        RewriteToComprehensionRule as RewriteToComprehension,
    )
    from fixit.rules.rewrite_to_literal import (
        RewriteToLiteralRule as RewriteToLiteral,
    )
    from fixit.rules.use_fstring import UseFstringRule as UseFstring
    _FIXIT_V1 = True
except ImportError:
    from fixit.api import fixit_file
    from fixit.ftypes import Options
    from fixit.rules.no_redundant_fstring import NoRedundantFString
    from fixit.rules.no_redundant_lambda import NoRedundantLambda
    from fixit.rules.no_redundant_list_comprehension import (
        NoRedundantListComprehension,
    )
    from fixit.rules.rewrite_to_comprehension import RewriteToComprehension
    from fixit.rules.rewrite_to_literal import RewriteToLiteral
    from fixit.rules.use_fstring import UseFstring
    _FIXIT_V1 = False


from gray.formatters.base import BaseFormatter


class FixitFormatter(BaseFormatter):

    def __init__(self, arguments: Namespace):
        self._rules = []
        if arguments.fixit_redundant_fstrings:
            self._rules.append(NoRedundantFString)
        if arguments.fixit_redundant_lambdas:
            self._rules.append(NoRedundantLambda)
        if arguments.fixit_redundant_list_comprehensions:
            self._rules.append(NoRedundantListComprehension)
        if arguments.fixit_to_comprehensions:
            self._rules.append(RewriteToComprehension)
        if arguments.fixit_to_literals:
            self._rules.append(RewriteToLiteral)
        if arguments.fixit_to_fstrings:
            self._rules.append(UseFstring)

    def process(self, file_path: Path):
        if _FIXIT_V1:
            report = lint_file_and_apply_patches(
                file_path,
                file_path.read_bytes(),
                rules=self._rules,
            )
            file_path.write_bytes(report.patched_source)
        else:
            options = Options(debug=False, config_file=None, rules=self._rules)
            fixit_file(file_path, autofix=True, options=options)
