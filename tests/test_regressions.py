#
# coding=utf-8
"""test_regressions - Test for regressions."""
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

import unicodedata

try:
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase

from pyisbn import _isbn_cleanse


class TestRegressions(TestCase):
    def test_issue_7_unistr(self):
        # The lookup hoop jumping here is to make it easier to generate native
        # Unicode types on the various supported Python versions.
        for isbn in [
                    '978-1-84724-253-2',
                    unicodedata.lookup('EN DASH').join(['978', '1', '84724',
                                                        '253', '2']),
                    unicodedata.lookup('HORIZONTAL BAR').join(['978',
                                                               '0199564095']),
                ]:
            with self.subTest(isbn):
                self.assertEqual(_isbn_cleanse(isbn),
                                 "".join(filter(lambda s: s.isdigit(), isbn)))
