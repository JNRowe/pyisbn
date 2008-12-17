#! /usr/bin/python -tt
# vim: set sw=4 sts=4 et tw=80 fileencoding=utf-8:
#
"""grab_net_sources - Fetch sources for tests"""
# Copyright (C) 2007-2008  James Rowe;
# All rights reserved.
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

import bz2
import gzip
import os
import sys
import tempfile
try:
    from urllib.parse import urlparse
    from urllib.request import (urlopen, urlretrieve)
except ImportError:
    from urlparse import urlparse
    from urllib import (urlopen, urlretrieve)


SOURCES = [
    "http://www.amazon.com/dp/0071148167",
    "http://www.amazon.com/dp/0460877356",
    "http://www.amazon.com/dp/0140621180",
    "http://www.amazon.com/dp/1556229119",
    "http://www.amazon.com/dp/1579550088",
    "http://www.amazon.com/dp/0521773628",
    "http://www.amazon.com/dp/0306474743",
    "http://www.amazon.com/dp/0961392142",
    "http://www.amazon.com/dp/0460873032",
    "http://www.amazon.com/dp/0121257401",
    "http://www.amazon.com/dp/0801869412",
    "http://www.amazon.com/dp/0806519606",
    "http://www.amazon.com/dp/0060845791",
    "http://www.amazon.com/dp/0006172768",
]

def data_file(name):
    """Generate a local filename for the source

    >>> print data_file(SOURCES[0])
    0071148167

    :Parameters:
        name : `str`
            Source filename
    :rtype: `str`
    :return: Local filename

    """
    filename = os.path.join(os.path.dirname(__file__), "data",
                            os.path.basename(urlparse(name).path))
    if filename.endswith(".gz"):
        return filename[:-3]
    elif filename.endswith(".bz2"):
        return filename[:-4]
    else:
        return filename

def main(argv=None):
    """Main script handler

    :Parameters:
        argv : `list`
            Command line arguments

    """
    print("*WARNING* This script will fetch some data files that can not be "
          "distributed legally!  In some jurisdictions you may not even be "
          "entitled to personal use of the data it fetches without express "
          "consent of the copyright holders.")
    if not argv:
        argv = sys.argv
    if len(argv) == 2 and argv[1] in ("-f" or "--force"):
        force = True
    else:
        force = False
    cached = 0
    for resource in SOURCES:
        filename = data_file(resource)
        if not force and os.path.exists(filename):
            print("`%s' already downloaded." % resource)
            cached += 1
        else:
            print("Fetching `%s'..." % resource)
            if resource.endswith(".gz"):
                temp = tempfile.mkstemp()[1]
                try:
                    urlretrieve(resource, temp)
                    data = gzip.GzipFile(temp).read()
                finally:
                    os.unlink(temp)
                open(filename, "w").write(data)
            elif resource.endswith(".bz2"):
                data = bz2.decompress(urlopen(resource).read())
                open(filename, "w").write(data)
            else:
                urlretrieve(resource, filename)
    if cached > 1:
        print("You can force download with the `-f' option to this script.")

if __name__ == '__main__':
    main(sys.argv)

