#! /usr/bin/env python
# coding=utf-8
"""setup.py - Setuptools tasks and config for pyisbn."""
# Copyright © 2007-2017  James Rowe <jnrowe@gmail.com>
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
#
# SPDX-License-Identifier: GPL-3.0+

try:
    from email.utils import parseaddr
except ImportError:  # Python2.4
    from email.Utils import parseaddr  # NOQA

from setuptools import setup

import pyisbn


author, author_email = parseaddr(pyisbn.__author__)

paras = pyisbn.__doc__.split('\n\n')
long_description = '\n\n'.join([paras[1], paras[3]])

setup(
    name='pyisbn',
    version=pyisbn.__version__,
    description=pyisbn.__doc__.splitlines()[0][:-1],
    long_description=long_description,
    author=author,
    author_email=author_email,
    maintainer=author,
    maintainer_email=author_email,
    url='https://github.com/JNRowe/pyisbn/',
    packages=['pyisbn', ],
    license=pyisbn.__license__,
    keywords='ISBN ISBN-10 ISBN-13 SBN',
    classifiers=[
        'Development Status :: 6 - Mature',
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
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
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Other/Nonlisted Topic',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Indexing',
    ],
)
