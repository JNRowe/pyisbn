#
# coding=utf-8
"""test_isbn13 - Test Isbn13 class"""
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

from pyisbn import Isbn13


class TestIsbn13(TestCase):
    def test_calculate_checksum(self):
        expect(Isbn13('978-052-187-1723').calculate_checksum()) == '3'

    def test_convert(self):
        expect(Isbn13('9780071148160').convert()) == '0071148167'
