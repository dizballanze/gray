"""Unittests for gray.formatters.composite."""

import pathlib
from unittest import mock

from gray.formatters.base import BaseFormatter
from gray.formatters.composite import CompositeFormatter


class FakeFormatter(BaseFormatter):
    """Fake Formatter Class for testing."""

    def __init__(self, name, callback):
        self.name = name
        self.callback = callback

    def process(self, file_path: pathlib.Path):
        self.callback(self.name, file_path)


def test_composite_preserves_order():
    callback = mock.MagicMock()
    formatter_a = FakeFormatter("a", callback)
    formatter_b = FakeFormatter("b", callback)
    formatter_c = FakeFormatter("c", callback)
    assert formatter_a is not formatter_b
    assert formatter_b is not formatter_c

    fake_path = pathlib.Path("/fake/file.py")

    formatters = CompositeFormatter(formatter_a, formatter_b, formatter_c)
    formatters.process(fake_path)
    assert callback.call_count == 3
    callback.assert_has_calls([
        mock.call("a", fake_path),
        mock.call("b", fake_path),
        mock.call("c", fake_path),
    ])

    callback.reset_mock()
    formatters = CompositeFormatter(formatter_c, formatter_b, formatter_a)
    formatters.process(fake_path)
    assert callback.call_count == 3
    callback.assert_has_calls([
        mock.call("c", fake_path),
        mock.call("b", fake_path),
        mock.call("a", fake_path),
    ])
