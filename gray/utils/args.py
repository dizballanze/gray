from configargparse import ArgumentError

from gray.formatters import FORMATTERS


def parse_formatters(v):
    formatters = v.split(",")

    for formatter_name in formatters:
        if formatter_name not in FORMATTERS:
            raise ArgumentError(f"Uknown formatter {formatter_name}")

    return formatters
