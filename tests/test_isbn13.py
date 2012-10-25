#
#
"""test_isbn13 - Test Isbn13 class"""
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

from pyisbn import Isbn13


class TestIsbn13():
    def test_calculate_checksum(self):
        """Calculate ISBN-13 checksum.

        >>> Isbn13("978-052-187-1723").calculate_checksum()
        '3'

        """

    def test_convert(self):
        """Convert ISBN-13 to ISBN-10.

        >>> Isbn13("9780071148160").convert()
        '0071148167'

        """
