#
# coding=utf-8
"""test_isbn - Test Isbn class"""
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

from unittest import TestCase

from expecter import expect
from nose2.tools import params

from pyisbn import (CountryError, Isbn, SiteError)


class TestIsbn(TestCase):
    @params(
        '9780521871723',
        '3540009787',
    )
    def test___repr__(self, isbn):
        expect(repr(Isbn(isbn))) == 'Isbn(%r)' % isbn

    @params(
        '9780521871723',
        '978-052-187-1723',
        '3540009787',
    )
    def test___str__(self, isbn):
        expect(str(Isbn(isbn))) == 'ISBN %s' % isbn

    @params(
        ('978-052-187-1723', '3'),
        ('3540009787', '7'),
        ('354000978', '7'),
    )
    def test_calculate_checksum(self, isbn, result):
        expect(Isbn(isbn).calculate_checksum()) == result

    @params(
        ('0071148167', '9780071148160'),
        ('9780071148160', '0071148167'),
    )
    def test_convert(self, isbn, result):
        expect(Isbn(isbn).convert()) == result

    @params(
        ('978-052-187-1723', True),
        ('978-052-187-1720', False),
        ('3540009787', True),
        ('354000978x', False),
    )
    def test_validate(self, isbn, result):
        expect(Isbn(isbn).validate()) == result

    @params(
        ('us', 'http://www.amazon.com/s?search-alias=stripbooks&field-isbn=0071148167'),
        ('uk', 'http://www.amazon.co.uk/s?search-alias=stripbooks&field-isbn=0071148167'),
        ('de', 'http://www.amazon.de/s?search-alias=stripbooks&field-isbn=0071148167'),
    )
    def test_to_url(self, country, result):
        expect(Isbn('0071148167').to_url(country=country)) == result

    def test_to_url_invalid_country(self):
        with expect.raises(CountryError, "zh"):
            Isbn('0071148167').to_url(country='zh')

    @params(
        ('copac', 'http://copac.ac.uk/search?isn=0071148167'),
        ('google', 'http://books.google.com/books?vid=isbn:0071148167'),
        ('isbndb', 'http://isbndb.com/search/all?query=0071148167'),
        ('worldcat', 'http://worldcat.org/isbn/0071148167'),
        ('waterstones',
         'http://www.waterstones.com/waterstonesweb/advancedSearch.do?buttonClicked=2&isbn=0071148167'),
        ('whsmith',
         'http://www.whsmith.co.uk/CatalogAndSearch/SearchWithinCategory.aspx?as_ISBN=0071148167'),
    )
    def test_to_url_site(self, site, result):
        expect(Isbn('0071148167').to_url(site=site)) == result

    def test_to_url_invalid_site(self):
        with expect.raises(SiteError, "nosite"):
            Isbn('0071148167').to_url(site='nosite')

    def test_to_urn(self):
        expect(Isbn('0071148167').to_urn()) == 'URN:ISBN:0071148167'
