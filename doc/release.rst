Release HOWTO
=============

..
  Much of this stuff is automated locally, but I’m describing the process for
  other people who will not have access to the same release tools I use.  The
  first thing I recommend that you do is find/write a tool that allows you to
  automate all of this, or you’re going to miss important steps at some point.

.. highlight:: console

Test
----

Tests can be run via pytest_::

    $ pip3 install -r extra/requirements-test.txt
    $ pytest -v tests

When preparing a release it is important to check that |modref| works with all
supported Python versions, and that the documentation for executing them is
correct.

Prepare release
---------------

With the tests passing, do the following steps:

* Update the version data in :file:`pyisbn/_version.py`
* Update :file:`NEWS.rst` with any user visible changes
* Commit the release notes and version changes
* Create a signed tag for the release
* Push the changes — including the new tag — to the GitHub repository
* Create a new release on GitHub

Update |PyPI|
-------------

..
  This is the section you’re especially likely to get wrong at some point if you
  try to handle all of this manually ;)

Create and upload the new release tarballs to |PyPI| using twine_::

    $ ./setup.py sdist bdist_wheel
    $ gpg --detach-sign --armour dist/pyisbn-${version}.tar.gz
    $ gpg --detach-sign --armour dist/pyisbn-${version}-*.whl
    $ twine upload dist/pyisbn-${version}*

Fetch the uploaded tarballs, and check for errors.

You should also test installation from |PyPI|, to check the experience
|modref|’s end users will have.

.. _pytest: http://pytest.org/
.. _twine: https://pypi.org/project/twine/
