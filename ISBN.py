#! /usr/bin/python -tt
# vim: set sw=4 sts=4 et tw=80 fileencoding=utf-8:
#
"""
ISBN - A module for working with 10- and 13-digit ISBNs
"""
# Copyright (C) 2007 James Rowe;
# All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111, USA.
#

__version__ = "0.1.1"
__date__ = "2007-05-18"
__author__ = "James Rowe <jnrowe@ukfsn.org>"
__copyright__ = "Copyright (C) 2007 James Rowe"
__license__ = "GNU General Public License Version 2"
__credits__ = ""
__history__ = "See Mercurial repository"

__doc__ += """
This module supports the calculation of ISBN checksums with
C{calculate_checksum()}, the conversion between ISBN-10 and ISBN-13 with
C{convert()} and the validation of ISBNs with C{validate()}.

All the functions require ISBNs to be passed in as C{str} types, even if it
would seem reasonable to accept some C{int} forms.  The reason behind this is
English speaking countries use ``0`` for their group identifier, and Python
would treat ISBNs beginning with ``0`` as octal representations producing
incorrect results.

The functions in this module also support 9-digit SBNs for people with older
books in their collection.

@version: %s
@author: U{%s%s}
@copyright: %s
@status: WIP
@license: %s
""" % (__version__, __author__[0:__author__.rfind(" ")],
       __author__[__author__.rfind(" "):], __copyright__, __license__)

import types

__test_isbns = {
    "20, 000 Twenty Thousand Leagues Under the Sea": "0140621180",
    "ADA in Distributed Real Time Systems": "0070465444",
    "Ada 2005 Reference Manual": "3540693351",
    "Antenna Arraying Techniques in the Deep Space Network": "0471467995",
    "Applied Satellite Navigation Using GPS, GALILEO, and Augmentation Systems": "1580538142",
    "Astronomical Algorithms": "0943396611",
    "Autonomous Software-defined Radio Receivers for Deep Space Applications": "0470082127",
    "Civil Engineering Formulas": "0071356126",
    "Classical Mechanics: An Undergraduate Text": "0521534097",
    "Data Analysis: A Bayesian Tutorial": "0198568320",
    "Democratizing Innovation": "0262002744",
    "Dependence Logic: A New Approach to Independence Friendly Logic": "0521700159",
    "Discovering Statistics Using SPSS": "0761944524",
    "Estimation with Applications to Tracking and Navigation": "047141655X",
    "Evolution of Networks": "0198515901",
    "From the Earth to the Moon": "0553214209",
    "Genetic Algorithms in Search, Optimization and Machine Learning": "0201157675",
    "Global Navigation Satellite System (GNSS) Receivers for Weak Signals": "1596930527",
    "Ground Penetrating Radar": "0863413609",
    "High Integrity Software": "0321136160",
    "IA-64 Linux Kernel": "0130610143",
    "Introduction to Quantum Computation and Information": "981024410X",
    "Journey to the Centre of the Earth": "0140621393",
    "Knots and Surfaces: A Guide to Discovering Mathematics": "0821804510",
    "Linux Kernel Development": "0672327201",
    "Local Search in Combinatorial Optimization": "0691115222",
    "Manual of Engineering Drawing": "0750651202",
    "Permutation City": "1857982185",
    "Physical Design Essentials": "0387366423",
    "Practical Statistics for Astronomers": "0521456169",
    "Quantum Groups: A Path to Current Algebra": "0521695244",
    "Radiometric Tracking Techniques for Deep-Space Navigation": "0471445347",
    "Random Graph Dynamics": "0521866561",
    "Reliable Embedded Systems": "0321252918",
    "Reliable Software Technology": "3540262865",
    "Resilience Engineering: Concepts and Precepts": "0754649040",
    "Sensor Modelling and Data Processing for Autonomous Navigation": "9810234961",
    "Signal Integrity Effects in Custom IC and ASIC Designs": "0471150428",
    "Statistical Mechanics: A Survival Guide": "0198508166",
    "Strapdown Inertial Navigation Technology": "0863413587",
    "Synthesis of Arithmetic Circuits": "0471687839",
    "The ASIC Handbook": "0130915580",
    "The Economics of the European Patent System": "0199216983",
    "The First Men in the Moon -": "0460873040",
    "The Invisible Man": "0460876287",
    "The Time Machine": "0460877356",
    "The Trouble with Physics": "0713997990",
    "The War of the Worlds": "0460873032",
    "VLSI: Memory, Microprocessor and ASIC": "0849317371",
    "Visual Complex Analysis": "0198534469",
}

def __isbn_cleanse(isbn, checksum=True):
    """
    Check ISBN is a string, and passes basic sanity checks

    >>> for isbn in __test_isbns.values():
    ...     if isbn.startswith("0"):
    ...         if not __isbn_cleanse(isbn[1:]) == isbn:
    ...             print "SBN with checksum failure `%s'" % isbn
    ...         if not __isbn_cleanse(isbn[1:-1], False) == isbn[:-1]:
    ...             print "SBN without checksum failure `%s'" % isbn

    >>> for isbn in __test_isbns.values():
    ...     if not __isbn_cleanse(isbn) == isbn:
    ...         print "ISBN with checksum failure `%s'" % isbn
    ...     if not __isbn_cleanse(isbn[:-1], False) == isbn[:-1]:
    ...         print "ISBN without checksum failure `%s'" % isbn

    >>> __isbn_cleanse(2)
    Traceback (most recent call last):
      ...
    TypeError: ISBN must be a string `2'
    >>> __isbn_cleanse("0-123")
    Traceback (most recent call last):
    ...
    ValueError: ISBN must be either 10 or 13 characters long
    >>> __isbn_cleanse("0-123", checksum=False)
    Traceback (most recent call last):
    ...
    ValueError: ISBN must be either 9 or 12 characters long without checksum

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
    if type(isbn) is types.StringType:
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

    >>> for isbn in __test_isbns.values():
    ...     if not calculate_checksum(isbn[:-1]) == isbn[-1]:
    ...         print "ISBN checksum failure `%s'" % isbn

    @type isbn: C{str}
    @param isbn: SBN, ISBN-10 or ISBN-13
    @rtype: C{str}
    @return: Checksum for given C{isbn}
    """
    isbn = [int(i) for i in __isbn_cleanse(isbn, checksum=False)]
    if len(isbn) == 9:
        products = [isbn[i] * (10 - i) for i in xrange(9)]
        remainder = sum(products) % 11
        check = 11 - remainder
        if check == 10:
            check = "X"
        elif check == 11:
            check = 0
    else:
        products = [(isbn[i] if i % 2 == 0 else isbn[i] * 3) for i in xrange(12)]
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

    >>> for isbn in __test_isbns.values():
    ...     if not convert(convert(isbn)) == isbn.replace("-", ""):
    ...         print "ISBN conversion failure `%s'" % isbn

    @type isbn: C{str}
    @param isbn: SBN, ISBN-10 or ISBN-13
    @type code: C{str}
    @param code: EAN Bookland code
    @rtype: C{bool}
    @return: C{True} if ISBN is valid
    @raise ValueError: When ISBN-13 isn't a Bookland ISBN
    """
    isbn = __isbn_cleanse(isbn)
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
    >>> for isbn in __test_isbns.values():
    ...     if not validate(isbn):
    ...         print "ISBN validation failure `%s'" % isbn

    Invalid ISBNs
    >>> for isbn in ("1-234-56789-0", "2-345-6789-1", "3-456-7890-X"):
    ...     if validate(isbn):
    ...         print "ISBN invalidation failure `%s'" % isbn

    @type isbn: C{str}
    @param isbn: SBN, ISBN-10 or ISBN-13
    @rtype: C{bool}
    @return: C{True} if ISBN is valid
    """
    isbn = __isbn_cleanse(isbn)
    return isbn[-1] == calculate_checksum(isbn[:-1])

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

