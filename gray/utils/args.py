from gray.formatters import FORMATTERS


def parse_formatters(v: str):
    """Validate and returns the formatters to use as a list."""
    formatters = [x.strip() for x in v.split(",") if x.strip()]

    for formatter_name in formatters:
        if formatter_name not in FORMATTERS:
            raise ValueError(f"Unknown formatter {formatter_name}")

    return formatters


def parse_bool(v):
    """Returns a command line flag as a boolean."""
    if isinstance(v, bool):
        return v

    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    if v.lower() in ("no", "false", "f", "n", "0"):
        return False

    raise ValueError("Boolean value expected.")


def parse_frozenset(v: str):
    """Returns a comma separated string as a frozen set."""
    return frozenset(x.strip() for x in v.split(",") if x.strip())
