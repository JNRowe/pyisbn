#
#
"""test_functions - Test function interface"""
# Copyright (C) 2007-2011  James Rowe
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from pyisbn import (_isbn_cleanse, calculate_checksum, convert, validate)
from test_data import TEST_BOOKS


def test__isbn_cleanse():
    """Check ISBN is a string, and passes basic sanity checks.

    >>> for isbn in TEST_BOOKS.values():
    ...     if isbn.startswith("0"):
    ...         if not _isbn_cleanse(isbn[1:]) == isbn:
    ...             print("SBN with checksum failure `%s'" % isbn)
    ...         if not _isbn_cleanse(isbn[1:-1], False) == isbn[:-1]:
    ...             print("SBN without checksum failure `%s'" % isbn)

    >>> for isbn in TEST_BOOKS.values():
    ...     if not _isbn_cleanse(isbn) == isbn:
    ...         print("ISBN with checksum failure `%s'" % isbn)
    ...     if not _isbn_cleanse(isbn[:-1], False) == isbn[:-1]:
    ...         print("ISBN without checksum failure `%s'" % isbn)

    >>> _isbn_cleanse(2)
    Traceback (most recent call last):
      ...
    TypeError: ISBN must be a string `2'
    >>> _isbn_cleanse("0-123")
    Traceback (most recent call last):
    ...
    ValueError: ISBN must be either 10 or 13 characters long
    >>> _isbn_cleanse("0-123", checksum=False)
    Traceback (most recent call last):
    ...
    ValueError: ISBN must be either 9 or 12 characters long without checksum
    >>> _isbn_cleanse("0-x4343")
    Traceback (most recent call last):
    ...
    ValueError: Invalid ISBN string(non-digit parts)
    >>> _isbn_cleanse("012345678-b")
    Traceback (most recent call last):
    ...
    ValueError: Invalid ISBN-10 string(non-digit or X checksum)
    >>> _isbn_cleanse("012345678901b")
    Traceback (most recent call last):
    ...
    ValueError: Invalid ISBN-13 string(non-digit checksum)
    >>> _isbn_cleanse("xxxxxxxxxxxx1")
    Traceback (most recent call last):
    ...
    ValueError: Invalid ISBN string(non-digit parts)

    """


def test_calculate_checksum():
    """Calculate ISBN checksum.

    >>> for isbn in TEST_BOOKS.values():
    ...     if not calculate_checksum(isbn[:-1]) == isbn[-1]:
    ...         print("ISBN checksum failure `%s'" % isbn)

    """


def test_convert():
    """Convert ISBNs between ISBN-10 and ISBN-13.

    >>> for isbn in TEST_BOOKS.values():
    ...     if not convert(convert(isbn)) == isbn.replace("-", ""):
    ...         print("ISBN conversion failure `%s'" % isbn)
    >>> convert("0000000000000")
    Traceback (most recent call last):
    ...
    ValueError: Only ISBN-13s with 978 Bookland code can be converted to ISBN-10.

    """


def test_validate():
    """Validate ISBNs.

    Valid ISBNs

    >>> for isbn in TEST_BOOKS.values():
    ...     if not validate(isbn):
    ...         print("ISBN validation failure `%s'" % isbn)

    Invalid ISBNs

    >>> for isbn in ("1-234-56789-0", "2-345-6789-1", "3-456-7890-X"):
    ...     if validate(isbn):
    ...         print("ISBN invalidation failure `%s'" % isbn)

    """
