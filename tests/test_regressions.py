"""test_regressions - Test for regressions."""
# Copyright © 2013-2026  James Rowe <jnrowe@gmail.com>
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

from pyisbn import IsbnError
from pyisbn._utils import isbn_cleanse  # NoQA: PLC2701


# NOTE: Depending on your typeface and editor you may notice that the following
# +# dashes are not HYPHEN-MINUS.  They're not, and this is on purpose
@pytest.mark.parametrize(
    "isbn",
    [
        "978-1-84724-253-2",
        "978–1–84724–253–2",  # NoQA: RUF001
        "978―0199564095",
    ],
)
def test_issue_7_unistr(isbn: str):
    """Test for issue #7 (unicode dashes)."""
    assert isbn_cleanse(isbn) == "".join(filter(lambda s: s.isdigit(), isbn))


@pytest.mark.parametrize(
    "isbn",
    [
        "2901568582497",
        "5800034170763",
    ],
)
def test_issue_16_bookland(isbn: str):
    """Test for issue #16 (Bookland ISBNs)."""
    with pytest.raises(IsbnError, match="Bookland"):
        isbn_cleanse(isbn)
