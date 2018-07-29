#
# coding=utf-8
"""test_isbn - Test Isbn class."""
# Copyright © 2012-2017  James Rowe <jnrowe@gmail.com>
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
#
# SPDX-License-Identifier: GPL-3.0+

from sys import version_info

from pytest import mark, raises

from pyisbn import (CountryError, Isbn, SiteError)
from tests.data import TEST_ISBNS


@mark.parametrize('isbn', TEST_ISBNS + [
    '9780521871723',
    '3540009787',
])
def test___repr__(isbn):
    assert repr(Isbn(isbn)) == 'Isbn(%r)' % isbn


@mark.parametrize('isbn', TEST_ISBNS + [
    '9780521871723',
    '978-052-187-1723',
    '3540009787',
])
def test___str__(isbn):
    assert str(Isbn(isbn)) == 'ISBN %s' % isbn


@mark.skipif(version_info < (2, 6),
             reason='format() not supported with this Python version')
@mark.parametrize('isbn,format_spec,result',
    [(s, '', 'ISBN %s' % s) for s in TEST_ISBNS] + [
    ('9780521871723', '', 'ISBN 9780521871723'),
    ('978-052-187-1723', 'urn', 'URN:ISBN:978-052-187-1723'),
    ('3540009787', 'url',
        'https://www.amazon.com/s?search-alias=stripbooks&field-isbn='
        '3540009787'),
    ('3540009787', 'url:amazon:uk',
        'https://www.amazon.co.uk/s?search-alias=stripbooks&field-isbn='
        '3540009787'),
    ('3540009787', 'url:amazon',
        'https://www.amazon.com/s?search-alias=stripbooks&field-isbn='
        '3540009787'),
])
def test___format__(isbn, format_spec, result):
    assert format(Isbn(isbn), format_spec) == result


def test___format__invalid_format_spec():
    with raises(ValueError, match="Unknown format_spec 'biscuit'"):
        format(Isbn('0071148167'), 'biscuit')


@mark.parametrize('isbn,result', [(s, s[-1]) for s in TEST_ISBNS] + [
    ('978-052-187-1723', '3'),
    ('3540009787', '7'),
    ('354000978', '7'),
])
def test_calculate_checksum(isbn, result):
    assert Isbn(isbn).calculate_checksum() == result


@mark.parametrize('isbn,result', [
    ('0071148167', '9780071148160'),
    ('9780071148160', '0071148167'),
])
def test_convert(isbn, result):
    assert Isbn(isbn).convert() == result


@mark.parametrize('isbn,result', [(s, True) for s in TEST_ISBNS] + [
    ('978-052-187-1723', True),
    ('978-052-187-1720', False),
    ('3540009787', True),
    ('354000978x', False),
])
def test_validate(isbn, result):
    assert Isbn(isbn).validate() == result


@mark.parametrize('country,result', [
    ('us', '.com/s?search-alias=stripbooks&field-isbn=0071148167'),
    ('uk', '.co.uk/s?search-alias=stripbooks&field-isbn=0071148167'),
    ('de', '.de/s?search-alias=stripbooks&field-isbn=0071148167'),
])
def test_to_url(country, result):
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
def test_to_url_site(site, result):
    assert Isbn('0071148167').to_url(site=site) == result


def test_to_url_invalid_site():
    with raises(SiteError, match='nosite'):
        Isbn('0071148167').to_url(site='nosite')


@mark.parametrize('isbn,result',
    [(s, 'URN:ISBN:%s' % s) for s in TEST_ISBNS]
)
def test_to_urn(isbn, result):
    assert Isbn(isbn).to_urn() == result
