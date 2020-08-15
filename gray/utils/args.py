from configargparse import ArgumentError

from gray.formatters import FORMATTERS


def parse_formatters(v):
    formatters = v.split(",")

    for formatter_name in formatters:
        if formatter_name not in FORMATTERS:
            raise ArgumentError(f"Uknown formatter {formatter_name}")

    return formatters


def parse_bool(v):
    if isinstance(v, bool):
       return v

    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False

    raise ArgumentError("Boolean value expected.")
