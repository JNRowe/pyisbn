.. highlight:: console

Installation
------------

You can install |modref| either via |PyPI| or from source.

Using |PyPI|
''''''''''''

To install using :pypi:`uv`::

    $ uv add pyisbn  # to add to the current project’s dependencies
    $ uv pip install pyisbn  # to install in the current workspace

Using :pypi:`pip`::

    $ pip3 install pyisbn  # to install in Python’s site-packages
    $ pip3 install --user pyisbn  # to install for a single user

From source
'''''''''''

If you have downloaded a source tarball you can install it with the following
steps::

    $ uv build  # to generate distributions
    # uv pip install --editable .  # to hack on pyisbn in the current workspace

|modref| has no dependencies outside the standard library.
