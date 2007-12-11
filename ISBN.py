#! /usr/bin/python -tt
# vim: set sw=4 sts=4 et tw=80 fileencoding=utf-8:
#
"""
ISBN - A module for working with 10- and 13-digit ISBNs
"""
# Copyright (C) 2007  James Rowe
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

__version__ = "0.3.0"
__date__ = "2007-05-18"
__author__ = "James Rowe <jnrowe@ukfsn.org>"
__copyright__ = "Copyright (C) 2007 James Rowe"
__license__ = "GNU General Public License Version 3"
__credits__ = ""
__history__ = "See Mercurial repository"

from email.utils import parseaddr

__doc__ += """
This module supports the calculation of ISBN checksums with
C{calculate_checksum()}, the conversion between ISBN-10 and ISBN-13 with
C{convert()} and the validation of ISBNs with C{validate()}.

All the ISBNs must be passed in as C{str} types, even if it would seem
reasonable to accept some C{int} forms.  The reason behind this is English
speaking countries use C{0} for their group identifier, and Python would treat
ISBNs beginning with C{0} as octal representations producing incorrect results.
While it may be feasible to allow some cases as non-C{str} types the complexity
in design and usage isn't worth the minimal benefit.

The functions in this module also support 9-digit SBNs for people with older
books in their collection.

@version: %s
@author: U{%s <mailto:%s>}
@copyright: %s
@status: WIP
@license: %s
""" % ((__version__, ) + parseaddr(__author__) + (__copyright__, __license__))

class ISBN(object):
    """
    Class for representing ISBN objects

    @ivar _isbn: Possibly formatted ISBN string
    @ivar isbn: Code only ISBN string
    """

    __slots__ = ('_isbn', 'isbn')

    def __init__(self, isbn):
        """
        Initialise a new C{ISBN} object

        @type isbn: C{str}
        @param isbn: ISBN string
        """
        self._isbn = isbn
        if len(isbn) in (9, 12):
            self.isbn = _isbn_cleanse(isbn, False)
        else:
            self.isbn = _isbn_cleanse(isbn)

    def __repr__(self):
        """
        Self-documenting string representation

        >>> ISBN("9780521871723")
        ISBN('9780521871723')
        >>> ISBN("3540009787")
        ISBN('3540009787')

        @rtype: C{str}
        @return: String to recreate C{ISBN} object
        """
        return "%s(%r)" % (self.__class__.__name__, self.isbn)

    def __str__(self):
        """
        Pretty printed ISBN string

        >>> print ISBN("9780521871723")
        9780521871723
        >>> print ISBN("978-052-187-1723")
        978-052-187-1723
        >>> print ISBN("3540009787")
        3540009787

        @rtype: C{str}
        @return: Human readable string representation of C{ISBN} object
        """
        return self._isbn

    def calculate_checksum(self):
        """
        Calculate ISBN checksum

        >>> ISBN("978-052-187-1723").calculate_checksum()
        '3'
        >>> ISBN("3540009787").calculate_checksum()
        '7'

        @rtype: C{str}
        @return: ISBN checksum value
        """
        if len(self.isbn) in (9, 12):
            return calculate_checksum(self.isbn)
        else:
            return calculate_checksum(self.isbn[:-1])

    def convert(self, code="978"):
        """
        Convert ISBNs between ISBN-10 and ISBN-13

        >>> ISBN("0071148167").convert()
        '9780071148160'
        >>> ISBN("9780071148160").convert()
        '0071148167'

        @type code: C{str}
        @param code: ISBN-13 prefix code
        @rtype: C{str}
        @return: Converted ISBN
        """
        return convert(self.isbn, code)

    def validate(self):
        """
        Validate an ISBN value

        >>> ISBN("978-052-187-1723").validate()
        True
        >>> ISBN("978-052-187-1720").validate()
        False
        >>> ISBN("3540009787").validate()
        True
        >>> ISBN("354000978x").validate()
        False

        @rtype: C{bool}
        @return: True if ISBN is valid
        """
        return validate(self.isbn)

class ISBN10(ISBN):
    """
    Class for representing ISBN-10 objects

    @see: C{ISBN}
    """
    def __init__(self, isbn):
        """
        Initialise a new C{ISBN10} object

        @type isbn: C{str}
        @param isbn: ISBN-10 string
        """
        if len(isbn) == 9:
            self._isbn = isbn
            self.isbn = _isbn_cleanse(isbn, False)
        else:
            self.isbn = _isbn_cleanse(isbn)

    def calculate_checksum(self):
        """
        Calculate ISBN-10 checksum

        >>> ISBN10("3540009787").calculate_checksum()
        '7'

        @rtype: C{str}
        @return: ISBN-10 checksum value
        """
        if len(self.isbn) == 9:
            return calculate_checksum(self.isbn)
        else:
            return calculate_checksum(self.isbn[:-1])

    def convert(self, code="978"):
        """
        Convert ISBN-10 to ISBN-13

        >>> ISBN10("0071148167").convert()
        '9780071148160'

        @type code: C{str}
        @param code: ISBN-13 prefix code
        @rtype: C{str}
        @return: ISBN-13 string
        """
        return convert(self.isbn, code)

class ISBN13(ISBN):
    """
    Class for representing ISBN-13 objects

    @see: C{ISBN}
    """
    def __init__(self, isbn):
        """
        Initialise a new C{ISBN13} object

        @type isbn: C{str}
        @param isbn: ISBN-13 string
        """
        if len(isbn) == 12:
            self._isbn = isbn
            self.isbn = _isbn_cleanse(isbn, False)
        else:
            self.isbn = _isbn_cleanse(isbn)

    def calculate_checksum(self):
        """
        Calculate ISBN-13 checksum

        >>> ISBN13("978-052-187-1723").calculate_checksum()
        '3'

        @rtype: C{str}
        @return: ISBN-13 checksum value
        """
        if len(self.isbn) == 12:
            return calculate_checksum(self.isbn)
        else:
            return calculate_checksum(self.isbn[:-1])

    def convert(self):
        """
        Convert ISBN-13 to ISBN-10

        >>> ISBN13("9780071148160").convert()
        '0071148167'

        @rtype: C{str}
        @return: ISBN-10 string
        """
        return convert(self.isbn)

def _isbn_cleanse(isbn, checksum=True):
    """
    Check ISBN is a string, and passes basic sanity checks

    >>> for isbn in test_isbns.values():
    ...     if isbn.startswith("0"):
    ...         if not _isbn_cleanse(isbn[1:]) == isbn:
    ...             print("SBN with checksum failure `%s'" % isbn)
    ...         if not _isbn_cleanse(isbn[1:-1], False) == isbn[:-1]:
    ...             print("SBN without checksum failure `%s'" % isbn)

    >>> for isbn in test_isbns.values():
    ...     if not _isbn_cleanse(isbn) == isbn:
    ...         print("ISBN with checksum failure `%s'" % isbn)
    ...     if not _isbn_cleanse(isbn[:-1], False) == isbn[:-1]:
    ...         print("ISBN without checksum failure `%s'" % isbn)

    >>> _isbn_cleanse(2)
    Traceback (most recent call last):
      ...
    TypeError: ISBN must be a string `2'
    >>> _isbn_cleanse("0-123")
    Traceback (most recent call last):
    ...
    ValueError: ISBN must be either 10 or 13 characters long
    >>> _isbn_cleanse("0-123", checksum=False)
    Traceback (most recent call last):
    ...
    ValueError: ISBN must be either 9 or 12 characters long without checksum
    >>> _isbn_cleanse("0-x4343")
    Traceback (most recent call last):
    ...
    ValueError: Invalid ISBN string(non-digit parts)
    >>> _isbn_cleanse("012345678-b")
    Traceback (most recent call last):
    ...
    ValueError: Invalid ISBN string(non-digit or X checksum)

    @type isbn: C{str}
    @param isbn: SBN, ISBN-10 or ISBN-13
    @type checksum: C{bool}
    @param checksum: True if C{isbn} includes checksum character
    @rtype: C{str}
    @return: ISBN with hyphenation removed
    @raise TypeError: C{isbn} is not a C{str} type
    @raise ValueError: Incorrect length for C{isbn}
    @raise ValueError: Incorrect SBN or ISBN formatting
    """
    if isinstance(isbn, basestring):
        isbn = isbn.replace("-", "")
    else:
        raise TypeError("ISBN must be a string `%s'" % isbn)
    if not isbn[:-1].isdigit():
        raise ValueError("Invalid ISBN string(non-digit parts)")
    if checksum:
        if not (isbn[-1].isdigit() or isbn[-1] in "Xx"):
            raise ValueError("Invalid ISBN string(non-digit or X checksum)")
        if len(isbn) == 9:
            isbn = "0" + isbn
        if not len(isbn) in (10, 13):
            raise ValueError("ISBN must be either 10 or 13 characters long")
    else:
        if not isbn[-1].isdigit():
            raise ValueError("Invalid ISBN string(non-digit parts)")
        if len(isbn) == 8:
            isbn = "0" + isbn
        if not len(isbn) in (9, 12):
            raise ValueError("ISBN must be either 9 or 12 characters long "
                             "without checksum")
    return isbn

def calculate_checksum(isbn):
    """
    Calculate ISBN checksum

    >>> for isbn in test_isbns.values():
    ...     if not calculate_checksum(isbn[:-1]) == isbn[-1]:
    ...         print("ISBN checksum failure `%s'" % isbn)

    @type isbn: C{str}
    @param isbn: SBN, ISBN-10 or ISBN-13
    @rtype: C{str}
    @return: Checksum for given C{isbn}
    """
    isbn = [int(i) for i in _isbn_cleanse(isbn, checksum=False)]
    if len(isbn) == 9:
        products = [isbn[i] * (10 - i) for i in range(9)]
        remainder = sum(products) % 11
        check = 11 - remainder
        if check == 10:
            check = "X"
        elif check == 11:
            check = 0
    else:
        products = [(isbn[i] if i % 2 == 0 else isbn[i] * 3) for i in range(12)]
        remainder = sum(products) % 10
        check = 10 - remainder
        if check == 10:
            check = 0
    return str(check)

def convert(isbn, code="978"):
    """
    Convert ISBNs between ISBN-10 and ISBN-13

    No attempt to hyphenate converted ISBNs is made, because the specification
    requires that I{any} hyphenation must be correct but allows ISBNs without
    hyphenation.

    >>> for isbn in test_isbns.values():
    ...     if not convert(convert(isbn)) == isbn.replace("-", ""):
    ...         print("ISBN conversion failure `%s'" % isbn)
    >>> convert("0000000000000")
    Traceback (most recent call last):
    ...
    ValueError: `000' is not a Bookland code

    @type isbn: C{str}
    @param isbn: SBN, ISBN-10 or ISBN-13
    @type code: C{str}
    @param code: EAN Bookland code
    @rtype: C{str}
    @return: Converted ISBN-10 or ISBN-13
    @raise ValueError: When ISBN-13 isn't a Bookland ISBN
    """
    isbn = _isbn_cleanse(isbn)
    if len(isbn) == 10:
        isbn = code + isbn[:-1]
        return isbn + calculate_checksum(isbn)
    else:
        if isbn.startswith(("978", "979")):
            return isbn[3:-1] + calculate_checksum(isbn[3:-1])
        else:
            raise ValueError("`%s' is not a Bookland code" % isbn[:3])

def validate(isbn):
    """
    Validate ISBNs

    @warn: Publishers have been known to go to press with broken ISBNs, and
    therefore validation failures do not completely guarantee an ISBN is
    incorrectly entered.  It should however be noted that it is massively more
    likely I{you} have entered an invalid ISBN than the published ISBN is
    incorrectly produced.  An example of this probability in the real world is
    that U{Amazon <http://www.amazon.com/>} consider it so unlikely that they
    refuse to search for invalid published ISBNs.

    Valid ISBNs
    >>> for isbn in test_isbns.values():
    ...     if not validate(isbn):
    ...         print("ISBN validation failure `%s'" % isbn)

    Invalid ISBNs
    >>> for isbn in ("1-234-56789-0", "2-345-6789-1", "3-456-7890-X"):
    ...     if validate(isbn):
    ...         print("ISBN invalidation failure `%s'" % isbn)

    @type isbn: C{str}
    @param isbn: SBN, ISBN-10 or ISBN-13
    @rtype: C{bool}
    @return: C{True} if ISBN is valid
    """
    isbn = _isbn_cleanse(isbn)
    return isbn[-1] == calculate_checksum(isbn[:-1])
