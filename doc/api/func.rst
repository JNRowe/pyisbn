.. currentmodule:: pyisbn

Functions for handling ISBNs
============================

.. testsetup::

    from pyisbn import calculate_checksum, convert, validate

.. autofunction:: calculate_checksum

    >>> calculate_checksum('978354000978')
    '8'

.. autofunction:: convert

    >>> convert('9783540009788')
    '3540009787'

.. autofunction:: validate

    >>> validate('9783540009788')
    True

.. spelling:word-list::

   EAN
