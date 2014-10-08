#
# coding=utf-8
"""test_isbn10 - Test Isbn10 class."""
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

from pyisbn import Isbn10


class TestIsbn10(TestCase):
    def test_calculate_checksum(self):
        self.assertEqual(Isbn10('3540009787').calculate_checksum(), '7')

    def test_convert(self):
        self.assertEqual(Isbn10('0071148167').convert(), '9780071148160')
