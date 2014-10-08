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

from sys import version_info

try:
    from unittest2 import TestCase, skipIf
except ImportError:
    from unittest import TestCase, skipIf

from pyisbn import (CountryError, Isbn, SiteError)


class TestIsbn(TestCase):
    def test___repr__(self):
        for isbn in [
                    '9780521871723',
                    '3540009787',
                ]:
            with self.subTest(isbn):
                expect(repr(Isbn(isbn))) == 'Isbn(%r)' % isbn

    def test___str__(self):
        for isbn in [
                    '9780521871723',
                    '978-052-187-1723',
                    '3540009787',
                ]:
            with self.subTest(isbn):
                expect(str(Isbn(isbn))) == 'ISBN %s' % isbn

    @skipIf(version_info < (2, 6),
            "format() not supported with this Python version")
    def test___format__(self):
        for isbn, format_spec, result in [
                    ('9780521871723', '', 'ISBN 9780521871723'),
                    ('978-052-187-1723', 'urn', 'URN:ISBN:978-052-187-1723'),
                    ('3540009787', 'url',
                     'https://www.amazon.com/s?search-alias=stripbooks&'
                     'field-isbn=3540009787'),
                    ('3540009787', 'url:amazon:uk',
                     'https://www.amazon.co.uk/s?search-alias=stripbooks&'
                     'field-isbn=3540009787'),
                    ('3540009787', 'url:amazon',
                     'https://www.amazon.com/s?search-alias=stripbooks&'
                     'field-isbn=3540009787'),
                ]:
            with self.subTest([isbn, format_spec, result]):
                expect(format(Isbn(isbn), format_spec)) == result

    def test___format__invalid_format_spec(self):
        with expect.raises(ValueError, "Unknown format_spec 'biscuit'"):
            format(Isbn('0071148167'), 'biscuit')

    def test_calculate_checksum(self):
        for isbn, result in [
                    ('978-052-187-1723', '3'),
                    ('3540009787', '7'),
                    ('354000978', '7'),
                ]:
            with self.subTest([isbn, result]):
                expect(Isbn(isbn).calculate_checksum()) == result

    def test_convert(self):
        for isbn, result in [
                    ('0071148167', '9780071148160'),
                    ('9780071148160', '0071148167'),
                ]:
            with self.subTest([isbn, result]):
                expect(Isbn(isbn).convert()) == result

    def test_validate(self):
        for isbn, result in [
                    ('978-052-187-1723', True),
                    ('978-052-187-1720', False),
                    ('3540009787', True),
                    ('354000978x', False),
                ]:
            with self.subTest([isbn, result]):
                expect(Isbn(isbn).validate()) == result

    def test_to_url(self):
        for country, result in [
                    ('us',
                     '.com/s?search-alias=stripbooks&field-isbn=0071148167'),
                    ('uk',
                     '.co.uk/s?search-alias=stripbooks&field-isbn=0071148167'),
                    ('de',
                     '.de/s?search-alias=stripbooks&field-isbn=0071148167'),
                ]:
            with self.subTest([country, result]):
                expect(Isbn('0071148167').to_url(country=country)) \
                   == 'https://www.amazon' + result

    def test_to_url_invalid_country(self):
        with expect.raises(CountryError, "zh"):
            Isbn('0071148167').to_url(country='zh')

    def test_to_url_site(self):
        for site, result in [
                    ('copac',
                     'http://copac.jisc.ac.uk/search?isn=0071148167'),
                    ('google',
                     'https://books.google.com/books?vid=isbn:0071148167'),
                    ('isbndb',
                     'https://isbndb.com/search/all?query=0071148167'),
                    ('waterstones',
                     'https://www.waterstones.com/books/search/term/'
                     '0071148167'),
                    ('whsmith',
                     'https://www.whsmith.co.uk/search/go?w=0071148167&'
                     'af=cat1:books'),
                    ('worldcat', 'http://worldcat.org/isbn/0071148167'),
                ]:
            with self.subTest([site, result]):
                expect(Isbn('0071148167').to_url(site=site)) == result

    def test_to_url_invalid_site(self):
        with expect.raises(SiteError, "nosite"):
            Isbn('0071148167').to_url(site='nosite')

    def test_to_urn(self):
        expect(Isbn('0071148167').to_urn()) == 'URN:ISBN:0071148167'
