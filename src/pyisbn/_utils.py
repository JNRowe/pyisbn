"""Internal utilities for ``pyisbn``."""
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


def isbn_cleanse(isbn: TIsbn, *, checksum: bool = True) -> str:  # NoQA: C901, PLR0912
    """Check ISBN is a string, and passes basic sanity checks.

    Args:
        isbn: SBN, ISBN-10 or ISBN-13
        checksum: ``True`` if ``isbn`` includes checksum character

    Returns:
        ISBN with hyphenation removed, including when called with a SBN

    Raises:
        TypeError: ``isbn`` is not a ``str`` type
        IsbnError: Incorrect length for ``isbn``
        IsbnError: Incorrect SBN or ISBN formatting

    """
    if not isinstance(isbn, str):
        raise TypeError(f"ISBN must be a string, received {isbn!r}")

    for dash in _constants.DASHES:
        isbn = isbn.replace(dash, "")

    if checksum:
        if not isbn[:-1].isdigit():
            raise IsbnError("non-digit parts")
        if len(isbn) == _constants.SBN_LENGTH:
            isbn = "0" + isbn
        if len(isbn) == _constants.ISBN10_LENGTH:
            if not (isbn[-1].isdigit() or isbn[-1] in "Xx"):
                raise IsbnError("non-digit or X checksum")
        elif len(isbn) == _constants.ISBN13_LENGTH:
            if not isbn[-1].isdigit():
                raise IsbnError("non-digit checksum")
            if not isbn.startswith(_constants.BOOKLAND_PREFIXES):
                raise IsbnError("invalid Bookland region")
        else:
            raise IsbnError("ISBN must be either 10 or 13 characters long")
    else:
        if len(isbn) == _constants.SBN_LENGTH_NO_CHECKSUM:
            isbn = "0" + isbn
        elif len(isbn) == _constants.ISBN13_LENGTH_NO_CHECKSUM and not isbn[
            :3
        ].startswith(_constants.BOOKLAND_PREFIXES):
            raise IsbnError("invalid Bookland region")
        if not isbn.isdigit():
            raise IsbnError("non-digit parts")
        if len(isbn) not in {
            _constants.ISBN10_LENGTH_NO_CHECKSUM,
            _constants.ISBN13_LENGTH_NO_CHECKSUM,
        }:
            raise IsbnError(
                "ISBN must be either 9 or 12 characters long without checksum"
            )
    return isbn
