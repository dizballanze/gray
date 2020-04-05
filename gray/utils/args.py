from configargparse import ArgumentError

from gray.formatters.composite import CompositeFormatter
from gray.processing import FORMATTERS


def parse_formatters(v):
    formatters = []
    for formatter_name in v.split(","):
        if formatter_name not in FORMATTERS:
            raise ArgumentError(f"Uknown formatter {formatter_name}")
        formatters.append(FORMATTERS[formatter_name]())

    return CompositeFormatter(*formatters)
