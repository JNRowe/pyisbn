"""test_func - Test function interface."""
# Copyright © 2026-2026  James Rowe <jnrowe@gmail.com>
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

import pytest
from hypothesis import given
from hypothesis.strategies import sampled_from

from pyisbn import (
    IsbnError,
    calculate_checksum,
    convert,
    validate,
)
from tests.data import TEST_ISBNS


@given(sampled_from(TEST_ISBNS))
def test_calculate_checksum(isbn: str):
    """Test calculating the checksum."""
    assert calculate_checksum(isbn[:-1]) == isbn[-1]


@given(sampled_from(TEST_ISBNS))
def test_convert(isbn: str):
    """Test converting an ISBN."""
    assert convert(convert(isbn)) == isbn


def test_convert_invalid():
    """Test converting an invalid ISBN."""
    with pytest.raises(
        IsbnError,
        match="Only ISBN-13s with 978 Bookland code can be converted",
    ):
        convert("9790000000001")


@given(sampled_from(TEST_ISBNS))
def test_validate(isbn: str):
    """Test validating an ISBN."""
    assert validate(isbn)


@pytest.mark.parametrize(
    "isbn",
    [
        "1-234-56789-0",
        "2-345-6789-1",
        "3-456-7890-X",
    ],
)
def test_validate_invalid(isbn: str):
    """Test validating an invalid ISBN."""
    assert validate(isbn) is False
