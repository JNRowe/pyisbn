Release HOWTO
=============

.. highlight:: sh

..
  Much of this stuff is automated locally, but I'm describing the process for
  other people who will not have access to the same release tools I use.  The
  first thing I recommend that you do is find/write a tool that allows you to
  automate all of this, or you're going to miss important steps at some point.

Test
----

In the general case tests can be run via ``nose2``::

    $ nose2 -vv tests

When preparing a release it is important to check that :mod:`pyisbn` works with
all currently supported Python versions, and that the documentation is correct.

Prepare release
---------------

With the tests passing, perform the following steps

* Update the version data in :file:`pyisbn/_version.py`
* Update :file:`NEWS.rst`, if there are any user visible changes
* Commit the release notes and version changes
* Create a signed tag for the release
* Push the changes, including the new tag, to the GitHub repository

Update PyPI
-----------

..
  This is the section you're especially likely to get wrong at some point if
  you try to handle all of this manually ;)

Create and upload the new release tarballs to PyPI::

    $ ./setup.py sdist bdist_wheel register upload --sign

Fetch the uploaded tarballs, and check for errors.

You should also perform test installations from PyPI, to check the experience
:mod:`pyisbn` users will have.
