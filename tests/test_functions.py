#
# coding=utf-8
"""test_functions - Test function interface."""
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

from expecter import expect

try:
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase

from pyisbn import (IsbnError, _isbn_cleanse, calculate_checksum, convert,
                    validate)
from tests.test_data import TEST_BOOKS


class TestFunctions(TestCase):
    def test__isbn_cleanse_sbn(self):
        for isbn in TEST_BOOKS.values():
            with self.subTest(isbn):
                if isbn.startswith('0'):
                    expect(_isbn_cleanse(isbn[1:])) == isbn.replace('-', '')
                    expect(_isbn_cleanse(isbn[1:-1], False)) \
                        == isbn.replace('-', '')[:-1]

    def test__isbn_cleanse_isbn(self):
        for isbn in TEST_BOOKS.values():
            with self.subTest(isbn):
                expect(_isbn_cleanse(isbn)) == isbn.replace('-', '')
                expect(_isbn_cleanse(isbn[:-1], False)) \
                    == isbn.replace('-', '')[:-1]

    # See tests.test_regressions.test_issue_7_unistr
    def test__isbn_cleanse_unicode_dash(self):
        for isbn in [
                    unicodedata.lookup('EN DASH').join(['978', '1', '84724',
                                                        '253', '2']),
                    unicodedata.lookup('EM DASH').join(['978', '0', '385',
                                                        '08695', '0']),
                    unicodedata.lookup('HORIZONTAL BAR').join(['978',
                                                               '0199564095']),
                ]:
            with self.subTest(isbn):
                expect(_isbn_cleanse(isbn)) \
                    == "".join(filter(lambda s: s.isdigit(), isbn))

    def test__isbn_cleanse_reflect_type(self):
        for isbn in [
                    unicodedata.lookup('EN DASH').join(['978', '1', '84724',
                                                        '253', '2']),
                    '978-0-385-08695-0',
                ]:
            with self.subTest(isbn):
                expect(type(_isbn_cleanse(isbn))) == type(isbn)

    def test__isbn_cleanse_invalid_type(self):
        with expect.raises(TypeError, "ISBN must be a string, received 2"):
            _isbn_cleanse(2)

    def test__isbn_cleanse_invalid_length(self):
        for checksum, message in [
                    (True, 'ISBN must be either 10 or 13 characters long'),
                    (False, 'ISBN must be either 9 or 12 characters long '
                        'without checksum'),
                ]:
            with self.subTest([checksum, message]):
                with expect.raises(IsbnError, message):
                    _isbn_cleanse('0-123', checksum=checksum)

    def test__isbn_cleanse_invalid(self):
        for isbn, message, checksum in [
                    ('0-x4343', 'non-digit parts', True),
                    ('012345678-b', 'non-digit or X checksum', True),
                    ('012345678901b', 'non-digit checksum', True),
                    ('xxxxxxxxxxxx1', 'non-digit parts', True),
                    ('0x0000000', 'non-digit parts', False),
                ]:
            with self.subTest([isbn, message, checksum]):
                with expect.raises(IsbnError, message):
                    _isbn_cleanse(isbn, checksum)

    def test_calculate_checksum(self):
        for isbn in TEST_BOOKS.values():
            with self.subTest(isbn):
                expect(calculate_checksum(isbn[:-1])) == isbn[-1]

    def test_convert(self):
        for isbn in TEST_BOOKS.values():
            with self.subTest(isbn):
                expect(convert(convert(isbn))) == isbn.replace('-', '')

    def test_convert_invalid(self):
        with expect.raises(IsbnError,
                           'Only ISBN-13s with 978 Bookland code can be '
                           'converted to ISBN-10.'):
            convert('0000000000000')

    def test_validate(self):
        for isbn in TEST_BOOKS.values():
            with self.subTest(isbn):
                expect(validate(isbn)) == True

    def test_validate_invalid(self):
        for isbn in [
                    '1-234-56789-0',
                    '2-345-6789-1',
                    '3-456-7890-X',
                ]:
            with self.subTest(isbn):
                expect(validate(isbn)) == False
