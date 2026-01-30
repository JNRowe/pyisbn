"""conf - Sphinx configuration information."""
# Copyright © 2011-2026  James Rowe <jnrowe@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This file is part of pyisbn.
#
# pyisbn is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# pyisbn is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# pyisbn.  If not, see <http://www.gnu.org/licenses/>.

import os
import pathlib
import sys
from contextlib import suppress
from importlib.metadata import version
from subprocess import CalledProcessError, PIPE, run  # NoQA: S404

root_dir = pathlib.Path(__file__).parent.parent
sys.path.insert(0, root_dir.as_posix())

on_rtd = "READTHEDOCS" in os.environ

extensions: list[str] = (
    [
        f"sphinx.ext.{ext}"
        for ext in [
            "autodoc",
            "coverage",
            "doctest",
            "extlinks",
            "ifconfig",
            "intersphinx",
            "napoleon",
            "todo",
            "viewcode",
        ]
    ]
    + [f"sphinxcontrib.{ext}" for ext in []]
    + [
        "sphinx_autodoc_typehints",
    ]
)

if not on_rtd:
    # Showing document build durations is only valuable when writing, so we'll
    # only enable it locally
    extensions.append("sphinx.ext.duration")

    # Only activate spelling if it is installed.  It is not required in the
    # general case and we don't have the granularity to describe this in a
    # clean way
    try:
        from sphinxcontrib import spelling  # NOQA: F401
    except ImportError:
        pass
    else:
        extensions.append("sphinxcontrib.spelling")

needs_sphinx = "4.3"

nitpicky = True

project = "pyisbn"
author = "James Rowe"
copyright = f"2007-2022  {author}"  # NoQA: A001

release = version("pyisbn")
version = release.rsplit(".", 1)[0]

trim_footnote_reference_space = True

rst_prolog = """
.. |ISBN| replace:: :abbr:`ISBN (International Standard Book Number)`
.. |PYPI| replace:: :abbr:`PyPI (Python Package Index)`
.. |modref| replace:: :mod:`pyisbn`
"""

modindex_common_prefix = [
    "pyisbn.",
]

# readthedocs.org handles this setup for their builds, but it is nice to see
# approximately correct builds on the local system too
if not on_rtd:
    html_theme = "sphinx_rtd_theme"

with suppress(CalledProcessError):
    proc = run(
        ["git", "log", "--pretty=format:%ad [%h]", "--date=short", "-n1"],  # NoQA: S607
        check=False,
        stdout=PIPE,
    )
    html_last_updated_fmt = proc.stdout.decode()

html_baseurl = "https://pyisbn.readthedocs.io/"

# Extension - autodoc
autoclass_content = "both"
autodoc_default_options: dict[str, str | None] = {
    "members": None,
}

# Extension - extlinks
extlinks: dict[str, tuple[str, str]] = {
    "pypi": ("http://pypi.python.org/pypi/%s", "%s"),
    "issue": ("https://github.com/JNRowe/jnrbase/issues/%s", "GitHub #"),
}

# Extension - intersphinx
intersphinx_mapping: dict[str, str] = {
    k: (v, os.getenv(f"SPHINX_{k.upper()}_OBJECTS"))
    for k, v in {
        "python": "https://docs.python.org/3/",
    }.items()
}

# Extension - spelling
spelling_ignore_acronyms = False
spelling_lang = "en_GB"
spelling_word_list_filename = "wordlist.txt"
spelling_ignore_python_builtins = False
spelling_ignore_importable_modules = False

# Extension - napoleon
napoleon_numpy_docstring = False

# Extension - todo
todo_include_todos = True
