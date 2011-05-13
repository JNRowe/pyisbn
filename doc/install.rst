Installation
============

You can download releases from the `downloads page`_ on GitHub or the `PyPI
page`_.

:mod:`pyisbn` works with Python_ v2.4 or newer, including Python 3.
:mod:`pyisbn` has no dependencies outside of Python's standard library.
If for some reason :mod:`pyisbn` doesn't work with the version of Python you
have installed, please open an issue_.

To install using ``pip``::

    $ pip install pyisbn  # to install in Python's site-packages
    $ pip install --install-option="--user" pyisbn  # to install for a single user

Although it is not recommended you can install using ``easy_install``::

    $ easy_install github2

If you downloaded a source tarball, or cloned from ``git`` you can install with
the following steps::

    $ python setup.py build
    # python setup.py install  # to install in Python's site-packages
    $ python setup.py install --user  # to install for a single user

.. _downloads page: https://github.com/JNRowe/pyisbn/downloads
.. _PyPI page: http://pypi.python.org/pypi/pyisbn/
.. _Python: http://www.python.org/
.. _issue: http://github.com/JNRowe/pyisbn/issues
