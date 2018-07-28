#
# coding=utf-8
"""pyisbn - A module for working with 10- and 13-digit ISBNs.

This module supports the calculation of ISBN checksums with
``calculate_checksum()``, the conversion between ISBN-10 and ISBN-13 with
``convert()`` and the validation of ISBNs with ``validate()``.

All the ISBNs must be passed in as ``str`` types, even if it would seem
reasonable to accept some ``int`` forms.  The reason behind this is English
speaking countries use ``0`` for their group identifier, and Python would treat
ISBNs beginning with ``0`` as octal representations producing incorrect
results.  While it may be feasible to allow some cases as non-``str`` types the
complexity in design and usage isn't worth the minimal benefit.

The functions in this module also support 9-digit SBNs for people with older
books in their collection.
"""
# Copyright © 2007-2018  James Rowe <jnrowe@gmail.com>
#                        notconfusing <isalix@gmail.com>
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

from pyisbn import _version


__version__ = _version.dotted
__date__ = _version.date
__author__ = 'James Rowe <jnrowe@gmail.com>'
__copyright__ = 'Copyright © 2007-2017  James Rowe'
__license__ = 'GNU General Public License Version 3'

import unicodedata

from sys import version_info

PY2 = version_info[0] == 2

if PY2:  # pragma: Python 2
    string_types = (str, unicode)
else:  # pragma: Python 3
    string_types = (str, )
    unicode = str

#: Dash types to accept, and scrub, in ISBN inputs
DASHES = [unicodedata.lookup(s) for s in ('HYPHEN-MINUS', 'EN DASH', 'EM DASH',
                                          'HORIZONTAL BAR')]

#: Site to URL mappings, broken out for easier extending at runtime
URL_MAP = {
    'amazon': (
        ('https://www.amazon.%(tld)s/s'
         '?search-alias=stripbooks&field-isbn=%(isbn)s'),
        {
            'de': None,
            'fr': None,
            'jp': None,
            'uk': 'co.uk',
            'us': 'com',
        }),
    'copac': 'http://copac.jisc.ac.uk/search?isn=%(isbn)s',
    'google': 'https://books.google.com/books?vid=isbn:%(isbn)s',
    'isbndb': 'https://isbndb.com/search/all?query=%(isbn)s',
    'waterstones': 'https://www.waterstones.com/books/search/term/%(isbn)s',
    'whsmith': 'https://www.whsmith.co.uk/search/go?w=%(isbn)s&af=cat1:books',
    'worldcat': 'http://worldcat.org/isbn/%(isbn)s',
}


class PyisbnError(ValueError):

    """Base ``pyisbn`` error."""


class CountryError(PyisbnError):

    """Unknown country value."""


class IsbnError(PyisbnError):

    """Invalid ISBN string."""


class SiteError(PyisbnError):

    """Unknown site value."""


class Isbn(object):

    """Class for representing ISBN objects."""

    __slots__ = ('__weakref__', '_isbn', 'isbn')

    def __init__(self, isbn):
        """Initialise a new ``Isbn`` object.

        Args:
            isbn (str): ISBN string

        """
        super(Isbn, self).__init__()
        self._isbn = isbn
        if len(isbn) in (9, 12):
            self.isbn = _isbn_cleanse(isbn, False)
        else:
            self.isbn = _isbn_cleanse(isbn)

    def __repr__(self):
        """Self-documenting string representation.


        Returns:
            ``str``: String to recreate ``Isbn`` object

        """
        return '%s(%r)' % (self.__class__.__name__, self.isbn)

    def __str__(self):
        """Pretty printed ISBN string.

        Returns:
            ``str``: Human readable string representation of ``Isbn`` object

        """
        return 'ISBN %s' % self._isbn

    def __format__(self, format_spec=None):
        """Extended pretty printing for ISBN strings.

        Args:
            format_spec (str): Extended format to use

        Returns:
            ``str``: Human readable string representation of ``Isbn`` object

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
            raise ValueError('Unknown format_spec %r' % format_spec)

    def calculate_checksum(self):
        """Calculate ISBN checksum.

        Returns:
            ``str``: ISBN checksum value

        """
        if len(self.isbn) in (9, 12):
            return calculate_checksum(self.isbn)
        else:
            return calculate_checksum(self.isbn[:-1])

    def convert(self, code='978'):
        """Convert ISBNs between ISBN-10 and ISBN-13.

        Args:
            code (str): ISBN-13 prefix code

        Returns:
            ``str``: Converted ISBN

        """
        return convert(self.isbn, code)

    def validate(self):
        """Validate an ISBN value.

        Returns:
            ``bool``: ``True`` if ISBN is valid

        """
        return validate(self.isbn)

    def to_url(self, site='amazon', country='us'):
        """Generate a link to an online book site.

        Args:
            site (str): Site to create link to
            country (str): Country specific version of ``site``

        Returns:
            ``str``: URL on ``site`` for book

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

    def to_urn(self):
        """Generate a RFC 3187 URN.

        :rfc:`3187` is the commonly accepted way to use ISBNs as uniform
        resource names.

        Returns:
            ``str``: :rfc:`3187` compliant URN

        """
        return 'URN:ISBN:%s' % self._isbn


class Isbn10(Isbn):

    """Class for representing ISBN-10 objects.

    See also:
        ``Isbn``

    """

    def __init__(self, isbn):
        """Initialise a new ``Isbn10`` object.

        Args:
            isbn (str): ISBN-10 string

        """
        super(Isbn10, self).__init__(isbn)

    def calculate_checksum(self):
        """Calculate ISBN-10 checksum.

        Returns:
            ``str``: ISBN-10 checksum value

        """
        return calculate_checksum(self.isbn[:9])

    def convert(self, code='978'):
        """Convert ISBN-10 to ISBN-13.

        Args:
            code (str): ISBN-13 prefix code

        Returns:
            ``str``: ISBN-13 string

        """
        return convert(self.isbn, code)


class Sbn(Isbn10):

    """Class for representing SBN objects.

    See also:
        ``Isbn10``

    """

    def __init__(self, sbn):
        """Initialise a new ``Sbn`` object.

        Args:
            sbn (str): SBN string

        """
        isbn = '0' + sbn
        super(Sbn, self).__init__(isbn)

    def __repr__(self):
        """Self-documenting string representation.

        Returns:
            ``str``: String to recreate ``Sbn`` object

        """
        return '%s(%r)' % (self.__class__.__name__, self.isbn[1:])

    def calculate_checksum(self):
        """Calculate SBN checksum.

        Returns:
            ``str``: SBN checksum value

        """
        return calculate_checksum(self.isbn[:9])

    def convert(self, code='978'):
        """Convert SBN to ISBN-13.

        Args:
            code (str): ISBN-13 prefix code

        Returns:
            ``str``: ISBN-13 string

        """
        return super(Sbn, self).convert(code)


class Isbn13(Isbn):

    """Class for representing ISBN-13 objects.

    See also:
        ``Isbn``

    """

    def __init__(self, isbn):
        """Initialise a new ``Isbn13`` object.

        Args:
            isbn (str): ISBN-13 string

        """
        super(Isbn13, self).__init__(isbn)

    def calculate_checksum(self):
        """Calculate ISBN-13 checksum.

        Returns:
            ``str``: ISBN-13 checksum value

        """
        return calculate_checksum(self.isbn[:12])

    def convert(self, code=None):
        """Convert ISBN-13 to ISBN-10.

        Args:
            code: Ignored, only for compatibility with ``Isbn``

        Returns:
            ``str``: ISBN-10 string

        Raises:
            ValueError: When ISBN-13 isn't a Bookland "978" ISBN

        """
        return convert(self.isbn)


def _isbn_cleanse(isbn, checksum=True):
    """Check ISBN is a string, and passes basic sanity checks.

    Args:
        isbn (str): SBN, ISBN-10 or ISBN-13
        checksum (bool): ``True`` if ``isbn`` includes checksum character

    Returns:
        ``str``: ISBN with hyphenation removed, including when called with a
            SBN

    Raises:
        TypeError: ``isbn`` is not a ``str`` type
        IsbnError: Incorrect length for ``isbn``
        IsbnError: Incorrect SBN or ISBN formatting

    """
    if not isinstance(isbn, string_types):
        raise TypeError('ISBN must be a string, received %r' % isbn)

    if PY2 and isinstance(isbn, str):  # pragma: Python 2
        isbn = unicode(isbn)
        uni_input = False
    else:  # pragma: Python 3
        uni_input = True

    for dash in DASHES:
        isbn = isbn.replace(dash, unicode())

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
        else:
            raise IsbnError('ISBN must be either 10 or 13 characters long')
    else:
        if len(isbn) == 8:
            isbn = '0' + isbn
        if not isbn.isdigit():
            raise IsbnError('non-digit parts')
        if not len(isbn) in (9, 12):
            raise IsbnError('ISBN must be either 9 or 12 characters long '
                            'without checksum')
    if PY2 and not uni_input:  # pragma: Python 2
        # Sadly, type ping-pong is required to maintain backwards compatibility
        # with previous pyisbn releases for Python 2 users.
        return str(isbn)
    else:  # pragma: Python 3
        return isbn


def calculate_checksum(isbn):
    """Calculate ISBN checksum.

    Args:
        isbn (str): SBN, ISBN-10 or ISBN-13

    Returns:
        ``str``: Checksum for given ISBN or SBN

    """
    isbn = [int(i) for i in _isbn_cleanse(isbn, checksum=False)]
    if len(isbn) == 9:
        products = [x * y for x, y in zip(isbn, range(1, 10))]
        check = sum(products) % 11
        if check == 10:
            check = 'X'
    else:
        # As soon as Python 2.4 support is dumped
        # [(isbn[i] if i % 2 == 0 else isbn[i] * 3) for i in range(12)]
        products = []
        for i in range(12):
            if i % 2 == 0:
                products.append(isbn[i])
            else:
                products.append(isbn[i] * 3)
        check = 10 - sum(products) % 10
        if check == 10:
            check = 0
    return str(check)


def convert(isbn, code='978'):
    """Convert ISBNs between ISBN-10 and ISBN-13.

    Note:
        No attempt to hyphenate converted ISBNs is made, because the
        specification requires that *any* hyphenation must be correct but
        allows ISBNs without hyphenation.

    Args:
        isbn (str): SBN, ISBN-10 or ISBN-13
        code (str): EAN Bookland code

    Returns:
        ``str``: Converted ISBN-10 or ISBN-13

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


def validate(isbn):
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
        isbn (str): SBN, ISBN-10 or ISBN-13

    Returns:
        ``bool``: ``True`` if ISBN is valid

    """
    isbn = _isbn_cleanse(isbn)
    return isbn[-1].upper() == calculate_checksum(isbn[:-1])
