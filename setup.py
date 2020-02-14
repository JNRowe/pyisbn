#! /usr/bin/env python3
"""setup.py - Setuptools tasks and config for pyisbn."""
# Copyright © 2007-2020  James Rowe <jnrowe@gmail.com>
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

from typing import List

from setuptools import setup


def parse_requires(file: str) -> List[str]:
    deps = []
    with open(f'extra/{file}') as f:
        entries = [s.split('#')[0].strip() for s in f.readlines()]
    for dep in entries:
        if not dep or dep.startswith('#'):
            continue
        elif dep.startswith('-r '):
            deps.extend(parse_requires(dep.split()[1]))
            continue
        deps.append(dep)
    return deps


# Note: We can't use setuptool’s requirements support as it only a list value,
# and doesn’t support pip’s inclusion mechanism
tests_require = parse_requires('requirements-test.txt')

if __name__ == '__main__':
    setup(tests_require=tests_require)
