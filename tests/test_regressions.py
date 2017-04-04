#
# coding=utf-8
"""test_regressions - Test for regressions"""
# Copyright © 2007-2017  James Rowe <jnrowe@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import unicodedata

from expecter import expect
from nose2.tools import params

from pyisbn import _isbn_cleanse


# The lookup hoop jumping here is make it easier to generate native Unicode
# types on the various supported Python versions.
@params(
    '978-1-84724-253-2',
    unicodedata.lookup('EN DASH').join(['978', '1', '84724', '253', '2']),
    unicodedata.lookup('HORIZONTAL BAR').join(['978', '0199564095']),
)
def test_issue_7_unistr(isbn):
    expect(_isbn_cleanse(isbn)) == "".join(filter(lambda s: s.isdigit(), isbn))
