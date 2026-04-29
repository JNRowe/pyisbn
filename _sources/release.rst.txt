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

    $ uv sync --group test
    $ pytest

Optionally, but *recommended*, is install the ``dev`` group and check for
problems reported by the linters.

When preparing a release it is important to check that |modref| works with all
supported Python versions, and that the documentation for executing them is
correct.

Prepare release
---------------

With the tests passing, do the following steps:

* Update the version data in :file:`pyproject.toml`
* Update :file:`NEWS.rst` with any user visible changes
* Commit the release notes and version changes
* Create a signed tag for the release
* Push the changes — including the new tag — to the GitHub repository
* Inspect the PyPI release created by pushing a new tag

.. _pytest: http://pytest.org/
