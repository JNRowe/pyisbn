#
#
"""test_isbn - Test Isbn class"""
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

from unittest import TestCase

from expecter import expect

from pyisbn import Isbn


class TestIsbn(TestCase):
    def test___repr__(self):
        expect(repr(Isbn("9780521871723"))) == "Isbn('9780521871723')"
        expect(repr(Isbn("3540009787"))) == "Isbn('3540009787')"

    def test___str__(self):
        expect(str(Isbn("9780521871723"))) == 'ISBN 9780521871723'
        expect(str(Isbn("978-052-187-1723"))) == 'ISBN 978-052-187-1723'
        expect(str(Isbn("3540009787"))) == 'ISBN 3540009787'

    def test_calculate_checksum(self):
        expect(Isbn("978-052-187-1723").calculate_checksum()) == '3'
        expect(Isbn("3540009787").calculate_checksum()) == '7'
        expect(Isbn("354000978").calculate_checksum()) == '7'

    def test_convert(self):
        expect(Isbn("0071148167").convert()) == '9780071148160'
        expect(Isbn("9780071148160").convert()) == '0071148167'

    def test_validate(self):
        expect(Isbn("978-052-187-1723").validate()) == True
        expect(Isbn("978-052-187-1720").validate()) == False
        expect(Isbn("3540009787").validate()) == True
        expect(Isbn("354000978x").validate()) == False

    def test_to_url(self):
        expect(Isbn("0071148167").to_url()) == \
            'http://amazon.com/dp/0071148167'
        expect(Isbn("0071148167").to_url(country="uk")) == \
            'http://amazon.co.uk/dp/0071148167'
        expect(Isbn("0071148167").to_url(country="de")) == \
            'http://amazon.de/dp/0071148167'

    def test_to_url_invalid_country(self):
        with expect.raises(ValueError, "Unknown site `zh'."):
            Isbn("0071148167").to_url(country="zh")

    def test_to_url_site(self):
        expect(Isbn("0071148167").to_url(site="google")) == \
            'http://books.google.com/books?vid=isbn:0071148167'
        expect(Isbn("0071148167").to_url(site="isbndb")) == \
            'http://isbndb.com/search-all.html?kw=0071148167'
        expect(Isbn("0071148167").to_url(site="worldcat")) == \
            'http://worldcat.org/isbn/0071148167'
        expect(Isbn("0071148167").to_url(site="waterstones")) == \
            'http://www.waterstones.com/waterstonesweb/advancedSearch.do?buttonClicked=2&isbn=0071148167'
        expect(Isbn("0071148167").to_url(site="whsmith")) == \
            'http://www.whsmith.co.uk/CatalogAndSearch/SearchWithinCategory.aspx?as_ISBN=0071148167'

    def test_to_url_invalid_site(self):
        with expect.raises(ValueError, "Unknown site `nosite'."):
            Isbn("0071148167").to_url(site="nosite")

    def test_to_urn(self):
        expect(Isbn("0071148167").to_urn()) == 'URN:ISBN:0071148167'
