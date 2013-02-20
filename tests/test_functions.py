#
# coding=utf-8
"""test_functions - Test function interface"""
# Copyright © 2007, 2008, 2009, 2010, 2011, 2012, 2013  James Rowe <jnrowe@gmail.com>
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
from nose2.tools import params


from pyisbn import (IsbnError, _isbn_cleanse, calculate_checksum, convert,
                    validate)
from tests.test_data import TEST_BOOKS


@params(*TEST_BOOKS.values())
def test__isbn_cleanse_sbn(isbn):
    if isbn.startswith('0'):
        expect(_isbn_cleanse(isbn[1:])) == isbn
        expect(_isbn_cleanse(isbn[1:-1], False)) == isbn[:-1]


@params(*TEST_BOOKS.values())
def test__isbn_cleanse_isbn(isbn):
    expect(_isbn_cleanse(isbn)) == isbn
    expect(_isbn_cleanse(isbn[:-1], False)) == isbn[:-1]


def test__isbn_cleanse_invalid_type():
    with expect.raises(TypeError, "ISBN must be a string, received 2"):
        _isbn_cleanse(2)


@params(
    (True, 'ISBN must be either 10 or 13 characters long'),
    (False, 'ISBN must be either 9 or 12 characters long without checksum'),
)
def test__isbn_cleanse_invalid_length(checksum, message):
    with expect.raises(IsbnError, message):
        _isbn_cleanse('0-123', checksum=checksum)


@params(
    ('0-x4343', 'non-digit parts'),
    ('012345678-b', 'non-digit or X checksum'),
    ('012345678901b', 'non-digit checksum'),
    ('xxxxxxxxxxxx1', 'non-digit parts'),
)
def test__isbn_cleanse_invalid(isbn, message):
    with expect.raises(IsbnError, message):
        _isbn_cleanse(isbn)


@params(*TEST_BOOKS.values())
def test_calculate_checksum(isbn):
    expect(calculate_checksum(isbn[:-1])) == isbn[-1]


@params(*TEST_BOOKS.values())
def test_convert(isbn):
    expect(convert(convert(isbn))) == isbn.replace('-', '')


def test_convert_invalid():
    with expect.raises(IsbnError,
                       'Only ISBN-13s with 978 Bookland code can be converted '
                       'to ISBN-10.'):
        convert('0000000000000')


@params(*TEST_BOOKS.values())
def test_validate(isbn):
    expect(validate(isbn)) == True


@params(
    ('1-234-56789-0', ),
    ('2-345-6789-1', ),
    ('3-456-7890-X', )
)
def test_validate_invalid(isbn):
    expect(validate(isbn)) == False
