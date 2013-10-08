#
# coding=utf-8
"""pyisbn - A module for working with 10- and 13-digit ISBNs"""
# Copyright © 2007, 2008, 2009, 2010, 2011, 2012, 2013  James Rowe <jnrowe@gmail.com>
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

from pyisbn import _version


__version__ = _version.dotted
__date__ = _version.date
__author__ = 'James Rowe <jnrowe@gmail.com>'
__copyright__ = 'Copyright © 2008, 2009, 2010, 2011, 2012  James Rowe'
__license__ = 'GNU General Public License Version 3'
__credits__ = ''
__history__ = 'See git repository'

try:
    from email.utils import parseaddr
except ImportError:  # Python 2.4
    from email.Utils import parseaddr  # NOQA

__doc__ += """.

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

:version: %s
:author: `%s <mailto:%s>`__
:copyright: %s
:status: Stable
:license: %s
""" % ((__version__, ) + parseaddr(__author__) + (__copyright__, __license__))


class CountryError(ValueError):

    """Unknown country value."""


class IsbnError(ValueError):

    """Invalid ISBN string."""


class SiteError(ValueError):

    """Unknown site value."""


class Isbn(object):

    """Class for representing ISBN objects."""

    __slots__ = ('__weakref__', '_isbn', 'isbn')

    def __init__(self, isbn):
        """Initialise a new ``Isbn`` object.

        :param str isbn: ISBN string

        """
        super(Isbn, self).__init__()
        self._isbn = isbn
        if len(isbn) in (9, 12):
            self.isbn = _isbn_cleanse(isbn, False)
        else:
            self.isbn = _isbn_cleanse(isbn)

    def __repr__(self):
        """Self-documenting string representation.

        :rtype: ``str``
        :return: String to recreate ``Isbn`` object

        """
        return '%s(%r)' % (self.__class__.__name__, self.isbn)

    def __str__(self):
        """Pretty printed ISBN string.

        :rtype: ``str``
        :return: Human readable string representation of ``Isbn`` object

        """
        return "ISBN %s" % self._isbn

    def calculate_checksum(self):
        """Calculate ISBN checksum.

        :rtype: ``str``
        :return: ISBN checksum value

        """
        if len(self.isbn) in (9, 12):
            return calculate_checksum(self.isbn)
        else:
            return calculate_checksum(self.isbn[:-1])

    def convert(self, code='978'):
        """Convert ISBNs between ISBN-10 and ISBN-13.

        :param str code: ISBN-13 prefix code
        :rtype: ``str``
        :return: Converted ISBN

        """
        return convert(self.isbn, code)

    def validate(self):
        """Validate an ISBN value.

        :rtype: ``bool``
        :return: ``True`` if ISBN is valid

        """
        return validate(self.isbn)

    def to_url(self, site='amazon', country='us'):
        """Generate a link to an online book site.

        :param str site: Site to create link to
        :param str country: Country specific version of ``site``
        :rtype: ``str``
        :return: URL on ``site`` for book
        :raise SiteError: Unknown site value
        :raise CountryError: Unknown country value

        """
        if site == 'amazon':
            if country in ('de', 'fr', 'jp'):
                pass
            elif country == 'uk':
                country = 'co.uk'
            elif country == 'us':
                country = 'com'
            else:
                raise CountryError(country)
            return 'http://amazon.%s/dp/%s' % (country, self.isbn)
        elif site == 'google':
            return 'http://books.google.com/books?vid=isbn:%s' % self.isbn
        elif site == 'isbndb':
            return 'http://isbndb.com/search-all.html?kw=%s' % self.isbn
        elif site == 'worldcat':
            return 'http://worldcat.org/isbn/%s' % self.isbn
        elif site == 'waterstones':
            return 'http://www.waterstones.com/waterstonesweb/' \
                'advancedSearch.do?buttonClicked=2&isbn=%s' % self.isbn
        elif site == 'whsmith':
            return 'http://www.whsmith.co.uk/CatalogAndSearch/' \
                'SearchWithinCategory.aspx?as_ISBN=%s' % self.isbn
        else:
            raise SiteError(site)

    def to_urn(self):
        """Generate a RFC 3187 URN.

        :rfc:`3187` is the commonly accepted way to use ISBNs as uniform
        resource names.

        :rtype: ``str``
        :return: :rfc:`3187` compliant URN

        """
        return 'URN:ISBN:%s' % self._isbn


class Isbn10(Isbn):

    """Class for representing ISBN-10 objects.

    :seealso: ``Isbn``

    """

    def __init__(self, isbn):
        """Initialise a new ``Isbn10`` object.

        :param str isbn: ISBN-10 string

        """
        super(Isbn10, self).__init__(isbn)

    def calculate_checksum(self):
        """Calculate ISBN-10 checksum.

        :rtype: ``str``
        :return: ISBN-10 checksum value

        """
        return calculate_checksum(self.isbn[:9])

    def convert(self, code='978'):
        """Convert ISBN-10 to ISBN-13.

        :param str code: ISBN-13 prefix code
        :rtype: ``str``
        :return: ISBN-13 string

        """
        return convert(self.isbn, code)


class Sbn(Isbn10):

    """Class for representing SBN objects.

    :seealso: ``Isbn10``

    """

    def __init__(self, sbn):
        """Initialise a new ``Sbn`` object.

        :param str sbn: SBN string

        """
        isbn = '0' + sbn
        super(Sbn, self).__init__(isbn)

    def __repr__(self):
        """Self-documenting string representation.

        :rtype: ``str``
        :return: String to recreate ``Sbn`` object

        """
        return '%s(%r)' % (self.__class__.__name__, self.isbn[1:])

    def calculate_checksum(self):
        """Calculate SBN checksum.

        :rtype: ``str``
        :return: SBN checksum value

        """
        return calculate_checksum(self.isbn[:9])

    def convert(self, code='978'):
        """Convert SBN to ISBN-13.

        :param str code: ISBN-13 prefix code
        :rtype: ``str``
        :return: ISBN-13 string

        """
        return super(Sbn, self).convert(code)


class Isbn13(Isbn):

    """Class for representing ISBN-13 objects.

    :seealso: ``Isbn``

    """

    def __init__(self, isbn):
        """Initialise a new ``Isbn13`` object.

        :param str isbn: ISBN-13 string

        """
        super(Isbn13, self).__init__(isbn)

    def calculate_checksum(self):
        """Calculate ISBN-13 checksum.

        :rtype: ``str``
        :return: ISBN-13 checksum value

        """
        return calculate_checksum(self.isbn[:12])

    def convert(self, code=None):
        """Convert ISBN-13 to ISBN-10.

        :param code: Ignored, only for compatibility with ``Isbn``
        :rtype: ``str``
        :return: ISBN-10 string
        :raise ValueError: When ISBN-13 isn't a Bookland "978" ISBN

        """
        return convert(self.isbn)


def _isbn_cleanse(isbn, checksum=True):
    """Check ISBN is a string, and passes basic sanity checks.

    :param str isbn: SBN, ISBN-10 or ISBN-13
    :param bool checksum: ``True`` if ``isbn`` includes checksum character
    :rtype: ``str``
    :return: ISBN with hyphenation removed, including when called with a SBN
    :raise TypeError: ``isbn`` is not a ``str`` type
    :raise IsbnError: Incorrect length for ``isbn``
    :raise IsbnError: Incorrect SBN or ISBN formatting

    """
    try:
        for dash in ('-','-','–'):
            isbn = isbn.replace(dash, '')
    except AttributeError:
        raise TypeError('ISBN must be a string, received %r' % isbn)
    if not isbn[:-1].isdigit():
        raise IsbnError('non-digit parts')
    if checksum:
        if len(isbn) == 9:
            isbn = "0" + isbn
        if len(isbn) == 10:
            if not (isbn[-1].isdigit() or isbn[-1] in "Xx"):
                raise IsbnError('non-digit or X checksum')
        elif len(isbn) == 13:
            if not isbn[-1].isdigit():
                raise IsbnError('non-digit checksum')
        else:
            raise IsbnError('ISBN must be either 10 or 13 characters long')
    else:
        if len(isbn) == 8:
            isbn = '0' + isbn
        if not isbn[-1].isdigit():
            raise IsbnError('non-digit parts')
        if not len(isbn) in (9, 12):
            raise IsbnError('ISBN must be either 9 or 12 characters long '
                            'without checksum')
    return isbn


def calculate_checksum(isbn):
    """Calculate ISBN checksum.

    :param str isbn: SBN, ISBN-10 or ISBN-13
    :rtype: ``str``
    :return: Checksum for given ISBN or SBN

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

    :note: No attempt to hyphenate converted ISBNs is made, because the
        specification requires that *any* hyphenation must be correct but
        allows ISBNs without hyphenation.

    :param str isbn: SBN, ISBN-10 or ISBN-13
    :param str code: EAN Bookland code
    :rtype: ``str``
    :return: Converted ISBN-10 or ISBN-13
    :raise IsbnError: When ISBN-13 isn't convertible to an ISBN-10

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

    :warn: Publishers have been known to go to press with broken ISBNs, and
        therefore validation failures do not completely guarantee an ISBN is
        incorrectly entered.  It should however be noted that it is massively
        more likely *you* have entered an invalid ISBN than the published ISBN
        is incorrectly produced.  An example of this probability in the real
        world is that `Amazon <http://www.amazon.com/>`__ consider it so
        unlikely that they refuse to search for invalid published ISBNs.

    :param str isbn: SBN, ISBN-10 or ISBN-13
    :rtype: ``bool``
    :return: ``True`` if ISBN is valid

    """
    isbn = _isbn_cleanse(isbn)
    return isbn[-1].upper() == calculate_checksum(isbn[:-1])
