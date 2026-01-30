"""Model interface to ``pyisbn``.

This module supports the calculation and validation of ISBN checksums with
various classes.

.. note::

    All the ISBNs must be passed in as ``str`` types, even if it would seem
    reasonable to accept some ``int`` forms.  The reason behind this is English
    speaking countries use ``0`` for their group identifier, and Python 3 would
    treat this as a syntax error [#]_.  While it may be feasible to allow some
    cases as non-``str`` types the complexity in design and usage isn't worth
    the minimal benefit.

There is support for SBNs in this module also to people with older books in
their collection.

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
from ._exceptions import CountryError, SiteError
from ._types import TIsbn, TIsbn13, TSbn
from ._utils import isbn_cleanse
from .func import calculate_checksum, convert, validate


class Isbn:
    """Class for representing ISBN objects."""

    def __init__(self, isbn: TIsbn) -> None:
        """Initialise a new ``Isbn`` object.

        Args:
            isbn: ISBN string

        """
        self._isbn = isbn
        if len(isbn) in {
            _constants.SBN_LENGTH,
            _constants.ISBN13_LENGTH_NO_CHECKSUM,
        }:
            self.isbn = isbn_cleanse(isbn, checksum=False)
        else:
            self.isbn = isbn_cleanse(isbn)

    def __repr__(self) -> str:
        """Self-documenting string representation.

        Returns:
            String to recreate ``Isbn`` object

        """
        return f"{self.__class__.__name__}({self.isbn!r})"

    def __str__(self) -> str:
        """Pretty printed ISBN string.

        Returns:
            Human readable string representation of ``Isbn`` object

        """
        return f"ISBN {self._isbn}"

    def __format__(self, format_spec: str | None = None) -> str:
        """Extended pretty printing for ISBN strings.

        Args:
            format_spec: Extended format to use

        Returns:
            Human readable string representation of ``Isbn`` object

        Raises:
            ValueError: Unknown value for ``format_spec``

        """
        match format_spec:
            case None | "":
                return str(self)
            case "url":
                return self.to_url()
            case "urn":
                return self.to_urn()
            case s if s.startswith("url:"):
                parts = s.split(":")
                site = parts[1]
                try:
                    country = parts[2]
                except IndexError:
                    country = "us"
                return self.to_url(site, country)
            case _:
                raise ValueError(f"Unknown format_spec {format_spec!r}")

    def calculate_checksum(self) -> str:
        """Calculate ISBN checksum.

        Returns:
            ISBN checksum value

        """
        if len(self.isbn) in {
            _constants.SBN_LENGTH,
            _constants.ISBN13_LENGTH_NO_CHECKSUM,
        }:
            return calculate_checksum(self.isbn)
        return calculate_checksum(self.isbn[:-1])

    def convert(self, code: str = "978") -> str:
        """Convert ISBNs between ISBN-10 and ISBN-13.

        Args:
            code: ISBN-13 prefix code

        Returns:
            Converted ISBN

        """
        return convert(self.isbn, code)

    def validate(self) -> bool:
        """Validate an ISBN value.

        Returns:
            ``True`` if ISBN is valid

        """
        return validate(self.isbn)

    def to_url(self, site: str = "amazon", country: str | None = "us") -> str:
        """Generate a link to an online book site.

        Args:
            site: Site to create link to
            country: Country specific version of ``site``

        Returns:
            URL on ``site`` for book

        Raises:
            SiteError: Unknown site value
            CountryError: Unknown country value

        """
        try:
            value = _constants.URL_MAP[site]
        except KeyError:
            raise SiteError(site) from KeyError

        if isinstance(value, tuple):
            url, tlds = value
        else:
            url, tlds = value, None

        inject = {"isbn": self._isbn}
        if tlds:
            if country not in tlds:
                raise CountryError(country)
            tld = tlds[country]
            if not tld:
                tld = country
            inject["tld"] = tld
        return url.format_map(inject)

    def to_urn(self) -> str:
        """Generate a RFC 3187 URN.

        :rfc:`3187` is the commonly accepted way to use ISBNs as uniform
        resource names.

        Returns:
            :rfc:`3187` compliant URN

        """
        return f"URN:ISBN:{self._isbn}"


class Isbn10(Isbn):
    """Class for representing ISBN-10 objects.

    See Also:
        :class:`Isbn`

    """

    def __init__(self, isbn: TIsbn) -> None:
        """Initialise a new ``Isbn10`` object.

        Args:
            isbn (str): ISBN-10 string

        """
        super().__init__(isbn)

    def calculate_checksum(self) -> str:
        """Calculate ISBN-10 checksum.

        Returns:
            ISBN-10 checksum value

        """
        return calculate_checksum(
            self.isbn[: _constants.ISBN10_LENGTH_NO_CHECKSUM]
        )

    def convert(self, code: str = "978") -> str:
        """Convert ISBN-10 to ISBN-13.

        Args:
            code: ISBN-13 prefix code

        Returns:
            ISBN-13 string

        """
        return convert(self.isbn, code)


class Sbn(Isbn10):
    """Class for representing SBN objects.

    See Also:
        :class:`Isbn10`

    """

    def __init__(self, sbn: TSbn) -> None:
        """Initialise a new ``Sbn`` object.

        Args:
            sbn: SBN string

        """
        isbn = "0" + sbn
        super().__init__(isbn)

    def __repr__(self) -> str:
        """Self-documenting string representation.

        Returns:
            String to recreate ``Sbn`` object

        """
        return f"{self.__class__.__name__}({self.isbn[1:]!r})"

    def calculate_checksum(self) -> str:
        """Calculate SBN checksum.

        Returns:
            SBN checksum value

        """
        return calculate_checksum(
            self.isbn[: _constants.ISBN10_LENGTH_NO_CHECKSUM]
        )

    def convert(self, code: str = "978") -> str:
        """Convert SBN to ISBN-13.

        Args:
            code: ISBN-13 prefix code

        Returns:
            ISBN-13 string

        """
        return super().convert(code)


class Isbn13(Isbn):
    """Class for representing ISBN-13 objects.

    See Also:
        :class:`Isbn`

    """

    def __init__(self, isbn: TIsbn13) -> None:
        """Initialise a new ``Isbn13`` object.

        Args:
            isbn: ISBN-13 string

        """
        super().__init__(isbn)

    def calculate_checksum(self) -> str:
        """Calculate ISBN-13 checksum.

        Returns:
            ISBN-13 checksum value

        """
        return calculate_checksum(
            self.isbn[: _constants.ISBN13_LENGTH_NO_CHECKSUM]
        )

    def convert(self, _code: str = "978") -> str:
        """Convert ISBN-13 to ISBN-10.

        Args:
            _code: Ignored, only for compatibility with ``Isbn``

        Returns:
            ISBN-10 string

        Raises:
            ValueError: When ISBN-13 isn't a Bookland "978" ISBN

        """  # NoQA: DOC502
        return convert(self.isbn)
