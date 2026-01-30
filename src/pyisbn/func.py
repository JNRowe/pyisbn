"""Classic function interface to ``pyisbn``.

This module supports the calculation of ISBN checksums with
``calculate_checksum()``, the conversion between ISBN-10 and ISBN-13 with
``convert()`` and the validation of ISBNs with ``validate()``.

.. note::

    All the ISBNs must be passed in as ``str`` types, even if it would seem
    reasonable to accept some ``int`` forms.  The reason behind this is English
    speaking countries use ``0`` for their group identifier, and Python 3 would
    treat this as a syntax error [#]_.  While it may be feasible to allow some
    cases as non-``str`` types the complexity in design and usage isn't worth
    the minimal benefit.

The functions in this module also support 9-digit SBNs for people with older
books in their collection.

.. [#] Previous Python releases would have assumed it was octal representation
       of a number
"""
# Copyright © 2026-2026  James Rowe <jnrowe@gmail.com>
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

from . import _constants
from ._exceptions import IsbnError
from ._types import TIsbn
from ._utils import isbn_cleanse


def calculate_checksum(isbn: TIsbn) -> str:
    """Calculate ISBN checksum.

    Args:
        isbn: SBN, ISBN-10 or ISBN-13

    Returns:
        Checksum for given ISBN or SBN

    """
    digits = [int(i) for i in isbn_cleanse(isbn, checksum=False)]
    if len(digits) == _constants.ISBN10_LENGTH_NO_CHECKSUM:
        products = [x * y for x, y in enumerate(digits, 1)]
        check = sum(products) % _constants.ISBN10_CHECKSUM_MODULUS
        if check == _constants.ISBN10_CHECKSUM_X:
            check = "X"
    else:
        products = [
            (x if n % 2 == 0 else x * _constants.ISBN13_ODD_MULTIPLIER)
            for n, x in enumerate(digits)
        ]
        check = (
            _constants.ISBN13_CHECKSUM_SUBTRACT
            - sum(products) % _constants.ISBN13_CHECKSUM_MODULUS
        )
        if check == _constants.ISBN13_CHECKSUM_MODULUS:
            check = _constants.ISBN13_CHECKSUM_TEN_REPLACEMENT
    return str(check)


def convert(isbn: TIsbn, code: str = "978") -> str:
    """Convert ISBNs between ISBN-10 and ISBN-13.

    Note:
        No attempt to hyphenate converted ISBNs is made, because the
        specification requires that *any* hyphenation must be correct but
        allows ISBNs without hyphenation.

    Args:
        isbn: SBN, ISBN-10 or ISBN-13
        code: EAN Bookland code

    Returns:
        Converted ISBN-10 or ISBN-13

    Raises:
        IsbnError: When ISBN-13 isn't convertible to an ISBN-10

    """
    isbn = isbn_cleanse(isbn)
    if len(isbn) == _constants.ISBN10_LENGTH:
        isbn = code + isbn[:-1]
        return isbn + calculate_checksum(isbn)
    if isbn.startswith(_constants.BOOKLAND_PREFIXES[0]):
        return isbn[
            _constants.BOOKLAND_PREFIX_LENGTH : -1
        ] + calculate_checksum(isbn[_constants.BOOKLAND_PREFIX_LENGTH : -1])
    raise IsbnError(
        "Only ISBN-13s with 978 Bookland code can be converted to ISBN-10."
    )


def validate(isbn: TIsbn) -> bool:
    """Validate ISBNs.

    Warning:
        Publishers have been known to go to press with broken ISBNs, and
        therefore validation failures do not completely guarantee an ISBN is
        incorrectly entered.  It should however be noted that it is massively
        more likely *you* have entered an invalid ISBN than the published ISBN
        is incorrectly produced.  An example of this probability in the real
        world is that `Amazon <https://www.amazon.com/>`__ consider it so
        unlikely that they refuse to search for invalid published ISBNs.

    Args:
        isbn: SBN, ISBN-10 or ISBN-13

    Returns:
        ``True`` if ISBN is valid

    """
    isbn = isbn_cleanse(isbn)
    return isbn[-1].upper() == calculate_checksum(isbn[:-1])
