from types import MappingProxyType

from gray.formatters.add_trailing_comma import AddTrailingCommaFormatter
from gray.formatters.composite import CompositeFormatter
from gray.formatters.isort import SortImportsFormatter
from gray.formatters.pyupgrade import PyUpgradeFormatter
from gray.formatters.unify import UnifyFormatter
from gray.formatters.base import BaseFormatter


FORMATTERS = MappingProxyType({
    "add-trailing-comma": AddTrailingCommaFormatter,
    "isort": SortImportsFormatter,
    "pyupgrade": PyUpgradeFormatter,
    "unify": UnifyFormatter,
})


__all__ = ("FORMATTERS", "BaseFormatter", "CompositeFormatter",)
