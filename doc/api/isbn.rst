.. currentmodule:: pyisbn

Handling ISBNs
==============

The :class:`Isbn` supports :abbr:`SBNs (Standard Book Numbering)`, |ISBN|-10
and -13.  If you’re handling multiple inputs it is easiest to use this class.

.. autoclass:: Isbn

Examples
--------

.. testsetup::

    from pyisbn import Isbn

Validate ISBN
'''''''''''''

    >>> book = Isbn('9783540009788')
    >>> book.validate()
    True
    >>> invalid_book = Isbn('0123456654321')
    Traceback (most recent call last):
      …
    pyisbn.IsbnError: invalid Bookland region

Format ISBN
'''''''''''

   >>> book.to_urn()
   'URN:ISBN:9783540009788'
   >>> book.to_url()
   'https://www.amazon.com/s?search-alias=stripbooks&field-isbn=9783540009788'
   >>> book.to_url('google')
   'https://books.google.com/books?vid=isbn:9783540009788'
