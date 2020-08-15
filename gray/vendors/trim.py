#!/usr/bin/env python
#
# Copyright (C) 2012-2015 Steven Myint
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""Trims trailing whitespace from files."""

from __future__ import print_function
from __future__ import unicode_literals

import io
import os
import sys


__version__ = '0.4'


CR = '\r'
LF = '\n'
CRLF = '\r\n'

MAX_READ = 1024
MAX_LINE_LENGTH = 200


try:
    unicode
except NameError:
    unicode = str


def trim(text, leading=False):
    """Return trailing whitespace removed."""
    split_lines = io.StringIO(text).readlines()
    line_ending = find_line_ending(split_lines)

    without_trailing = line_ending.join(
        [line.rstrip() for line in split_lines]).rstrip() + line_ending

    if leading:
        without_trailing = without_trailing.lstrip(line_ending)

    return without_trailing


def find_line_ending(source):
    """Return type of line ending used in source."""
    cr, lf, crlf = 0, 0, 0
    for s in source:
        if s.endswith(CRLF):
            crlf += 1
        elif s.endswith(CR):
            cr += 1
        elif s.endswith(LF):
            lf += 1
    _max = max(cr, crlf, lf)
    if _max == lf:
        return LF
    elif _max == crlf:
        return CRLF
    elif _max == cr:
        return CR
    else:
        return LF


def trim_file(filename, leading=False):
    """Remove trailing whitespace from a file in place.

    Remove leading newlines if "leading" is True.

    Return True if file is modified.

    """
    with open_unicode_file(filename) as input_file:
        original_text = input_file.read()

    trimmed_text = trim(original_text, leading=leading)

    if trimmed_text != original_text:
        with open_unicode_file(filename, 'w') as output_file:
            output_file.write(trimmed_text)

        return True

    return False


def is_text(filename):
    """Return True if file is a text file.

    This is a guess. Files with null bytes are considered to be binary.
    Also, files that start with an extremely long line are considered to
    be binary. Empty files are considered as not text.

    """
    if os.path.islink(filename):
        return False

    try:
        with open_unicode_file(filename) as input_file:
            string = input_file.read(MAX_READ)

            if not string or '\x00' in string:
                return False

            split_string = string.split()
            if split_string and len(split_string[0]) > MAX_LINE_LENGTH:
                return False
    except (IOError, UnicodeDecodeError):
        return False

    return True


def open_unicode_file(filename, mode='r'):
    """Return opened Unicode file."""
    return io.open(filename, mode=mode, encoding='utf-8',
                   newline='')  # Preserve line endings


def main():
    """Main."""
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, prog='trim')
    parser.add_argument('--leading-newlines', action='store_true',
                        help='remove leading newlines too')
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + __version__)
    parser.add_argument('files', nargs='+',
                        help='files to trim')

    args = parser.parse_args()

    filenames = list(set(args.files))
    while filenames:
        name = filenames.pop(0)
        if os.path.isdir(name):
            for root, directories, children in os.walk(unicode(name)):
                filenames += [os.path.join(root, f) for f in children
                              if not f.startswith('.')]

                directories[:] = [d for d in directories
                                  if not d.startswith('.')]
        else:
            try:
                if is_text(name) and trim_file(name,
                                               leading=args.leading_newlines):
                    print('[file:%s]' % name, file=sys.stderr)
            except (IOError, UnicodeDecodeError) as error:
                print('{0}:{1}'.format(name, error), file=sys.stderr)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(1)
