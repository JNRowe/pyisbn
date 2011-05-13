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


import __pkg_data__

author, author_email = parseaddr(__pkg_data__.MODULE.__author__)

setup(
    name=__pkg_data__.MODULE.__name__,
    version=__pkg_data__.MODULE.__version__,
    description=__pkg_data__.DESCRIPTION,
    long_description=__pkg_data__.LONG_DESCRIPTION,
    author=author,
    author_email=author_email,
    maintainer=author,
    maintainer_email=author_email,
    url="https://github.com/JNRowe/%s/" % __pkg_data__.MODULE.__name__,
    download_url="http://pypi.python.org/packages/source/%s/%s/%s-%s.tar.gz" \
        % (__pkg_data__.MODULE.__name__[0], __pkg_data__.MODULE.__name__,
            __pkg_data__.MODULE.__name__, __pkg_data__.MODULE.__version__),
    packages=[__pkg_data__.MODULE.__name__],
    scripts=["%s.py" % i.__name__ for i in __pkg_data__.SCRIPTS],
    license=__pkg_data__.MODULE.__license__,
    keywords=" ".join(__pkg_data__.KEYWORDS),
    classifiers=__pkg_data__.CLASSIFIERS,
    obsoletes=__pkg_data__.OBSOLETES,
)
