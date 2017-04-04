#
# coding=utf-8
"""test_isbn10 - Test Isbn10 class"""
# Copyright © 2007-2017  James Rowe <jnrowe@gmail.com>
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

from expecter import expect

from pyisbn import Isbn10


def test_calculate_checksum():
    expect(Isbn10('3540009787').calculate_checksum()) == '7'


def test_convert():
    expect(Isbn10('0071148167').convert()) == '9780071148160'
