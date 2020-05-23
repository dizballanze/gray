from types import MappingProxyType

from .add_trailing_comma import AddTrailingCommaFormatter
from .autoflake import AutoflakeFormatter
from .base import BaseFormatter
from .composite import CompositeFormatter
from .isort import SortImportsFormatter
from .pyupgrade import PyUpgradeFormatter
from .trim import TrimFormatter
from .unify import UnifyFormatter


FORMATTERS = MappingProxyType({
    "add-trailing-comma": AddTrailingCommaFormatter,
    "autoflake": AutoflakeFormatter,
    "isort": SortImportsFormatter,
    "pyupgrade": PyUpgradeFormatter,
    "trim": TrimFormatter,
    "unify": UnifyFormatter,
})


__all__ = ("FORMATTERS", "BaseFormatter", "CompositeFormatter")
