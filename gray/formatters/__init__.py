from types import MappingProxyType

from .add_trailing_comma import AddTrailingCommaFormatter
from .autoflake import AutoflakeFormatter
from .base import BaseFormatter
from .black import BlackFormatter
from .composite import CompositeFormatter
from .fixit import FixitFormatter
from .isort import SortImportsFormatter
from .pyupgrade import PyUpgradeFormatter
from .string_fixer import StringFixerFormatter
from .trim import TrimFormatter


FORMATTERS = MappingProxyType({
    "add-trailing-comma": AddTrailingCommaFormatter,
    "autoflake": AutoflakeFormatter,
    "black": BlackFormatter,
    "fixit": FixitFormatter,
    "isort": SortImportsFormatter,
    "pyupgrade": PyUpgradeFormatter,
    "trim": TrimFormatter,
    "string_fixer": StringFixerFormatter,
})

OPTIONAL_FORMATTERS = ("black",)


__all__ = ("FORMATTERS", "BaseFormatter", "CompositeFormatter")
