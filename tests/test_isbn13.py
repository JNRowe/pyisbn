#
# coding=utf-8
"""test_isbn13 - Test Isbn13 class."""
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

try:
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase

from pyisbn import Isbn13


class TestIsbn13(TestCase):
    def test_calculate_checksum(self):
        self.assertEqual(Isbn13('978-052-187-1723').calculate_checksum(), '3')

    def test_convert(self):
        self.assertEqual(Isbn13('9780071148160').convert(), '0071148167')
