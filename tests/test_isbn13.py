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
#
# SPDX-License-Identifier: GPL-3.0+

from pytest import mark

from pyisbn import Isbn13

from tests.data import TEST_ISBN13S


@mark.parametrize('isbn', TEST_ISBN13S + ['978-052-187-1723', ])
def test_calculate_checksum(isbn):
    assert Isbn13(isbn).calculate_checksum() == isbn[-1]


@mark.parametrize('isbn', TEST_ISBN13S + ['9780071148160', ])
def test_convert(isbn):
    assert Isbn13(isbn).convert()[:-1] == isbn[3:-1]
