#
# coding=utf-8
"""conf - Sphinx configuration information"""
# Copyright © 2007, 2008, 2009, 2010, 2011, 2012, 2013  James Rowe <jnrowe@gmail.com>
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

import os
import sys

from subprocess import (CalledProcessError, check_output)

root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, root_dir)

import pyisbn

extensions = \
    ['sphinx.ext.%s' % ext for ext in ['autodoc', 'coverage', 'doctest',
                                       'ifconfig', 'intersphinx', 'todo',
                                       'viewcode']] \
    + ["sphinxcontrib.%s" % ext for ext in ['cheeseshop']]


master_doc = 'index'
source_suffix = '.rst'

project = 'pyisbn'
try:
    unicode
    copyright = pyisbn.__copyright__.decode('utf-8')
except NameError:
    copyright = pyisbn.__copyright__

version = ".".join(map(str, pyisbn._version.tuple[:2]))
release = pyisbn._version.dotted

pygments_style = 'sphinx'
html_theme_options = {
    "externalrefs": True,
}
try:
    html_last_updated_fmt = check_output(['git', 'log',
                                          "--pretty=format:'%ad [%h]'",
                                          '--date=short', '-n1'])
except CalledProcessError:
    pass

# Autodoc extension settings
autoclass_content = "init"
autodoc_default_flags = ['members', 'inherited-members']

intersphinx_mapping = {
    'python': ('http://docs.python.org/', os.getenv('SPHINX_PYTHON_OBJECTS')),
}

