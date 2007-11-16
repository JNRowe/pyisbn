#! /usr/bin/python -tt
# vim: set sw=4 sts=4 et tw=80 fileencoding=utf-8:
#
"""ISBN - A module for working with 10- and 13-digit ISBNs"""
# Copyright (C) 2007  James Rowe
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from distutils.core import setup

import re

import ISBN

from sys import version_info
if version_info < (2, 5, 0, 'final'):
    raise SystemExit("Requires Python v2.5+ for conditional expressions")

setup(
    name = "pyisbn",
    version = ISBN.__version__,
    description = ISBN.__doc__.splitlines()[1],
    long_description = re.sub("C{([^}]*)}", r"``\1``",
                              ISBN.__doc__[:ISBN.__doc__.rfind('\n\n')]),
    author = ISBN.__author__[0:ISBN.__author__.rfind(" ")],
    author_email = ISBN.__author__[ISBN.__author__.rfind(" ") + 2:-1],
    url = "http://www.jnrowe.ukfsn.org/projects/pyisbn.html",
    download_url = "http://www.jnrowe.ukfsn.org/data/pyisbn-%s.tar.bz2" \
                   % ISBN.__version__,
    py_modules = ['ISBN'],
    license = ISBN.__license__,
    keywords = ['ISBN', 'ISBN-10', 'ISBN-13', 'SBN'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Other/Nonlisted Topic',
        'Topic :: Text Processing :: Indexing',
    ],
    options = {'sdist': {'formats': 'bztar'}},
)

