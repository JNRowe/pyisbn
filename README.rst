``pyisbn``
==========

A module for working with 10- and 13-digit ISBNs
------------------------------------------------

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

``pyisbn`` does not depend on any modules that aren't included in Python_'s
standard library, and as such should run with Python 2.4 or newer(including
Python 3) [#]_.  If ``pyisbn`` doesn't work with the version of Python you have
installed, open an issue_ and I'll endeavour to fix it.

The module have been tested on many UNIX-like systems, including Linux and OS X,
but it should work fine on other systems too.

.. [#] The module may work with older Python versions, but it has only
       been tested with v2.4 and above.

Example
-------

The simplest way to show how ``pyisbn`` works is by example, and here
goes::

    >>> import pyisbn
    >>> Permutation_City = "1-85798-218-5"
    >>> pyisbn.validate(Permutation_City)
    True
    >>> pyisbn.convert(Permutation_City)
    '9781857982183'
    >>> print("ISBN %s" % Permutation_City)
    ISBN 1-85798-218-5

or to process ISBNs using the object pattern use::

    >>> Permutation_City = pyisbn.Isbn10("1-85798-218-5")
    >>> Permutation_City.validate()
    True
    >>> Permutation_City.convert()
    '9781857982183'
    >>> print(Permutation_City)
    ISBN 1-85798-218-5

All independent functions contain hopefully useful docstrings with
``doctest``-based examples.

API Stability
-------------

API stability isn't guaranteed across versions, although frivolous changes won't
be made.

When ``pyisbn`` 1.0 is released the API will be frozen, and any changes which
aren't backwards compatible will force a major version bump.

Hacking
-------

Patches are most welcome, but I'd appreciate it if you could follow the
guidelines below to make it easier to integrate your changes.  These are
guidelines however, and as such can be broken if the need arises or you just
want to convince me that your style is better.

* `PEP 8`_, the style guide, should be followed where possible.
* While support for Python versions prior to v2.4 may be added in the future if
  such a need were to arise, you are encouraged to use v2.4 features now.
* All new classes and methods should be accompanied by new ``doctest`` examples,
  and Sphinx's `autodoc`_-compatible formatted descriptions if at all possible.
* Tests *must not* span network boundaries, see ``test.mock`` for workarounds.
* ``doctest`` tests in modules are only for unit testing in general, and should
  not rely on any modules that aren't in Python's standard library.
* Functional tests should be in the ``doc`` directory in reStructuredText_
  formatted files, with actual tests in ``doctest`` blocks.  Functional tests
  can depend on external modules, but they must be Open Source.

New examples for the ``doc`` directory are as appreciated as code changes.

Bugs
----

If you find a bug don't hesitate to open an issue, preferably including
a minimal testcase or even better a patch!

.. _GPL v3: http://www.gnu.org/licenses/
.. _view the content online: http://packages.python.org/pyisbn
.. _Python: http://www.python.org/
.. _issue: http://github.com/JNRowe/pyisbn/issues
.. _autodoc: http://sphinx.pocoo.org/ext/autodoc.html#module-sphinx.ext.autodoc
.. _PEP 8: http://www.python.org/dev/peps/pep-0008/
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
