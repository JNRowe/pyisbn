#
# vim: set sw=4 sts=4 et tw=80 fileencoding=utf-8:
#
"""Per-package configuration data"""
# Copyright (C) 2008-2010  James Rowe
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

import pyisbn
MODULE = pyisbn

SCRIPTS = []

DESCRIPTION = MODULE.__doc__.splitlines()[0][:-1]
LONG_DESCRIPTION = "\n\n".join(MODULE.__doc__.split("\n\n")[1:4])

KEYWORDS = ['ISBN', 'ISBN-10', 'ISBN-13', 'SBN']
CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Other Audience',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.4',
    'Programming Language :: Python :: 2.5',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 3',
    'Topic :: Other/Nonlisted Topic',
    'Topic :: Text Processing :: Indexing',
]

OBSOLETES = []

GRAPH_TYPE = None

from test import isbns
TEST_EXTRAGLOBS = {
    "TEST_ISBNS": isbns.TEST_ISBNS,
}

SCM = "git"

