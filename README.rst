``pyisbn`` - A module for working with 10- and 13-digit ISBNs
=============================================================

|status| |actions| |pypi| |pyvers| |readthedocs| |develop|

Introduction
------------

``pyisbn`` is a `GPL v3`_ licensed module for working with various book
identification numbers.  It includes functions for conversion, verification and
generation of checksums.  It also includes basic classes for representing ISBNs
as objects.

See the ``doc`` directory for installation instructions and usage information,
you can also `view the content online`_.

Requirements
------------

``pyisbn`` does not depend on any modules that aren’t included in Python_’s
standard library, and as such should run with Python 3.11 or newer [#]_.  If
``pyisbn`` doesn’t work with the version of Python you have installed, open an
issue_ and I’ll endeavour to fix it.

The module have been tested on many UNIX-like systems, including Linux and OS X,
but it should work fine on other systems too.

.. [#] Versions v1.2 and earlier will run on older Python versions, right back
       to 2.4.

Example
-------

The simplest way to show how ``pyisbn`` works is by example, and here goes::

    >>> import pyisbn
    >>> Permutation_City = "1-85798-218-5"
    >>> pyisbn.validate(Permutation_City)
    True
    >>> pyisbn.convert(Permutation_City)
    '9781857982183'

or using the object pattern use::

    >>> Permutation_City = pyisbn.Isbn10("1-85798-218-5")
    >>> Permutation_City.validate()
    True
    >>> Permutation_City.convert()
    '9781857982183'
    >>> print(Permutation_City)
    ISBN 1-85798-218-5

All independent functions and classes contain (hopefully) useful docstrings.

API Stability
-------------

Now that ``pyisbn`` 1.0 has been released the API will is frozen, and any
changes which aren’t backwards compatible will force a major version bump.

Contributors
------------

I’d like to thank the following people who have contributed to ``pyisbn``.

Patches
'''''''

* Christopher Wells

Bug reports
'''''''''''

* James Gaffney
* hbc (bcho)
* Wen Heping
* Max Klein (notconfusing)
* Matt Leighy
* Nathaniel M. Beaver (nbeaver)
* Randy Syring (rsyring)
* Stephen Thorne

Ideas
'''''

* Kevin Simmons

If I’ve forgotten to include your name I wholeheartedly apologise.  Just drop
me a mail_ and I’ll update the list!

Bugs
----

If you find any problems, bugs or just have a question about this package
either file an issue_ or drop me a mail_.

If you’ve found a bug please attempt to include a minimal testcase so I can
reproduce the problem, or even better a patch!

.. _GPL v3: http://www.gnu.org/licenses/
.. _view the content online: http://pyisbn.rtfd.org/
.. _Python: http://www.python.org/
.. _issue: https://github.com/JNRowe/pyisbn/issues
.. _mail: jnrowe@gmail.com

.. |develop| image:: https://img.shields.io/github/commits-since/JNRowe/pyisbn/latest.png
   :target: https://github.com/JNRowe/pyisbn
   :alt: Recent developments

.. |pyvers| image:: https://img.shields.io/pypi/pyversions/pyisbn.png
   :alt: Supported Python versions

.. |status| image:: https://img.shields.io/pypi/status/pyisbn.png
   :alt: Development status

.. |pypi| image:: https://img.shields.io/pypi/v/pyisbn.png
   :target: https://pypi.org/project/pyisbn/
   :alt: Current PyPI release

.. |readthedocs| image:: https://img.shields.io/readthedocs/pyisbn/stable.png
   :target: https://pyisbn.readthedocs.io/
   :alt: Documentation

.. |actions| image:: https://img.shields.io/github/actions/workflow/status/JNRowe/pyisbn/pytest.yml?branch=main
   :alt: Test state on main
