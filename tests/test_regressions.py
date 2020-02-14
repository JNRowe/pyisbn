#
"""test_regressions - Test for regressions."""
# Copyright © 2012-2020  James Rowe <jnrowe@gmail.com>
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

from pytest import mark, raises

from pyisbn import IsbnError, _isbn_cleanse


# NOTE: Depending on your typeface and editor you may notice that the following
# +# dashes are not HYPHEN-MINUS.  They're not, and this is on purpose
@mark.parametrize('isbn', [
    '978-1-84724-253-2',
    '978–1–84724–253–2',
    '978―0199564095',
])
def test_issue_7_unistr(isbn: str):
    assert _isbn_cleanse(isbn) == ''.join(filter(lambda s: s.isdigit(), isbn))


@mark.parametrize('isbn', [
    '2901568582497',
    '5800034170763',
])
def test_issue_16_bookland(isbn: str):
    with raises(IsbnError, match='Bookland'):
        _isbn_cleanse(isbn)
