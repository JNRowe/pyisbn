#
"""test_meta - Tests for project maintenance."""
# Copyright © 2012-2021  James Rowe <jnrowe@gmail.com>
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
import os

from pytest import mark


@mark.skipif(
    'GITHUB_WORKFLOW' in os.environ,
    reason='Maintainer test for use in git hooks',
)
def test_formatting():
    with open('tests/books.json') as fp:
        data = fp.read()
    content = json.loads(data)
    dumped = json.dumps(content, indent=4) + "\n"
    assert data == dumped
