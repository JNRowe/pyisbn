#
#
"""test_sbn - Test Sbn class"""
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

from pyisbn import Sbn


class TestSbn():
    def test___repr__(self):
        """Self-documenting string representation.

        >>> Sbn("521871723")
        Sbn('521871723')

        """

    def test_calculate_checksum(self):
        """Calculate SBN checksum.

        >>> Sbn("07114816").calculate_checksum()
        '7'
        >>> Sbn("071148167").calculate_checksum()
        '7'

        """

    def test_convert(self):
        """Convert SBN to ISBN-13.

        >>> Sbn("071148167").convert()
        '9780071148160'

        """
