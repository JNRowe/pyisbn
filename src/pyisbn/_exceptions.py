"""Exception hierarchy for ``pyisbn``."""
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


class PyisbnError(ValueError):
    """Base ``pyisbn`` error."""


class CountryError(PyisbnError):
    """Unknown country value."""


class IsbnError(PyisbnError):
    """Invalid ISBN string."""


class SiteError(PyisbnError):
    """Unknown site value."""
