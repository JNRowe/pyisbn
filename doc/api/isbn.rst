.. currentmodule:: pyisbn

Handling ISBNs
==============

The :py:class:`Isbn` supports SBNs, ISBN-10 and -13.  If you're handling
multiple inputs it is easiest to use this class.

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
    >>> invalid_book.validate()
    False

Format ISBN
'''''''''''

   >>> book.to_urn()
   'URN:ISBN:9783540009788'
   >>> book.to_url()
   'http://www.amazon.com/s?search-alias=stripbooks&field-isbn=9783540009788'
   >>> book.to_url('google')
   'http://books.google.com/books?vid=isbn:9783540009788'
