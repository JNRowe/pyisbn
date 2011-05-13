#! /usr/bin/python -tt
"""setup.py - Setuptools tasks and config for pyisbn"""
# Copyright (C) 2007-2011  James Rowe
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

try:
    from email.utils import parseaddr
except ImportError:  # Python2.4
    from email.Utils import parseaddr

from setuptools import setup

import pyisbn


author, author_email = parseaddr(pyisbn.__author__)

paras = pyisbn.__doc__.split("\n\n")
long_description = "\n\n".join([paras[1], paras[3]])

setup(
    name='pyisbn',
    version=pyisbn.__version__,
    description=pyisbn.__doc__.splitlines()[0][:-1],
    long_description=long_description,
    author=author,
    author_email=author_email,
    maintainer=author,
    maintainer_email=author_email,
    url="https://github.com/JNRowe/pyisbn/",
    download_url="http://pypi.python.org/packages/source/p/pyisbn/pyisbn-%s.tar.gz" \
        % pyisbn.__version__,
    packages=['pyisbn', ],
    license=pyisbn.__license__,
    keywords='ISBN ISBN-10 ISBN-13 SBN',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Topic :: Other/Nonlisted Topic',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Indexing',
    ],
)
