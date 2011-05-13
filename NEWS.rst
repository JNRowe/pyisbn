``pyisbn``
==========

User-visible changes
--------------------

.. contents::

0.6.0 - 2011-05-13
------------------

* Massive clean up, this is just a mainenance release
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
* Python "egg" packages can now be built if setuptools_ is installed
* This package has been renamed ``pyisbn`` from ``ISBN`` to be more compliant
  with PEP-8_'s naming guidelines

.. _PEP-8: http://www.python.org/dev/peps/pep-0008/
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
