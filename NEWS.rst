User-visible changes
====================

.. contents::

1.4.0 - 2026-01-30
------------------

* *Large scale refactoring*.  Speak up, and accept my apology in advance, if
  I’ve broken something
* Adopt Contributor Covenant Code of Conduct
* We now use uv_build_ as the packaging backend
* Python 3.11 to 3.14 are now officially supported
* Pypy is no longer supported, but if you require it open an issue_
* sphinx-autodoc-typehints_ is now required to build docs

.. _uv_build: https://docs.astral.sh/uv/concepts/build-backend/
.. _issue: https://github.com/JNRowe/pyisbn/issues
.. _sphinx-autodoc-typehints: https://pypi.org/project/sphinx-autodoc-typehints/

1.3.0 - 2020-02-10
------------------

* Python 2 support is dropped, pin dependencies to <1.2 if you require it
* Python 3.8 is now officially supported
* Type hints have been added
* hypothesis_ is now required to run tests

.. _hypothesis: https://github.com/HypothesisWorks/hypothesis

1.2.0 - 2018-07-28
------------------

.. note::

   This is really just a maintenance release, but changes a few deep things in
   the development process.  It also marks a *possible* fork point for dropping
   Python 2 support.

* ``pyisbn`` errors are now children of ``PyisbnError``
* pytest_ is now required to run the tests
* expecter_ is no longer required
* 3.7 is now officially supported

.. _pytest: http://pytest.org/
.. _expecter: https://pypi.org/project/expecter/

1.1.0 - 2017-04-04
------------------

* 3.{4..6} are now officially supported
* URL links now use HTTPs where possible
* Sphinx_ 1.3 is now required to build documentation
* nose2_ 0.5 with the coverage plugin is now required to run the tests

.. _nose2: https://pypi.org/project/nose2/

1.0.0 - 2014-01-31
------------------

* This package is, and should, only be receiving bug fixes at this point

0.6.0 - 2011-05-13
------------------

* Massive clean up, this is just a maintenance release
* Switched to Sphinx_ for documentation

.. _Sphinx: http://sphinx.pocoo.org/

0.5.1 - 2009-07-28
------------------

* Fixed to work with Python v2.4 and above

0.5.0 - 2008-12-12
------------------

* Python 3 module and install support, however until tools are ported
  documentation must still be built with Python 2

0.4.0 - 2008-05-21
------------------

* Fixed installs with easy_install
* SBNs can now be represented with the ``SBN`` object
* Python “egg” packages can now be built, if setuptools_ is installed

.. _setuptools: http://peak.telecommunity.com/DevCenter/setuptools

0.3.0 - 2007-12-11
------------------

* Data for tests is now external, which significantly reduces the import
  footprint
* ``make`` is no longer required to build and install the package

0.2.0 - 2007-11-16
------------------

* Relicensed under the `GPL v3`_
* Introduced classes ``ISBN``, ``ISBN10`` and ``ISBN13`` for easier use within
  OO code
* Larger, more thorough, test suite

.. _GPL v3: http://www.gnu.org/licenses/

0.1.0 - 2007-05-21
------------------

* Initial release
