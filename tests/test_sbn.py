#
# coding=utf-8
"""test_sbn - Test Sbn class."""
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

from pyisbn import Sbn

from tests.data import TEST_ISBN10S


@mark.parametrize('sbn', [s[1:] for s in TEST_ISBN10S] + ['521871723', ])
def test___repr__(sbn):
    assert repr(Sbn(sbn)) == "Sbn(%r)" % sbn


@mark.parametrize('sbn,result', [
    ('07114816', '7'),
    ('071148167', '7'),
])
def test_calculate_checksum(sbn, result):
    assert Sbn(sbn).calculate_checksum() == result


@mark.parametrize('sbn', [s[1:] for s in TEST_ISBN10S] + ['071148167', ])
def test_convert(sbn):
    assert Sbn(sbn).convert()[:-1] == '9780' + sbn[:-1]
