#
# vim: set sw=4 sts=4 et tw=80 fileencoding=utf-8:
#
"""test - Support code and data for test suite"""
# Copyright (C) 2007-2008  James Rowe
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

__version__ = "0.1.0"
__date__ = "2007-11-29"
__author__ = "James Rowe <jnrowe@gmail.com>"
__copyright__ = "Copyright (C) 2007-2008 James Rowe"
__license__ = "GNU General Public License Version 3"
__credits__ = ""
__history__ = "See git repository"

try:
    from email.utils import parseaddr
except ImportError: # Python 2.4
    from email.Utils import parseaddr

__doc__ += """

:version: %s
:author: `%s <mailto:%s>`__
:copyright: %s
:status: WIP
:license: %s
""" % ((__version__, ) + parseaddr(__author__) + (__copyright__, __license__))

from test import mock

