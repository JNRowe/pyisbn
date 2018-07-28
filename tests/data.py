#
# coding=utf-8
"""data - ISBNs for use in tests."""
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

import json


with open('tests/books.json') as f:
    #: Sample book data for use in tests
    TEST_BOOKS = json.load(f)

#: ISBNs from sample book data for use in tests
TEST_ISBNS = [s.replace('-', '') for s in TEST_BOOKS.values()]
#: ISBN 10s from sample book data for use in tests
TEST_ISBN10S = [s for s in TEST_ISBNS if len(s) == 10]
#: ISBN 13s from sample book data for use in tests
TEST_ISBN13S = [s for s in TEST_ISBNS if len(s) == 13]
