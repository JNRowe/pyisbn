"""data - ISBNs for use in tests."""
# Copyright © 2017-2025  James Rowe <jnrowe@gmail.com>
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

import json
import pathlib

from pyisbn import _constants  # NoQA: PLC2701

_DATA = pathlib.Path("tests/books.json").read_text(encoding="utf-8")
TEST_BOOKS: dict[str, str] = json.loads(_DATA)

#: ISBNs from sample book data for use in tests
TEST_ISBNS: list[str] = [s.replace("-", "") for s in TEST_BOOKS.values()]
#: ISBN 10s from sample book data for use in tests
TEST_ISBN10S: list[str] = [
    s for s in TEST_ISBNS if len(s) == _constants.ISBN10_LENGTH
]
#: ISBN 13s from sample book data for use in tests
TEST_ISBN13S: list[str] = [
    s for s in TEST_ISBNS if len(s) == _constants.ISBN13_LENGTH
]
#: SBNs from sample book data for use in tests
TEST_SBNS: list[str] = [s[1:] for s in TEST_ISBN10S if s.startswith("0")]
