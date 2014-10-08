#
# coding=utf-8
"""test_isbn - Test Isbn class"""
# Copyright © 2007-2013  James Rowe <jnrowe@gmail.com>
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

from sys import version_info

from pytest import (mark, raises)

from pyisbn import (CountryError, Isbn, SiteError)


class TestIsbn:
    @mark.parametrize('isbn', [
        '9780521871723',
        '3540009787',
    ])
    def test___repr__(self, isbn):
        assert repr(Isbn(isbn)) == 'Isbn(%r)' % isbn

    @mark.parametrize('isbn', [
        '9780521871723',
        '978-052-187-1723',
        '3540009787',
    ])
    def test___str__(self, isbn):
        assert str(Isbn(isbn)) == 'ISBN %s' % isbn

    @mark.skipif(version_info < (2, 6),
                 reason="format() not supported with this Python version")
    @mark.parametrize('isbn, format_spec, result', [
        ('9780521871723', '', 'ISBN 9780521871723'),
        ('978-052-187-1723', 'urn', 'URN:ISBN:978-052-187-1723'),
        ('3540009787', 'url',
         'http://www.amazon.com/s?search-alias=stripbooks&field-isbn='
         '3540009787'),
        ('3540009787', 'url:amazon:uk',
         'http://www.amazon.co.uk/s?search-alias=stripbooks&field-isbn='
         '3540009787'),
    ])
    def test___format__(self, isbn, format_spec, result):
        assert format(Isbn(isbn), format_spec) == result

    @mark.parametrize('isbn, result', [
        ('978-052-187-1723', '3'),
        ('3540009787', '7'),
        ('354000978', '7'),
    ])
    def test_calculate_checksum(self, isbn, result):
        assert Isbn(isbn).calculate_checksum() == result

    @mark.parametrize('isbn, result', [
        ('0071148167', '9780071148160'),
        ('9780071148160', '0071148167'),
    ])
    def test_convert(self, isbn, result):
        assert Isbn(isbn).convert() == result

    @mark.parametrize('isbn, result', [
        ('978-052-187-1723', True),
        ('978-052-187-1720', False),
        ('3540009787', True),
        ('354000978x', False),
    ])
    def test_validate(self, isbn, result):
        assert Isbn(isbn).validate() == result

    @mark.parametrize('country, result', [
        ('us', 'http://www.amazon.com/s?search-alias=stripbooks&field-isbn=0071148167'),
        ('uk', 'http://www.amazon.co.uk/s?search-alias=stripbooks&field-isbn=0071148167'),
        ('de', 'http://www.amazon.de/s?search-alias=stripbooks&field-isbn=0071148167'),
    ])
    def test_to_url(self, country, result):
        assert Isbn('0071148167').to_url(country=country) == result

    def test_to_url_invalid_country(self):
        with raises(CountryError) as err:
            Isbn('0071148167').to_url(country='zh')
        assert err.value.message == 'zh'

    @mark.parametrize('site, result', [
        ('copac', 'http://copac.ac.uk/search?isn=0071148167'),
        ('google', 'http://books.google.com/books?vid=isbn:0071148167'),
        ('isbndb', 'http://isbndb.com/search/all?query=0071148167'),
        ('worldcat', 'http://worldcat.org/isbn/0071148167'),
        ('waterstones',
         'http://www.waterstones.com/waterstonesweb/advancedSearch.do?buttonClicked=2&isbn=0071148167'),
        ('whsmith',
         'http://www.whsmith.co.uk/CatalogAndSearch/SearchWithinCategory.aspx?as_ISBN=0071148167'),
    ])
    def test_to_url_site(self, site, result):
        assert Isbn('0071148167').to_url(site=site) == result

    def test_to_url_invalid_site(self):
        with raises(SiteError) as err:
            Isbn('0071148167').to_url(site='nosite')
        assert err.value.message == "nosite"

    def test_to_urn(self):
        assert Isbn('0071148167').to_urn() == 'URN:ISBN:0071148167'
