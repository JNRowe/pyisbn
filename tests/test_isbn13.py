"""test_isbn13 - Test Isbn13 class."""
# Copyright © 2012-2025  James Rowe <jnrowe@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
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

from hypothesis import example, given
from hypothesis.strategies import sampled_from

from pyisbn import Isbn13
from tests.data import TEST_ISBN13S


@example("978-052-187-1723")
@given(sampled_from(TEST_ISBN13S))
def test_calculate_checksum(isbn: str):
    """Test calculating the checksum of an ISBN-13."""
    assert Isbn13(isbn).calculate_checksum() == isbn[-1]


@example("9780071148160")
@given(sampled_from(TEST_ISBN13S))
def test_convert(isbn: str):
    """Test converting an ISBN-13."""
    assert Isbn13(isbn).convert()[:-1] == isbn[3:-1]
