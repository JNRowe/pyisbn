"""Internal constants."""
# Copyright © 2025  James Rowe <jnrowe@gmail.com>
#
# This file was authored by Gemini.  As per the Google Terms of Service, the
# user retains ownership of the generated content. For more information, see:
# https://policies.google.com/terms
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

#: SBN length.
SBN_LENGTH = 9
#: SBN length without checksum.
SBN_LENGTH_NO_CHECKSUM = 8

#: ISBN-10 length.
ISBN10_LENGTH = 10
#: ISBN-10 length without checksum.
ISBN10_LENGTH_NO_CHECKSUM = 9

#: ISBN-13 length.
ISBN13_LENGTH = 13
#: ISBN-13 length without checksum.
ISBN13_LENGTH_NO_CHECKSUM = 12


#: ISBN-13 'Bookland' prefixes.
BOOKLAND_PREFIXES = ("978", "979")
#: ISBN-13 'Bookland' prefix length.
BOOKLAND_PREFIX_LENGTH = 3


#: ISBN-10 checksum modulus.
ISBN10_CHECKSUM_MODULUS = 11
#: ISBN-10 checksum value for 'X'.
ISBN10_CHECKSUM_X = 10

#: ISBN-13 checksum modulus.
ISBN13_CHECKSUM_MODULUS = 10
#: ISBN-13 checksum multiplier for odd-positioned digits.
ISBN13_ODD_MULTIPLIER = 3
#: ISBN-13 checksum subtraction value.
ISBN13_CHECKSUM_SUBTRACT = 10
#: ISBN-13 checksum replacement for a value of ten.
ISBN13_CHECKSUM_TEN_REPLACEMENT = 0
