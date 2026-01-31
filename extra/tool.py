#! /usr/bin/env python3
"""tool - A simple pyisbn interface for the command line."""
# Copyright © 2013-2026  James Rowe <jnrowe@gmail.com>
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
from importlib.metadata import metadata
from typing import cast
from collections.abc import Callable

from pyisbn import Isbn
from pyisbn._constants import URL_MAP  # NoQA: PLC2701
from pyisbn._types import TIsbn

DISTRIBUTION = metadata("pyisbn")
PROJECT_URLS = dict(s.split(", ") for s in DISTRIBUTION.get_all("Project-URL"))


def isbn_typecheck(string: TIsbn) -> Isbn:
    """Check if string is a valid ISBN.

    Args:
        string: The string to check.

    Returns:
        The Isbn object.

    Raises:
        argparse.ArgumentTypeError: Invalid ISBN value
    """
    try:
        isbn = Isbn(string)
        if not isbn.validate():
            raise argparse.ArgumentTypeError("Invalid checksum")
    except ValueError as e:
        raise argparse.ArgumentTypeError(f"{e} {string!r}") from None
    return isbn


def build_command_argument(
    add_argument_func: Callable[..., argparse.Action],
) -> Callable[..., argparse.Action]:
    """Create a wrapper for argparse's add_argument to add command arguments.

    This wrapper automatically sets 'dest' to 'command', 'action' to
    'store_const', and computes 'const' from the long option if it's not
    provided (e.g., '--to-urn' becomes 'to_urn').

    Args:
        add_argument_func: The `add_argument` method of an argparse group.

    Returns:
        A function that adds a command argument to the parser.
    """

    def wrapper(*args: str, **kwargs: str) -> argparse.Action:
        """Add a command argument to the parser.

        Returns:
            argparse argument handler with our defaults applied.
        """
        if "const" not in kwargs:
            # e.g. '--to-urn' -> 'to_urn'
            kwargs["const"] = args[1][2:].replace("-", "_")
        return add_argument_func(
            *args, dest="command", action="store_const", **kwargs
        )

    return wrapper


def main() -> None:
    """Parse arguments and run the tool."""
    parser = argparse.ArgumentParser(
        description=cast(str, __doc__).splitlines()[0].split(" - ", 1)[1],
        epilog=f"Please report bugs at {PROJECT_URLS['Issue tracker']}",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"pyisbn {DISTRIBUTION['Version']}",
    )
    commands = parser.add_mutually_exclusive_group()
    add_command = build_command_argument(commands.add_argument)
    add_command(
        "-c",
        "--checksum",
        const="calculate_checksum",
        help="generate checksum",
    )
    add_command(
        "-x", "--convert", help="convert between 10- and 13-digit types"
    )
    commands.add_argument(
        "-u", "--to-url", choices=sorted(URL_MAP.keys()), help="generate URL"
    )
    add_command("-n", "--to-urn", help="generate RFC 3187 URN")
    parser.add_argument(
        "isbn", type=isbn_typecheck, nargs="+", help="ISBNs to operate on"
    )

    args = parser.parse_args()

    for isbn in args.isbn:
        if args.command:
            res = getattr(isbn, args.command)()
        elif args.to_url:
            res = isbn.to_url(args.to_url)
        else:
            res = str(isbn)
        print(res)


if __name__ == "__main__":
    main()
