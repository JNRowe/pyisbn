"""test_functions - Test internal functions."""
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

from pyisbn import IsbnError
from pyisbn._utils import isbn_cleanse  # NoQA: PLC2701
from tests.data import TEST_ISBNS


@given(sampled_from(TEST_ISBNS))
def test__isbn_cleanse_sbn(isbn: str):
    """Test cleansing SBNs."""
    if isbn.startswith("0"):
        assert isbn_cleanse(isbn[1:]) == isbn
        assert isbn_cleanse(isbn[1:-1], checksum=False) == isbn[:-1]


@given(sampled_from(TEST_ISBNS))
def test__isbn_cleanse_isbn(isbn: str):
    """Test cleansing ISBNs."""
    assert isbn_cleanse(isbn) == isbn
    assert isbn_cleanse(isbn[:-1], checksum=False) == isbn[:-1]


# See tests.test_regressions.test_issue_7_unistr
# NOTE: Depending on your typeface and editor you may notice that the following
# dashes are not HYPHEN-MINUS.  They're not, and this is on purpose
@pytest.mark.parametrize(
    "isbn",
    [
        "978–1–84724–253–2",  # NoQA: RUF001
        "978—0—385—08695—0",
        "978―0199564095",
    ],
)
def test__isbn_cleanse_unicode_dash(isbn: str):
    """Test cleansing ISBNs with unicode dashes."""
    assert isbn_cleanse(isbn) == "".join(filter(lambda s: s.isdigit(), isbn))


# NOTE: Depending on your typeface and editor you may notice that the following
# dashes are not HYPHEN-MINUS.  They're not, and this is on purpose
@pytest.mark.parametrize(
    "isbn",
    [
        "978–1–84724–253–2",  # NoQA: RUF001
        "978-0-385-08695-0",
    ],
)
def test__isbn_cleanse_reflect_type(isbn: str):
    """Test that the cleansed ISBN has the same type as the original."""
    assert type(isbn_cleanse(isbn)) is type(isbn)


def test__isbn_cleanse_invalid_type():
    """Test cleansing an invalid type."""
    with pytest.raises(TypeError, match="ISBN must be a string, received 2"):
        isbn_cleanse(2)  # ty: ignore[invalid-argument-type]


@pytest.mark.parametrize(
    ("checksum", "message"),
    [
        (True, "ISBN must be either 10 or 13 characters long"),
        (
            False,
            "ISBN must be either 9 or 12 characters long without checksum",
        ),
    ],
)
def test__isbn_cleanse_invalid_length(
    checksum: bool,  # NoQA: FBT001
    message: str,
):
    """Test cleansing an invalid length."""
    with pytest.raises(IsbnError, match=message):
        isbn_cleanse("0-123", checksum=checksum)


@pytest.mark.parametrize(
    ("isbn", "message"),
    [
        ("0-x4343", "non-digit parts"),
        ("012345678-b", "non-digit or X checksum"),
        ("012345678901b", "non-digit checksum"),
        ("xxxxxxxxxxxx1", "non-digit parts"),
        ("0x0000000", "non-digit parts"),
    ],
)
def test__isbn_cleanse_invalid(isbn: str, message: str):
    """Test cleansing an invalid ISBN."""
    with pytest.raises(IsbnError, match=message):
        isbn_cleanse(isbn)


@pytest.mark.parametrize(
    ("isbn", "message"),
    [
        ("0x0000000", "non-digit parts"),
        ("580003417076", "invalid Bookland region"),
    ],
)
def test__isbn_cleanse_invalid_no_checksum(isbn: str, message: str):
    """Test cleansing an invalid ISBN without checksum."""
    with pytest.raises(IsbnError, match=message):
        isbn_cleanse(isbn, checksum=False)
