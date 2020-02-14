#
"""pyisbn - A module for working with 10- and 13-digit ISBNs.

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
# Copyright © 2007-2020  James Rowe <jnrowe@gmail.com>
#                        notconfusing <isalix@gmail.com>
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

from . import _version

__version__ = _version.dotted
__date__ = _version.date
__author__ = 'James Rowe <jnrowe@gmail.com>'
__copyright__ = 'Copyright © 2007-2017  James Rowe'
__license__ = 'GNU General Public License Version 3'

import unicodedata
from typing import Any, Dict, List, Optional, Tuple, Union

#: ISBN string type
TIsbn = str
TIsbn10 = TIsbn
TIsbn13 = TIsbn

#: SBN string type
TSbn = str

#: Dash types to accept, and scrub, in ISBN inputs
DASHES: List[str] = [
    unicodedata.lookup(s)
    for s in ('HYPHEN-MINUS', 'EN DASH', 'EM DASH', 'HORIZONTAL BAR')
]

#: Site to URL mappings, broken out for easier extending at runtime
URL_MAP: Dict[str, Union[str, Tuple[str, Dict[str, Optional[str]]]]] = {
    'amazon': (('https://www.amazon.%(tld)s/s'
                '?search-alias=stripbooks&field-isbn=%(isbn)s'), {
                    'de': None,
                    'fr': None,
                    'jp': None,
                    'uk': 'co.uk',
                    'us': 'com',
                }),
    'copac':
    'http://copac.jisc.ac.uk/search?isn=%(isbn)s',
    'google':
    'https://books.google.com/books?vid=isbn:%(isbn)s',
    'isbndb':
    'https://isbndb.com/search/all?query=%(isbn)s',
    'waterstones':
    'https://www.waterstones.com/books/search/term/%(isbn)s',
    'whsmith':
    'https://www.whsmith.co.uk/search/go?w=%(isbn)s&af=cat1:books',
    'worldcat':
    'http://worldcat.org/isbn/%(isbn)s',
}


class PyisbnError(ValueError):
    """Base ``pyisbn`` error."""


class CountryError(PyisbnError):
    """Unknown country value."""


class IsbnError(PyisbnError):
    """Invalid ISBN string."""


class SiteError(PyisbnError):
    """Unknown site value."""


class Isbn:
    """Class for representing ISBN objects."""
    def __init__(self, isbn: TIsbn) -> None:
        """Initialise a new ``Isbn`` object.

        Args:
            isbn: ISBN string

        """
        super(Isbn, self).__init__()
        self._isbn = isbn
        if len(isbn) in (9, 12):
            self.isbn = _isbn_cleanse(isbn, False)
        else:
            self.isbn = _isbn_cleanse(isbn)

    def __repr__(self) -> str:
        """Self-documenting string representation.


        Returns:
            String to recreate ``Isbn`` object

        """
        return f'{self.__class__.__name__}({self.isbn!r})'

    def __str__(self) -> str:
        """Pretty printed ISBN string.

        Returns:
            Human readable string representation of ``Isbn`` object

        """
        return f'ISBN {self._isbn}'

    def __format__(self, format_spec: Optional[str] = None) -> str:
        """Extended pretty printing for ISBN strings.

        Args:
            format_spec: Extended format to use

        Returns:
            Human readable string representation of ``Isbn`` object

        Raises:
            ValueError: Unknown value for ``format_spec``

        """
        if not format_spec:  # default format calls set format_spec to ''
            return str(self)
        elif format_spec == 'url':
            return self.to_url()
        elif format_spec.startswith('url:'):
            parts = format_spec.split(':')[1:]
            site = parts[0]
            if len(parts) > 1:
                country = parts[1]
            else:
                country = 'us'
            return self.to_url(site, country)
        elif format_spec == 'urn':
            return self.to_urn()
        else:
            raise ValueError(f'Unknown format_spec {format_spec!r}')

    def calculate_checksum(self) -> str:
        """Calculate ISBN checksum.

        Returns:
            ISBN checksum value

        """
        if len(self.isbn) in (9, 12):
            return calculate_checksum(self.isbn)
        else:
            return calculate_checksum(self.isbn[:-1])

    def convert(self, code: str = '978') -> str:
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

    def to_url(self, site: str = 'amazon',
               country: Optional[str] = 'us') -> str:
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
            try:
                url, tlds = URL_MAP[site]
            except ValueError:
                tlds = None
                url = URL_MAP[site]
        except KeyError:
            raise SiteError(site)
        inject = {'isbn': self._isbn}
        if tlds:
            if country not in tlds:
                raise CountryError(country)
            tld = tlds[country]
            if not tld:
                tld = country
            inject['tld'] = tld
        return url % inject

    def to_urn(self) -> str:
        """Generate a RFC 3187 URN.

        :rfc:`3187` is the commonly accepted way to use ISBNs as uniform
        resource names.

        Returns:
            :rfc:`3187` compliant URN

        """
        return f'URN:ISBN:{self._isbn}'


class Isbn10(Isbn):
    """Class for representing ISBN-10 objects.

    See also:
        ``Isbn``

    """
    def __init__(self, isbn: TIsbn) -> None:
        """Initialise a new ``Isbn10`` object.

        Args:
            isbn (str): ISBN-10 string

        """
        super(Isbn10, self).__init__(isbn)

    def calculate_checksum(self) -> str:
        """Calculate ISBN-10 checksum.

        Returns:
            ISBN-10 checksum value

        """
        return calculate_checksum(self.isbn[:9])

    def convert(self, code: str = '978') -> str:
        """Convert ISBN-10 to ISBN-13.

        Args:
            code: ISBN-13 prefix code

        Returns:
            ISBN-13 string

        """
        return convert(self.isbn, code)


class Sbn(Isbn10):
    """Class for representing SBN objects.

    See also:
        ``Isbn10``

    """
    def __init__(self, sbn: TSbn) -> None:
        """Initialise a new ``Sbn`` object.

        Args:
            sbn: SBN string

        """
        isbn = '0' + sbn
        super(Sbn, self).__init__(isbn)

    def __repr__(self) -> str:
        """Self-documenting string representation.

        Returns:
            String to recreate ``Sbn`` object

        """
        return f'{self.__class__.__name__}({self.isbn[1:]!r})'

    def calculate_checksum(self) -> str:
        """Calculate SBN checksum.

        Returns:
            SBN checksum value

        """
        return calculate_checksum(self.isbn[:9])

    def convert(self, code: str = '978') -> str:
        """Convert SBN to ISBN-13.

        Args:
            code: ISBN-13 prefix code

        Returns:
            ISBN-13 string

        """
        return super(Sbn, self).convert(code)


class Isbn13(Isbn):
    """Class for representing ISBN-13 objects.

    See also:
        ``Isbn``

    """
    def __init__(self, isbn: TIsbn13) -> None:
        """Initialise a new ``Isbn13`` object.

        Args:
            isbn: ISBN-13 string

        """
        super(Isbn13, self).__init__(isbn)

    def calculate_checksum(self) -> str:
        """Calculate ISBN-13 checksum.

        Returns:
            ISBN-13 checksum value

        """
        return calculate_checksum(self.isbn[:12])

    def convert(self, code: Any = None) -> str:
        """Convert ISBN-13 to ISBN-10.

        Args:
            code: Ignored, only for compatibility with ``Isbn``

        Returns:
            ISBN-10 string

        Raises:
            ValueError: When ISBN-13 isn't a Bookland "978" ISBN

        """
        return convert(self.isbn)


def _isbn_cleanse(isbn: TIsbn, checksum: bool = True) -> str:
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
        raise TypeError(f'ISBN must be a string, received {isbn!r}')

    for dash in DASHES:
        isbn = isbn.replace(dash, '')

    if checksum:
        if not isbn[:-1].isdigit():
            raise IsbnError('non-digit parts')
        if len(isbn) == 9:
            isbn = '0' + isbn
        if len(isbn) == 10:
            if not (isbn[-1].isdigit() or isbn[-1] in 'Xx'):
                raise IsbnError('non-digit or X checksum')
        elif len(isbn) == 13:
            if not isbn[-1].isdigit():
                raise IsbnError('non-digit checksum')
            if not isbn.startswith(('978', '979')):
                raise IsbnError('invalid Bookland region')
        else:
            raise IsbnError('ISBN must be either 10 or 13 characters long')
    else:
        if len(isbn) == 8:
            isbn = '0' + isbn
        elif len(isbn) == 12 and not isbn[:3].startswith(('978', '979')):
            raise IsbnError('invalid Bookland region')
        if not isbn.isdigit():
            raise IsbnError('non-digit parts')
        if not len(isbn) in (9, 12):
            raise IsbnError('ISBN must be either 9 or 12 characters long '
                            'without checksum')
    return isbn


def calculate_checksum(isbn: TIsbn) -> str:
    """Calculate ISBN checksum.

    Args:
        isbn: SBN, ISBN-10 or ISBN-13

    Returns:
        Checksum for given ISBN or SBN

    """
    digits = [int(i) for i in _isbn_cleanse(isbn, checksum=False)]
    if len(digits) == 9:
        products = [x * y for x, y in enumerate(digits, 1)]
        check = sum(products) % 11
        if check == 10:
            check = 'X'
    else:
        products = [(x if n % 2 == 0 else x * 3) for n, x in enumerate(digits)]
        check = 10 - sum(products) % 10
        if check == 10:
            check = 0
    return str(check)


def convert(isbn: TIsbn, code: str = '978') -> str:
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

    Raise:
        IsbnError: When ISBN-13 isn't convertible to an ISBN-10

    """
    isbn = _isbn_cleanse(isbn)
    if len(isbn) == 10:
        isbn = code + isbn[:-1]
        return isbn + calculate_checksum(isbn)
    else:
        if isbn.startswith('978'):
            return isbn[3:-1] + calculate_checksum(isbn[3:-1])
        else:
            raise IsbnError('Only ISBN-13s with 978 Bookland code can be '
                            'converted to ISBN-10.')


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
    isbn = _isbn_cleanse(isbn)
    return isbn[-1].upper() == calculate_checksum(isbn[:-1])
