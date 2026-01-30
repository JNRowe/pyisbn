"""test_sbn - Test Sbn class."""
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

import pytest
from hypothesis import example, given
from hypothesis.strategies import sampled_from

from pyisbn import Sbn
from tests.data import TEST_SBNS


@example("521871723")
@given(sampled_from(TEST_SBNS))
def test___repr__(sbn: str):
    """Test the repr of the Sbn object."""
    assert repr(Sbn(sbn)) == f"Sbn({sbn!r})"


@pytest.mark.parametrize(
    ("sbn", "result"),
    [
        ("07114816", "7"),
        ("071148167", "7"),
    ],
)
def test_calculate_checksum(sbn: str, result: str):
    """Test calculating the checksum of an SBN."""
    assert Sbn(sbn).calculate_checksum() == result


@example("071148167")
@given(sampled_from(TEST_SBNS))
def test_convert(sbn: str):
    """Test converting an SBN."""
    assert Sbn(sbn).convert()[:-1] == "9780" + sbn[:-1]
