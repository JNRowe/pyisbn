.. highlight:: console

Installation
------------

You can install :mod:`pyisbn` either via :abbr:`PyPI (Python Package Index)` or
from source.

Using :abbr:`PyPI (Python Package Index)`
'''''''''''''''''''''''''''''''''''''''''

To install using :pypi:`pip`::

    $ pip install pyisbn  # to install in Python's site-packages
    $ pip install --install-option="--user" pyisbn  # to install for a single user

To install using :pypi:`easy_install <setuptools>`::

    $ easy_install pyisbn

From source
'''''''''''

If you have downloaded a source tarball you can install it with the following
steps::

    $ python setup.py build
    # python setup.py install  # to install in Python's site-packages
    $ python setup.py install --user  # to install for a single user

:mod:`pyisbn` has no dependencies outside the standard library.
