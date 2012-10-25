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

from pyisbn import Isbn


class TestIsbn():
    def test___repr__(self):
        """Self-documenting string representation.

        >>> Isbn("9780521871723")
        Isbn('9780521871723')
        >>> Isbn("3540009787")
        Isbn('3540009787')

        """

    def test___str__(self):
        """Pretty printed ISBN string.

        >>> print(Isbn("9780521871723"))
        ISBN 9780521871723
        >>> print(Isbn("978-052-187-1723"))
        ISBN 978-052-187-1723
        >>> print(Isbn("3540009787"))
        ISBN 3540009787

        """

    def test_calculate_checksum(self):
        """Calculate ISBN checksum.

        >>> Isbn("978-052-187-1723").calculate_checksum()
        '3'
        >>> Isbn("3540009787").calculate_checksum()
        '7'
        >>> Isbn("354000978").calculate_checksum()
        '7'

        """

    def test_convert(self):
        """Convert ISBNs between ISBN-10 and ISBN-13.

        >>> Isbn("0071148167").convert()
        '9780071148160'
        >>> Isbn("9780071148160").convert()
        '0071148167'

        :param str code: ISBN-13 prefix code
        :rtype: ``str``
        :return: Converted ISBN

        """

    def test_validate(self):
        """Validate an ISBN value.

        >>> Isbn("978-052-187-1723").validate()
        True
        >>> Isbn("978-052-187-1720").validate()
        False
        >>> Isbn("3540009787").validate()
        True
        >>> Isbn("354000978x").validate()
        False

        """

    def test_to_url(self):
        """Generate a link to an online book site.

        >>> print(Isbn("0071148167").to_url())
        http://amazon.com/dp/0071148167
        >>> print(Isbn("0071148167").to_url(country="uk"))
        http://amazon.co.uk/dp/0071148167
        >>> print(Isbn("0071148167").to_url(country="de"))
        http://amazon.de/dp/0071148167
        >>> print(Isbn("0071148167").to_url(country="zh"))
        Traceback (most recent call last):
        ...
        ValueError: Unknown site `zh'.
        >>> print(Isbn("0071148167").to_url(site="google"))
        http://books.google.com/books?vid=isbn:0071148167
        >>> print(Isbn("0071148167").to_url(site="isbndb"))
        http://isbndb.com/search-all.html?kw=0071148167
        >>> print(Isbn("0071148167").to_url(site="worldcat"))
        http://worldcat.org/isbn/0071148167
        >>> print(Isbn("0071148167").to_url(site="waterstones"))
        http://www.waterstones.com/waterstonesweb/advancedSearch.do?buttonClicked=2&isbn=0071148167
        >>> print(Isbn("0071148167").to_url(site="whsmith"))
        http://www.whsmith.co.uk/CatalogAndSearch/SearchWithinCategory.aspx?as_ISBN=0071148167
        >>> print(Isbn("0071148167").to_url(site="nosite"))
        Traceback (most recent call last):
        ...
        ValueError: Unknown site `nosite'.

        """

    def test_to_urn(self):
        """Generate a RFC 3187 URN.

        >>> print(Isbn("0071148167").to_urn())
        URN:ISBN:0071148167

        """
