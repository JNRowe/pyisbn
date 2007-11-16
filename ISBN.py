#! /usr/bin/python -tt
# vim: set sw=4 sts=4 et tw=80 fileencoding=utf-8:
#
"""
ISBN - A module for working with 10- and 13-digit ISBNs
"""
# Copyright (C) 2007  James Rowe
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

__version__ = "0.2.0"
__date__ = "2007-05-18"
__author__ = "James Rowe <jnrowe@ukfsn.org>"
__copyright__ = "Copyright (C) 2007 James Rowe"
__license__ = "GNU General Public License Version 3"
__credits__ = ""
__history__ = "See Mercurial repository"

__doc__ += """
This module supports the calculation of ISBN checksums with
C{calculate_checksum()}, the conversion between ISBN-10 and ISBN-13 with
C{convert()} and the validation of ISBNs with C{validate()}.

All the functions require ISBNs to be passed in as C{str} types, even if it
would seem reasonable to accept some C{int} forms.  The reason behind this is
English speaking countries use ``0`` for their group identifier, and Python
would treat ISBNs beginning with ``0`` as octal representations producing
incorrect results.

The functions in this module also support 9-digit SBNs for people with older
books in their collection.

@version: %s
@author: U{%s%s}
@copyright: %s
@status: WIP
@license: %s
""" % (__version__, __author__[0:__author__.rfind(" ")],
       __author__[__author__.rfind(" "):], __copyright__, __license__)

__test_isbns = {
    "20, 000 Twenty Thousand Leagues Under the Sea": "0140621180",
    "3D Math Primer for Graphics and Game Development": "1556229119",
    "A Course in Combinatorics": "0521006015",
    "A Course in Modern Mathematical Physics: Groups, Hilbert Space and Differential Geometry": "0521829607",
    "A First Course in Coding Theory (Oxford Applied Mathematics & Computing Science S.)": "0198538030",
    "A First Course in General Relativity": "0521277035",
    "A First Course in String Theory": "0521831431",
    "A New Kind of Science": "1579550088",
    "ADA in Distributed Real Time Systems": "0070465444",
    "Ada 2005 Reference Manual": "3540693351",
    "Advanced Engineering Mathematics": "1403903123",
    "Advanced Signal Processing Algorithms, Architectures, and Implementation IX (SPIE)": "0819432938",
    "Aerodynamics for Engineering Students": "0750651113",
    "An Introduction to Fire Dynamics": "0471972916",
    "An Introduction to Modern Astrophysics (International Edition)": "0321210301",
    "An Introduction to Radio Astronomy": "0521005175",
    "Antenna Arraying Techniques in the Deep Space Network": "0471467995",
    "Applied Combinatorics": "047143809X",
    "Applied Cryptography: Protocols, Algorithms and Source Code in C": "0471117099",
    "Applied Satellite Navigation Using GPS, GALILEO, and Augmentation Systems": "1580538142",
    "Archimedes Effect": "0141011432",
    "Artificial Intelligence: A Modern Approach (International Edition)": "0130803022",
    "Artificial Intelligence: Structures and Strategies for Complex Problem Solving": "0321263189",
    "Astronomical Algorithms": "0943396611",
    "At the Bench: A Laboratory Navigator": "0879697083",
    "Automatic Target Recognition IX (SPIE)": "0819431923",
    "Autonomous Software-defined Radio Receivers for Deep Space Applications": "0470082127",
    "Beyond Fear: Thinking Sensibly About Security in an Uncertain World": "0387026207",
    "Brunel: The Man Who Built the World": "0297844083",
    "Causality: Models, Reasoning, and Inference": "0521773628",
    "Chaos and Complexity in Astrophysics": "0521855349",
    "Chaos and Complexity in Astrophysics": "0521855349",
    "Chaos: An Introduction to Dynamical Systems (Textbooks in Mathematical Sciences S.)": "0387946772",
    "Civil Engineering Formulas": "0071356126",
    "Classical Mechanics: An Undergraduate Text": "0521534097",
    "Clear and Present Danger": "0006177301",
    "Colossus: The Secrets of Bletchley Park's Code-breaking Computers": "019284055X",
    "Combinatorial Auctions": "0262033429",
    "Combinatorics: Topics, Techniques, Algorithms": "0521457610",
    "Count Zero": "0575036966",
    "Creating More Effective Graphs": "047127402X",
    "Crime Scene Investigation: Methods and Procedures": "0335214908",
    "Crime Scene to Court: The Essentials of Forensic Science": "0854046569",
    "Criminalistics: An Introduction to Forensic Science": "0131228897",
    "Cryptography Theory and Practice": "1584885084",
    "Cybernetics: Or Control and Communication in the Animal and the Machine": "026273009X",
    "Cyberpunk and Cyberculture: Science Fiction and the Work of William Gibson": "0485006073",
    "Data Analysis: A Bayesian Tutorial": "0198568320",
    "Dead Reckoning: Calculating Without Instruments": "0884150879",
    "Deep Down Things: The Breathtaking Beauty of Particle Physics": "080187971X",
    "Democratizing Innovation": "0262002744",
    "Dependence Logic: A New Approach to Independence Friendly Logic": "0521700159",
    "Design patterns : elements of reusable object-oriented software": "0201633612",
    "Dictionary of British Sign Language": "0571143466",
    "Discovering Genomics, Proteomics and Bioinformatics": "0805382194",
    "Discovering Statistics Using SPSS": "0761944524",
    "Einstein's Miraculous Year: Five Papers That Changed the Face of Physics": "0691122288",
    "Elements of Photogrammetry with Applications in GIS": "0072924543",
    "Engineering Mathematics 5th ed": "0333919394",
    "Estimation with Applications to Tracking and Navigation": "047141655X",
    "Evolution of Networks": "0198515901",
    "Evolution of Networks: From Biological Nets to the Internet and WWW": "0198515901",
    "Factory Physics": "0071163786",
    "Forensic Science": "0130432512",
    "Friendly Introduction to Graph Theory": "0130669490",
    "From the Earth to the Moon": "0553214209",
    "Fundamentals of Biomechanics": "0306474743",
    "Fundamentals of Heat and Mass Transfer": "0471386502",
    "Fundamentals of the Physical Environment": "0415232945",
    "Gauge Theories in Particle Physics: From Relativistic Quantum Mechanics to QED: v. 1": "0750308648",
    "Generalized Latent Variable Modeling: Multilevel, Longitudinal, & Structural Equation Models": "1584880007",
    "Generating Families in the Restricted Three-Body Problem (Lecture Notes in Physics S.)": "3540638024",
    "Generating Families in the Restricted Three-body Problem: Quantitative Study of Bifurcations: Pt. 2 (Lecture Notes in Physics)": "3540417338",
    "Genetic Algorithms in Search, Optimization and Machine Learning": "0201157675",
    "Getting Things Done: The Art of Stress-Free Productivity": "0670889067",
    "Global Navigation Satellite System (GNSS) Receivers for Weak Signals": "1596930527",
    "Gonzo Gizmos: Projects and Devices to Channel Your Inner Geek": "1556525206",
    "Gravity from the Ground Up: An Introductory Guide to Gravity and General Relativity": "0521455065",
    "Ground Penetrating Radar": "0863413609",
    "Guide to Biometrics (Springer Professional Computing S.)": "0387400893",
    "Guide to Elliptic Curve Cryptography (Springer Professional Computing)": "038795273X",
    "Hackers and Painters: Essays on the Art of Programming": "0596006624",
    "Handbook of Applied Cryptography": "0849385237",
    "Handbook of Fingerprint Recognition (Springer Professional Computing S.)": "0387954317",
    "Heat and Mass Transfer": "1904798470",
    "Heat and Thermodynamics": "0071148167",
    "High Integrity Software": "0321136160",
    "How to Research": "0335209033",
    "How to Use a Computerized Telescope: Practical Amateur Astronomy Volume 1: v. 1 (Practical Amateur Astronomy)": "0521007909",
    "IA-64 Linux Kernel": "0130610143",
    "IA-64 Linux Kernel: Design and Implementation": "0130610143",
    "Icon Steve Jobs: The Greatest Second Act in the History of Business": "0471720836",
    "In Search of Dark Matter: The Search for Dark Matter in the Universe (Springer-Praxis Books S.)": "0387276165",
    "Information and Coding Theory (Springer Undergraduate Mathematics S.)": "1852336226",
    "Introduction to Algorithms": "0262531968",
    "Introduction to Elementary Particles": "0471603864",
    "Introduction to Mechanics": "0070854238",
    "Introduction to Quantum Computation and Information": "981024410X",
    "Introduction to Space Physics (Cambridge Atmospheric & Space Science S.)": "0521457149",
    "Introduction to Statistical Physics": "0748409424",
    "Isambard Kingdom Brunel": "0140117520",
    "Joel on Software: And on Diverse and Occasionally Related Matters That Will Prove of Interest to Software Developers, Designers, and Managers, and to Those Who, Whether by Good Fortune or Ill-Luck, Work with Them in Some Capacity": "1590593898",
    "Journey to the Centre of the Earth": "0140621393",
    "Knots and Surfaces: A Guide to Discovering Mathematics": "0821804510",
    "Knowledge Representation: Logical, Philosophical and Computational Foundations": "0534949657",
    "LDAP in the Solaris Operating Environment: Deploying Secure Directory Services": "0131456938",
    "Let's Sign Dictionary: Everyday BSL for Learners": "0954238435",
    "Linux Kernel Development": "0672327201",
    "Linux Kernel Development": "0672327201",
    "Local Search in Combinatorial Optimization": "0691115222",
    "Lunar and Planetary Webcam User's Guide (Patrick Moore's Practical Astronomy S.)": "1846281970",
    "Malicious Cryptography: Exposing Cryptovirology": "0764549758",
    "Manual of Engineering Drawing": "0750651202",
    "Masters of Doom: How Two Guys Created an Empire and Transformed Pop Culture": "0749924896",
    "Mathematical Handbook for Scientists and Engineers: Definitions, Theorems, and Formulas for Reference and Review": "0486411478",
    "Mechanics (Course of Theoretical Physics)": "0750628960",
    "MicroC/OS II: The Real Time Kernel": "1578201039",
    "Microfluidics for Biotechnology": "1580539610",
    "Modern Supersymmetry: Dynamics and Duality (International Series of Monographs on Physics)": "0198567634",
    "Neuromancer": "0441569560",
    "Nonlinear Control Systems (Communications & Control Engineering S.)": "3540199160",
    "Nuclear and Particle Physics": "0582450888",
    "Numerical Heat Transfer and Fluid Flow": "0891165223",
    "Numerical Recipes in C++: The Art of Scientific Computing": "0521750334",
    "Paradigms of Artificial Intelligence Programming: Case Studies in Common LISP": "1558601910",
    "Particle Astrophysics (Oxford Master Series in Physics)": "0198509529",
    "Particle Astrophysics (Oxford Master Series in Physics)": "0198509529",
    "Particle Physics (Manchester Physics S.)": "0471972851",
    "Permutation City": "1857982185",
    "Physical Design Essentials": "0387366423",
    "Power and Invention: Situating Science (Theory Out of Bounds S.)": "0816625174",
    "Practical Statistics for Astronomers": "0521456169",
    "Predicting Motion: The Physical World (The Physical World)": "0750307161",
    "Probabilistic Robotics (Intelligent Robotics & Autonomous Agents S.)": "0262201623",
    "Probabilistic Robotics (Intelligent Robotics & Autonomous Agents S.)": "0262201623",
    "Probability Theory: The Logic of Science: Principles and Elementary Applications Vol 1": "0521592712",
    "Programming in Haskell": "9780521871723",
    "Quantum Groups: A Path to Current Algebra": "0521695244",
    "Radiometric Tracking Techniques for Deep-Space Navigation": "0471445347",
    "Rainbow Six": "0140274057",
    "Ramsey Theory on the Integers (Student Mathematical Library)": "0821831992",
    "Random Graph Dynamics": "0521866561",
    "Reliable Embedded Systems": "0321252918",
    "Reliable Software Technology": "3540262865",
    "Renormalization Methods: A Guide for Beginners ": "0198506945",
    "Resilience Engineering: Concepts and Precepts": "0754649040",
    "Revolutionaries of the Cosmos: The Astro-Physicists": "0198570996",
    "Schaum's Outline of Feedback and Control Systems (Schaum S.)": "0070170525",
    "Secrets and Lies: Digital Security in a Networked World": "0471453803",
    "Security Engineering: A Guide to Building Dependable Distributed Systems": "0471389226",
    "Sensor Modelling and Data Processing for Autonomous Navigation": "9810234961",
    "Show Me the Numbers: Designing Tables and Graphs to Enlighten": "0970601999",
    "Signal Integrity Effects in Custom IC and ASIC Designs": "0471150428",
    "Small Worlds: The Dynamics of Networks Between Order and Randomness (Princeton Studies in Complexity)": "0691117047",
    "Softwar: An Intimate Portrait of Larry Ellison and Oracle": "0743225058",
    "Software as Capital: Economic Perspective on Software Engineering": "0818677791",
    "Solaris: Systems Programming": "0201750392",
    "Statistical Analysis of Circular Data": "0521568900",
    "Statistical Mechanics of Lattice Systems: Exact, Series and Renormalization Group Methods: v. 2 (Texts & Monographs in Physics)": "3540644369",
    "Statistical Mechanics": "9971966077",
    "Statistical Mechanics: A Survival Guide ": "0198508166",
    "Statistical Mechanics: A Survival Guide": "0198508166",
    "Statistical Mechanics: Entropy, Order Parameters and Complexity": "0198566778",
    "Statistics: An Introduction Using R": "0470022981",
    "Storming the Reality Studio: Casebook of Cyberpunk and Postmodern Science Fiction": "0822311682",
    "Strange Attractors: Chaos, Complexity and the Art of Family Therapy (Wiley Series in Couples & Family Dynamics & Treatment)": "0471079510",
    "Strapdown Inertial Navigation Technology": "0863413587",
    "Synthesis of Arithmetic Circuits": "0471687839",
    "Techniques of Crime Scene Investigation": "084931691X",
    "The ASIC Handbook": "0130915580",
    "The Art of Intrusion: The Real Stories Behind the Exploits of Hackers, Intruders and Deceivers": "0764569597",
    "The Art of Project Management": "0596007868",
    "The Computational Beauty of Nature: Computer Explorations of Fractals, Chaos, Complex Systems and Adaptation (Bradford Book S.)": "0262561271",
    "The Computational Beauty of Nature: Computer Explorations of Fractals, Chaos, Complex Systems and Adaptation (Bradford Book S.)": "0262561271",
    "The Concepts and Practice of Mathematical Finance (Mathematic, Finance & Risk S.)": "0521823552",
    "The Difference Engine": "0575047623",
    "The Economics of the European Patent System": "0199216983",
    "The Egyptian Calendar: A Work for Eternity": "190269905X",
    "The First Men in the Moon -": "0460873040",
    "The HP Way: How Bill Hewlett and I Built Our Company": "0060845791",
    "The Hunt for Red October": "0006172768",
    "The Invisible Man": "0460876287",
    "The Meaning of It All (Allen Lane History S.)": "0140276351",
    "The Mythical Man Month and Other Essays on Software Engineering": "0201835959",
    "The Principia: Mathematical Principles of Natural Philosophy": "0520088174",
    "The Statistical Mechanics of Financial Markets (Texts & Monographs in Physics)": "3540009787",
    "The Thermodynamics Problem Solver": "0878915559",
    "The Time Machine": "0460877356",
    "The Tipping Point": "0316316962",
    "The Trouble with Physics": "0713997990",
    "The Universal Computer: The Road from Leibniz to Turing": "0393047857",
    "The Visual Display of Quantitative Information": "0961392142",
    "The War of the Worlds": "0460873032",
    "Theory of Financial Risk and Derivative Pricing: From Statistical Physics to Risk Management": "0521819164",
    "Thermal Physics": "0521658381",
    "Thermodynamics of Natural Systems": "0521847729",
    "Time's Alteration: Calendar Reform in Early Modern England": "1857286227",
    "Turbo Codes: Principles and Applications (Kluwer International Series in Engineering & Computer Science)": "0792378687",
    "Turbulence and Structures: Chaos, Fluctuations and Helical Self-organizaton in Nature and Laboratory (A Volume in the INTERNATIONAL GEOPHYSICS Series)": "0121257401",
    "Understanding Energy: Energy, Entropy and Thermodynamics for Everyman": "9810206798",
    "Understanding the Linux Kernel": "0596005652",
    "User Interface Design for Programmers": "1893115941",
    "VLSI: Memory, Microprocessor and ASIC": "0849317371",
    "Visual Complex Analysis": "0198534469",
    "What Are the Chances?: Voodoo Deaths, Office Gossip and Other Adventures in Probability": "0801869412",
    "Without Remorse": "0006476414",
    "Wizard: Life and Times of Nikola Tesla": "0806519606",
}

class ISBN(object):
    """
    Class for representing ISBN objects

    @ivar _isbn: Possibly formatted ISBN string
    @ivar isbn: Code only ISBN string
    """

    __slots__ = ('_isbn', 'isbn')

    def __init__(self, isbn):
        """
        Initialise a new C{ISBN} object

        @type isbn: C{str}
        @param isbn: ISBN string
        """
        self._isbn = isbn
        if len(isbn) in (9, 12):
            self.isbn = _isbn_cleanse(isbn, False)
        else:
            self.isbn = _isbn_cleanse(isbn)

    def __repr__(self):
        """
        Self-documenting string representation

        >>> ISBN("9780521871723")
        ISBN('9780521871723')
        >>> ISBN("3540009787")
        ISBN('3540009787')

        @rtype: C{str}
        @return: String to recreate C{ISBN} object
        """
        return "%s(%r)" % (self.__class__.__name__, self.isbn)

    def __str__(self):
        """
        Pretty printed ISBN string

        >>> print ISBN("9780521871723")
        9780521871723
        >>> print ISBN("978-052-187-1723")
        978-052-187-1723
        >>> print ISBN("3540009787")
        3540009787

        @rtype: C{str}
        @return: Human readable string representation of C{ISBN} object
        """
        return self._isbn

    def calculate_checksum(self):
        """
        Calculate ISBN checksum

        >>> ISBN("978-052-187-1723").calculate_checksum()
        '3'
        >>> ISBN("3540009787").calculate_checksum()
        '7'

        @rtype: C{str}
        @return: ISBN checksum value
        """
        if len(self.isbn) in (9, 12):
            return calculate_checksum(self.isbn)
        else:
            return calculate_checksum(self.isbn[:-1])

    def convert(self, code="978"):
        """
        Convert ISBNs between ISBN-10 and ISBN-13

        >>> ISBN("0071148167").convert()
        '9780071148160'
        >>> ISBN("9780071148160").convert()
        '0071148167'

        @type code: C{str}
        @param code: ISBN-13 prefix code
        @rtype: C{str}
        @return: Converted ISBN
        """
        return convert(self.isbn, code)

    def validate(self):
        """
        Validate an ISBN value

        >>> ISBN("978-052-187-1723").validate()
        True
        >>> ISBN("978-052-187-1720").validate()
        False
        >>> ISBN("3540009787").validate()
        True
        >>> ISBN("354000978x").validate()
        False

        @rtype: C{bool}
        @return: True if ISBN is valid
        """
        return validate(self.isbn)

class ISBN10(ISBN):
    """
    Class for representing ISBN-10 objects

    @see: C{ISBN}
    """
    def __init__(self, isbn):
        """
        Initialise a new C{ISBN10} object

        @type isbn: C{str}
        @param isbn: ISBN-10 string
        """
        if len(isbn) == 9:
            self._isbn = isbn
            self.isbn = _isbn_cleanse(isbn, False)
        else:
            self.isbn = _isbn_cleanse(isbn)

    def calculate_checksum(self):
        """
        Calculate ISBN-10 checksum

        >>> ISBN10("3540009787").calculate_checksum()
        '7'

        @rtype: C{str}
        @return: ISBN-10 checksum value
        """
        if len(self.isbn) == 9:
            return calculate_checksum(self.isbn)
        else:
            return calculate_checksum(self.isbn[:-1])

    def convert(self, code="978"):
        """
        Convert ISBN-10 to ISBN-13

        >>> ISBN10("0071148167").convert()
        '9780071148160'

        @type code: C{str}
        @param code: ISBN-13 prefix code
        @rtype: C{str}
        @return: ISBN-13 string
        """
        return convert(self.isbn, code)

class ISBN13(ISBN):
    """
    Class for representing ISBN-13 objects

    @see: C{ISBN}
    """
    def __init__(self, isbn):
        """
        Initialise a new C{ISBN13} object

        @type isbn: C{str}
        @param isbn: ISBN-13 string
        """
        if len(isbn) == 12:
            self._isbn = isbn
            self.isbn = _isbn_cleanse(isbn, False)
        else:
            self.isbn = _isbn_cleanse(isbn)

    def calculate_checksum(self):
        """
        Calculate ISBN-13 checksum

        >>> ISBN13("978-052-187-1723").calculate_checksum()
        '3'

        @rtype: C{str}
        @return: ISBN-13 checksum value
        """
        if len(self.isbn) == 12:
            return calculate_checksum(self.isbn)
        else:
            return calculate_checksum(self.isbn[:-1])

    def convert(self):
        """
        Convert ISBN-13 to ISBN-10

        >>> ISBN13("9780071148160").convert()
        '0071148167'

        @rtype: C{str}
        @return: ISBN-10 string
        """
        return convert(self.isbn)

def _isbn_cleanse(isbn, checksum=True):
    """
    Check ISBN is a string, and passes basic sanity checks

    >>> for isbn in __test_isbns.values():
    ...     if isbn.startswith("0"):
    ...         if not _isbn_cleanse(isbn[1:]) == isbn:
    ...             print("SBN with checksum failure `%s'" % isbn)
    ...         if not _isbn_cleanse(isbn[1:-1], False) == isbn[:-1]:
    ...             print("SBN without checksum failure `%s'" % isbn)

    >>> for isbn in __test_isbns.values():
    ...     if not _isbn_cleanse(isbn) == isbn:
    ...         print("ISBN with checksum failure `%s'" % isbn)
    ...     if not _isbn_cleanse(isbn[:-1], False) == isbn[:-1]:
    ...         print("ISBN without checksum failure `%s'" % isbn)

    >>> _isbn_cleanse(2)
    Traceback (most recent call last):
      ...
    TypeError: ISBN must be a string `2'
    >>> _isbn_cleanse("0-123")
    Traceback (most recent call last):
    ...
    ValueError: ISBN must be either 10 or 13 characters long
    >>> _isbn_cleanse("0-123", checksum=False)
    Traceback (most recent call last):
    ...
    ValueError: ISBN must be either 9 or 12 characters long without checksum
    >>> _isbn_cleanse("0-x4343")
    Traceback (most recent call last):
    ...
    ValueError: Invalid ISBN string(non-digit parts)
    >>> _isbn_cleanse("012345678-b")
    Traceback (most recent call last):
    ...
    ValueError: Invalid ISBN string(non-digit or X checksum)

    @type isbn: C{str}
    @param isbn: SBN, ISBN-10 or ISBN-13
    @type checksum: C{bool}
    @param checksum: True if C{isbn} includes checksum character
    @rtype: C{str}
    @return: ISBN with hyphenation removed
    @raise TypeError: C{isbn} is not a C{str} type
    @raise ValueError: Incorrect length for C{isbn}
    @raise ValueError: Incorrect SBN or ISBN formatting
    """
    if isinstance(isbn, str):
        isbn = isbn.replace("-", "")
    else:
        raise TypeError("ISBN must be a string `%s'" % isbn)
    if not isbn[:-1].isdigit():
        raise ValueError("Invalid ISBN string(non-digit parts)")
    if checksum:
        if not (isbn[-1].isdigit() or isbn[-1] in "Xx"):
            raise ValueError("Invalid ISBN string(non-digit or X checksum)")
        if len(isbn) == 9:
            isbn = "0" + isbn
        if not len(isbn) in (10, 13):
            raise ValueError("ISBN must be either 10 or 13 characters long")
    else:
        if not isbn[-1].isdigit():
            raise ValueError("Invalid ISBN string(non-digit parts)")
        if len(isbn) == 8:
            isbn = "0" + isbn
        if not len(isbn) in (9, 12):
            raise ValueError("ISBN must be either 9 or 12 characters long "
                             "without checksum")
    return isbn

def calculate_checksum(isbn):
    """
    Calculate ISBN checksum

    >>> for isbn in __test_isbns.values():
    ...     if not calculate_checksum(isbn[:-1]) == isbn[-1]:
    ...         print("ISBN checksum failure `%s'" % isbn)

    @type isbn: C{str}
    @param isbn: SBN, ISBN-10 or ISBN-13
    @rtype: C{str}
    @return: Checksum for given C{isbn}
    """
    isbn = [int(i) for i in _isbn_cleanse(isbn, checksum=False)]
    if len(isbn) == 9:
        products = [isbn[i] * (10 - i) for i in range(9)]
        remainder = sum(products) % 11
        check = 11 - remainder
        if check == 10:
            check = "X"
        elif check == 11:
            check = 0
    else:
        products = [(isbn[i] if i % 2 == 0 else isbn[i] * 3) for i in range(12)]
        remainder = sum(products) % 10
        check = 10 - remainder
        if check == 10:
            check = 0
    return str(check)

def convert(isbn, code="978"):
    """
    Convert ISBNs between ISBN-10 and ISBN-13

    No attempt to hyphenate converted ISBNs is made, because the specification
    requires that I{any} hyphenation must be correct but allows ISBNs without
    hyphenation.

    >>> for isbn in __test_isbns.values():
    ...     if not convert(convert(isbn)) == isbn.replace("-", ""):
    ...         print("ISBN conversion failure `%s'" % isbn)
    >>> convert("0000000000000")
    Traceback (most recent call last):
    ...
    ValueError: `000' is not a Bookland code

    @type isbn: C{str}
    @param isbn: SBN, ISBN-10 or ISBN-13
    @type code: C{str}
    @param code: EAN Bookland code
    @rtype: C{str}
    @return: Converted ISBN-10 or ISBN-13
    @raise ValueError: When ISBN-13 isn't a Bookland ISBN
    """
    isbn = _isbn_cleanse(isbn)
    if len(isbn) == 10:
        isbn = code + isbn[:-1]
        return isbn + calculate_checksum(isbn)
    else:
        if isbn.startswith(("978", "979")):
            return isbn[3:-1] + calculate_checksum(isbn[3:-1])
        else:
            raise ValueError("`%s' is not a Bookland code" % isbn[:3])

def validate(isbn):
    """
    Validate ISBNs

    @warn: Publishers have been known to go to press with broken ISBNs, and
    therefore validation failures do not completely guarantee an ISBN is
    incorrectly entered.  It should however be noted that it is massively more
    likely I{you} have entered an invalid ISBN than the published ISBN is
    incorrectly produced.  An example of this probability in the real world is
    that U{Amazon <http://www.amazon.com/>} consider it so unlikely that they
    refuse to search for invalid published ISBNs.

    Valid ISBNs
    >>> for isbn in __test_isbns.values():
    ...     if not validate(isbn):
    ...         print("ISBN validation failure `%s'" % isbn)

    Invalid ISBNs
    >>> for isbn in ("1-234-56789-0", "2-345-6789-1", "3-456-7890-X"):
    ...     if validate(isbn):
    ...         print("ISBN invalidation failure `%s'" % isbn)

    @type isbn: C{str}
    @param isbn: SBN, ISBN-10 or ISBN-13
    @rtype: C{bool}
    @return: C{True} if ISBN is valid
    """
    isbn = _isbn_cleanse(isbn)
    return isbn[-1] == calculate_checksum(isbn[:-1])

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])

