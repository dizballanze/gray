"""Unittests for gray.formatters.composite."""

import pathlib
import unittest
from unittest import mock
from gray.formatters.composite import CompositeFormatter
from gray.formatters.base import BaseFormatter

class FakeFormatter(BaseFormatter):
    """Fake Formatter Class for testing."""

    def __init__(self, name, callback):
        self.name = name
        self.callback = callback

    def process(self, file_path: pathlib.Path):
        self.callback(self.name, file_path)


class TestCompositeFormatter(unittest.TestCase):
    """Test the CompositeFormatter class."""

    def test_composite_preserves_order(self):
        callback = mock.MagicMock()
        formatter_a = FakeFormatter('a', callback)
        formatter_b = FakeFormatter('b', callback)
        formatter_c = FakeFormatter('c', callback)
        self.assertIsNot(formatter_a, formatter_b)
        self.assertIsNot(formatter_b, formatter_c)

        fake_path = pathlib.Path('/fake/file.py')

        formatters = CompositeFormatter(formatter_a, formatter_b, formatter_c)
        formatters.process(fake_path)
        self.assertEqual(3, callback.call_count)
        callback.assert_has_calls([
            mock.call('a', fake_path),
            mock.call('b', fake_path),
            mock.call('c', fake_path),
        ])

        callback.reset_mock()
        formatters = CompositeFormatter(formatter_c, formatter_b, formatter_a)
        formatters.process(fake_path)
        self.assertEqual(3, callback.call_count)
        callback.assert_has_calls([
            mock.call('c', fake_path),
            mock.call('b', fake_path),
            mock.call('a', fake_path),
        ])
