#
# coding=utf-8
"""conf - Sphinx configuration information."""
# Copyright © 2011-2018  James Rowe <jnrowe@gmail.com>
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

import os
import sys

from subprocess import CalledProcessError
try:
    from subprocess import check_output
except ImportError:
    from subprocess import (PIPE, Popen)

    def check_output(cmd):
        process = Popen(cmd, stdout=PIPE)
        out, _ = process.communicate()
        ret = process.wait()
        if ret:
            raise CalledProcessError(ret, cmd[0])
        return out


root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, root_dir)

import pyisbn  # NOQA

extensions = \
    ['sphinx.ext.%s' % ext for ext in ['autodoc', 'coverage', 'doctest',
                                       'extlinks', 'ifconfig', 'intersphinx',
                                       'napoleon', 'todo', 'viewcode']] \
    + ['sphinxcontrib.%s' % ext for ext in []]

# Only activate spelling if it is installed.  It is not required in the
# general case and we don't have the granularity to describe this in a clean
# way
try:
    from sphinxcontrib import spelling  # NOQA
except ImportError:
    pass
else:
    extensions.append('sphinxcontrib.spelling')

master_doc = 'index'
source_suffix = '.rst'

project = 'pyisbn'
try:
    unicode
    copyright = pyisbn.__copyright__.decode('utf-8')
except NameError:
    copyright = pyisbn.__copyright__

version = '.'.join(map(str, pyisbn._version.tuple[:2]))
release = pyisbn._version.dotted

rst_prolog = """
.. |ISBN| replace:: :abbr:`ISBN (International Standard Book Number)`
.. |PYPI| replace:: :abbr:`PyPI (Python Package Index)`
.. |modref| replace:: :mod:`pyisbn`
"""

pygments_style = 'sphinx'
try:
    html_last_updated_fmt = check_output(['git', 'log',
                                          "--pretty=format:'%ad [%h]'",
                                          '--date=short', '-n1'])
except CalledProcessError:
    pass

# Autodoc extension settings
autoclass_content = 'init'
autodoc_default_flags = ['members', ]

# intersphinx extension settings
intersphinx_mapping = {
    k: (v, os.getenv('SPHINX_%s_OBJECTS' % k.upper()))
    for k, v in {
        'python': 'http://docs.python.org/',
    }.items()
}

# extlinks extension settings
extlinks = {
    'pypi': ('http://pypi.python.org/pypi/%s', ''),
    'issue': ('https://github.com/JNRowe/jnrbase/issues/%s', 'GitHub #'),
}

# spelling extension settings
spelling_lang = 'en_GB'
spelling_word_list_filename = 'wordlist.txt'

# napoleon extension settings
napoleon_numpy_docstring = False
