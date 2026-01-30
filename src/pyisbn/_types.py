"""Type definitions."""
# Copyright © 2026-2026  James Rowe <jnrowe@gmail.com>
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

from typing import NewType, TypeAlias

#: ISBN string type
TIsbn = NewType("TIsbn", str)
TIsbn10 = NewType("TIsbn10", TIsbn)
TIsbn13 = NewType("TIsbn13", TIsbn)

#: SBN string type
TSbn = NewType("TSbn", str)


_UrlMapTlds: TypeAlias = dict[str, str | None]
_UrlMapValue: TypeAlias = str | tuple[str, _UrlMapTlds]
