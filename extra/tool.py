#! /usr/bin/env python3
"""tool - A simple pyisbn interface for the command line."""
# Copyright © 2013-2020  James Rowe <jnrowe@gmail.com>
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

import argparse
from typing import Callable

from pyisbn import Isbn, TIsbn, URL_MAP, _version


def isbn_typecheck(string: TIsbn) -> Isbn:
    try:
        isbn = Isbn(string)
        if not isbn.validate():
            raise ValueError('Invalid checksum')
    except ValueError as e:
        raise argparse.ArgumentTypeError(f'{e} {string!r}')
    return isbn


def partial_arg(f: Callable) -> Callable:
    def wrapper(*args: str, **kwargs: str):
        if 'const' not in kwargs:
            kwargs['const'] = args[1][2:].replace('-', '_')
        return f(*args, dest='command', action='store_const', **kwargs)

    return wrapper


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0].split(' - ', 1)[1],
        epilog='Please report bugs at https://github.com/JNRowe/pyisbn/issues')
    parser.add_argument('--version',
                        action='version',
                        version=f'pyisbn {_version.dotted}')
    commands = parser.add_mutually_exclusive_group()
    parg = partial_arg(commands.add_argument)
    parg('-c',
         '--checksum',
         const='calculate_checksum',
         help='generate checksum')
    parg('-x', '--convert', help='convert between 10- and 13-digit types')
    commands.add_argument('-u',
                          '--to-url',
                          choices=sorted(URL_MAP.keys()),
                          help='generate URL')
    parg('-n', '--to-urn', help='generate RFC 3187 URN')
    parser.add_argument('isbn',
                        type=isbn_typecheck,
                        nargs='+',
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
