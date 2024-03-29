#
"""test_functions - Test function interface."""
# Copyright © 2012-2021  James Rowe <jnrowe@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This file is part of pyisbn.
#
# pyisbn is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# pyisbn is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# pyisbn.  If not, see <http://www.gnu.org/licenses/>.

from hypothesis import given
from hypothesis.strategies import sampled_from
from pytest import mark, raises

from pyisbn import (
    IsbnError,
    _isbn_cleanse,
    calculate_checksum,
    convert,
    validate,
)
from tests.data import TEST_ISBNS


@given(sampled_from(TEST_ISBNS))
def test__isbn_cleanse_sbn(isbn: str):
    if isbn.startswith('0'):
        assert _isbn_cleanse(isbn[1:]) == isbn
        assert _isbn_cleanse(isbn[1:-1], False) == isbn[:-1]


@given(sampled_from(TEST_ISBNS))
def test__isbn_cleanse_isbn(isbn: str):
    assert _isbn_cleanse(isbn) == isbn
    assert _isbn_cleanse(isbn[:-1], False) == isbn[:-1]


# See tests.test_regressions.test_issue_7_unistr
# NOTE: Depending on your typeface and editor you may notice that the following
# dashes are not HYPHEN-MINUS.  They're not, and this is on purpose
@mark.parametrize(
    'isbn',
    [
        '978–1–84724–253–2',
        '978—0—385—08695—0',
        '978―0199564095',
    ],
)
def test__isbn_cleanse_unicode_dash(isbn: str):
    assert _isbn_cleanse(isbn) == ''.join(filter(lambda s: s.isdigit(), isbn))


# NOTE: Depending on your typeface and editor you may notice that the following
# dashes are not HYPHEN-MINUS.  They're not, and this is on purpose
@mark.parametrize(
    'isbn',
    [
        '978–1–84724–253–2',
        '978-0-385-08695-0',
    ],
)
def test__isbn_cleanse_reflect_type(isbn: str):
    assert type(_isbn_cleanse(isbn)) == type(isbn)


def test__isbn_cleanse_invalid_type():
    with raises(TypeError, match='ISBN must be a string, received 2'):
        _isbn_cleanse(2)


@mark.parametrize(
    'checksum,message',
    [
        (True, 'ISBN must be either 10 or 13 characters long'),
        (
            False,
            'ISBN must be either 9 or 12 characters long without checksum',
        ),
    ],
)
def test__isbn_cleanse_invalid_length(checksum: bool, message: str):
    with raises(IsbnError, match=message):
        _isbn_cleanse('0-123', checksum=checksum)


@mark.parametrize(
    'isbn,message',
    [
        ('0-x4343', 'non-digit parts'),
        ('012345678-b', 'non-digit or X checksum'),
        ('012345678901b', 'non-digit checksum'),
        ('xxxxxxxxxxxx1', 'non-digit parts'),
        ('0x0000000', 'non-digit parts'),
    ],
)
def test__isbn_cleanse_invalid(isbn: str, message: str):
    with raises(IsbnError, match=message):
        _isbn_cleanse(isbn)


@mark.parametrize(
    'isbn,message',
    [
        ('0x0000000', 'non-digit parts'),
        ('580003417076', 'invalid Bookland region'),
    ],
)
def test__isbn_cleanse_invalid_no_checksum(isbn, message):
    with raises(IsbnError, match=message):
        _isbn_cleanse(isbn, False)


@given(sampled_from(TEST_ISBNS))
def test_calculate_checksum(isbn: str):
    assert calculate_checksum(isbn[:-1]) == isbn[-1]


@given(sampled_from(TEST_ISBNS))
def test_convert(isbn: str):
    assert convert(convert(isbn)) == isbn


def test_convert_invalid():
    with raises(
        IsbnError,
        match='Only ISBN-13s with 978 Bookland code can be '
        'converted to ISBN-10.',
    ):
        convert('9790000000001')


@given(sampled_from(TEST_ISBNS))
def test_validate(isbn: str):
    assert validate(isbn)


@mark.parametrize(
    'isbn',
    [
        '1-234-56789-0',
        '2-345-6789-1',
        '3-456-7890-X',
    ],
)
def test_validate_invalid(isbn: str):
    assert validate(isbn) is False
