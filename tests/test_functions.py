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

from expecter import expect

from pyisbn import (_isbn_cleanse, calculate_checksum, convert, validate)
from test_data import TEST_BOOKS


def test__isbn_cleanse_sbn():
    for isbn in TEST_BOOKS.values():
        if isbn.startswith("0"):
            expect(_isbn_cleanse(isbn[1:])) == isbn
            expect(_isbn_cleanse(isbn[1:-1], False)) == isbn[:-1]


def test__isbn_cleanse_isbn():
    for isbn in TEST_BOOKS.values():
        expect(_isbn_cleanse(isbn)) == isbn
        expect(_isbn_cleanse(isbn[:-1], False)) == isbn[:-1]


def test__isbn_cleanse_invalid_type():
    with expect.raises(TypeError, "ISBN must be a string `2'"):
        _isbn_cleanse(2)


def test__isbn_cleanse_invalid_length():
    with expect.raises(ValueError,
                       'ISBN must be either 10 or 13 characters long'):
        _isbn_cleanse("0-123")
    with expect.raises(ValueError,
                       'ISBN must be either 9 or 12 characters long without '
                       'checksum'):
        _isbn_cleanse("0-123", checksum=False)


def test__isbn_cleanse_invalid():
    with expect.raises(ValueError, 'Invalid ISBN string(non-digit parts)'):
        _isbn_cleanse("0-x4343")
    with expect.raises(ValueError,
                       'Invalid ISBN-10 string(non-digit or X checksum)'):
        _isbn_cleanse("012345678-b")
    with expect.raises(ValueError,
                       'Invalid ISBN-13 string(non-digit checksum)'):
        _isbn_cleanse("012345678901b")
    with expect.raises(ValueError, 'Invalid ISBN string(non-digit parts)'):
        _isbn_cleanse("xxxxxxxxxxxx1")


def test_calculate_checksum():
    for isbn in TEST_BOOKS.values():
        expect(calculate_checksum(isbn[:-1])) == isbn[-1]


def test_convert():
    for isbn in TEST_BOOKS.values():
        expect(convert(convert(isbn))) == isbn.replace("-", "")


def test_convert_invalid():
    with expect.raises(ValueError,
                       'Only ISBN-13s with 978 Bookland code can be converted '
                       'to ISBN-10.'):
        convert("0000000000000")


def test_validate():
    for isbn in TEST_BOOKS.values():
        expect(validate(isbn)) == True


def test_validate_invalid():
    for isbn in ("1-234-56789-0", "2-345-6789-1", "3-456-7890-X"):
        expect(validate(isbn)) == False
