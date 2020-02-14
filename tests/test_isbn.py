#
"""test_isbn - Test Isbn class."""
# Copyright © 2012-2020  James Rowe <jnrowe@gmail.com>
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

from sys import version_info
from typing import Tuple

from hypothesis import example, given
from hypothesis.strategies import sampled_from
from pytest import mark, raises

from pyisbn import (CountryError, Isbn, SiteError)
from tests.data import TEST_ISBNS


@example('9780521871723')
@example('3540009787')
@given(sampled_from(TEST_ISBNS))
def test___repr__(isbn: str):
    assert repr(Isbn(isbn)) == f'Isbn({isbn!r})'


@example('9780521871723')
@example('978-052-187-1723')
@example('3540009787')
@given(sampled_from(TEST_ISBNS))
def test___str__(isbn: str):
    assert str(Isbn(isbn)) == f'ISBN {isbn}'


@mark.skipif(version_info < (2, 6),
             reason='format() not supported with this Python version')
@example(('9780521871723', '', 'ISBN 9780521871723'))
@example(('978-052-187-1723', 'urn', 'URN:ISBN:978-052-187-1723'))
@example(
    ('3540009787', 'url',
     'https://www.amazon.com/s?search-alias=stripbooks&field-isbn=3540009787'))
@example((
    '3540009787', 'url:amazon:uk',
    'https://www.amazon.co.uk/s?search-alias=stripbooks&field-isbn=3540009787')
         )
@example(
    ('3540009787', 'url:amazon',
     'https://www.amazon.com/s?search-alias=stripbooks&field-isbn=3540009787'))
@given(sampled_from([(s, '', f'ISBN {s}') for s in TEST_ISBNS]))
def test___format__(data: Tuple[str, str, str]):
    isbn, format_spec, result = data
    assert format(Isbn(isbn), format_spec) == result


def test___format__invalid_format_spec():
    with raises(ValueError, match="Unknown format_spec 'biscuit'"):
        format(Isbn('0071148167'), 'biscuit')


@example(('978-052-187-1723', '3'))
@example(('3540009787', '7'))
@example(('354000978', '7'))
@given(sampled_from([(s, s[-1]) for s in TEST_ISBNS]))
def test_calculate_checksum(data: Tuple[str, str]):
    isbn, result = data
    assert Isbn(isbn).calculate_checksum() == result


@mark.parametrize('isbn,result', [
    ('0071148167', '9780071148160'),
    ('9780071148160', '0071148167'),
])
def test_convert(isbn: str, result: str):
    assert Isbn(isbn).convert() == result


@example(('978-052-187-1723', True))
@example(('978-052-187-1720', False))
@example(('3540009787', True))
@example(('354000978x', False))
@given(sampled_from([(s, True) for s in TEST_ISBNS]))
def test_validate(data: Tuple[str, bool]):
    isbn, result = data
    assert Isbn(isbn).validate() == result


@mark.parametrize('country,result', [
    ('us', '.com/s?search-alias=stripbooks&field-isbn=0071148167'),
    ('uk', '.co.uk/s?search-alias=stripbooks&field-isbn=0071148167'),
    ('de', '.de/s?search-alias=stripbooks&field-isbn=0071148167'),
])
def test_to_url(country: str, result: str):
    assert Isbn('0071148167').to_url(country=country) \
        == 'https://www.amazon' + result


def test_to_url_invalid_country():
    with raises(CountryError, match='zh'):
        Isbn('0071148167').to_url(country='zh')


@mark.parametrize('site,result', [
    ('copac', 'http://copac.jisc.ac.uk/search?isn=0071148167'),
    ('google', 'https://books.google.com/books?vid=isbn:0071148167'),
    ('isbndb', 'https://isbndb.com/search/all?query=0071148167'),
    ('waterstones',
     'https://www.waterstones.com/books/search/term/0071148167'),
    ('whsmith',
     'https://www.whsmith.co.uk/search/go?w=0071148167&af=cat1:books'),
    ('worldcat', 'http://worldcat.org/isbn/0071148167'),
])
def test_to_url_site(site: str, result: str):
    assert Isbn('0071148167').to_url(site=site) == result


def test_to_url_invalid_site():
    with raises(SiteError, match='nosite'):
        Isbn('0071148167').to_url(site='nosite')


@given(sampled_from([(s, f'URN:ISBN:{s}') for s in TEST_ISBNS]))
def test_to_urn(data: Tuple[str, str]):
    isbn, result = data
    assert Isbn(isbn).to_urn() == result
