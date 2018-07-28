#! /usr/bin/env python
# coding=utf-8
"""tool - A simple pyisbn interface for the command line."""
# Copyright © 2013-2018  James Rowe <jnrowe@gmail.com>
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

# You won't find this pretty… however it was quick to write and it's compatible
# with 2.4-3.3

import argparse
import sys

from pyisbn import (Isbn, URL_MAP, _version)


def isbn_typecheck(string):
    try:
        isbn = Isbn(string)
        if not isbn.validate():
            raise ValueError('Invalid checksum')
    except ValueError:
        ex = sys.exc_info()[1]
        raise argparse.ArgumentTypeError('%s %r' % (ex.args[0], string))
    return isbn


def partial_arg(f):
    def wrapper(*args, **kwargs):
        # Can't mix kwargs and supplied args in call for Python 2.5 compat
        kwargs.update({'dest': 'command', 'action': 'store_const'})
        if 'const' not in kwargs:
            kwargs['const'] = args[1][2:].replace('-', '_')
        return f(*args, **kwargs)
    return wrapper


def main():
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0].split('-', 1)[1],
        epilog='Please report bugs to jnrowe@gmail.com'
    )
    parser.add_argument('--version', action='version',
                        version='pyisbn %s' % _version.dotted)
    commands = parser.add_mutually_exclusive_group()
    parg = partial_arg(commands.add_argument)
    parg('-c', '--checksum', const='calculate_checksum',
         help='generate checksum')
    parg('-x', '--convert', help='convert between 10- and 13-digit types')
    commands.add_argument('-u', '--to-url',
                          choices=sorted(URL_MAP.keys()),
                          help='generate URL')
    parg('-n', '--to-urn', help='generate RFC 3187 URN')
    parser.add_argument('isbn', type=isbn_typecheck, nargs='+',
                        help='ISBNs to operate on')

    args = parser.parse_args()

    for isbn in args.isbn:
        if args.command:
            res = getattr(isbn, args.command)()
        elif args.to_url:
            res = isbn.to_url(args.to_url)
        else:
            res = str(isbn)
        print(res)


if __name__ == '__main__':
    main()
