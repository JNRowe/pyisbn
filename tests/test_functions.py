#
# coding=utf-8
"""test_functions - Test function interface"""
# Copyright © 2007-2017  James Rowe <jnrowe@gmail.com>
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

import unicodedata

from expecter import expect
from nose2.tools import params


from pyisbn import (IsbnError, _isbn_cleanse, calculate_checksum, convert,
                    validate)
from tests.test_data import TEST_BOOKS


@params(*TEST_BOOKS.values())
def test__isbn_cleanse_sbn(isbn):
    if isbn.startswith('0'):
        expect(_isbn_cleanse(isbn[1:])) == isbn.replace('-', '')
        expect(_isbn_cleanse(isbn[1:-1], False)) == isbn.replace('-', '')[:-1]


@params(*TEST_BOOKS.values())
def test__isbn_cleanse_isbn(isbn):
    expect(_isbn_cleanse(isbn)) == isbn.replace('-', '')
    expect(_isbn_cleanse(isbn[:-1], False)) == isbn.replace('-', '')[:-1]


# See tests.test_regressions.test_issue_7_unistr
@params(
    unicodedata.lookup('EN DASH').join(['978', '1', '84724', '253', '2']),
    unicodedata.lookup('EM DASH').join(['978', '0', '385', '08695', '0']),
    unicodedata.lookup('HORIZONTAL BAR').join(['978', '0199564095']),
)
def test__isbn_cleanse_unicode_dash(isbn):
    expect(_isbn_cleanse(isbn)) == "".join(filter(lambda s: s.isdigit(), isbn))


@params(
    unicodedata.lookup('EN DASH').join(['978', '1', '84724', '253', '2']),
    '978-0-385-08695-0',
)
def test__isbn_cleanse_reflect_type(isbn):
    expect(type(_isbn_cleanse(isbn))) == type(isbn)


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
    ('0x0000000', 'non-digit parts', False),
)
def test__isbn_cleanse_invalid(isbn, message, checksum=True):
    with expect.raises(IsbnError, message):
        _isbn_cleanse(isbn, checksum)


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
