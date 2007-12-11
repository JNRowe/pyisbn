#! /usr/bin/python -tt
# vim: set sw=4 sts=4 et tw=80 fileencoding=utf-8:
#
"""ISBN - A module for working with 10- and 13-digit ISBNs"""
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

import doctest
import os
import shutil
import sys

from distutils.archive_util import make_archive
from distutils.command.clean import clean
from distutils.command.sdist import sdist
from distutils.cmd import Command
from distutils.core import setup
from distutils.dep_util import newer
from distutils.errors import DistutilsModuleError
from distutils.file_util import write_file
from distutils.util import execute
from email.utils import parseaddr
from glob import glob
from re import sub
from subprocess import check_call
from time import strftime

try:
    from docutils.core import publish_cmdline, default_description
    from docutils import nodes
    from docutils.parsers.rst import directives
    DOCUTILS = True
except ImportError:
    DOCUTILS = False
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import HtmlFormatter
    PYGMENTS = True
except ImportError:
    PYGMENTS = False
try:
    from epydoc import cli
    EPYDOC = True
except ImportError:
    EPYDOC = False
try:
    from mercurial import hg
    MERCURIAL = True
except ImportError:
    MERCURIAL = False

import ISBN
from test_isbns import test_isbns

BASE_URL = "http://www.jnrowe.ukfsn.org/"

from sys import version_info
if version_info < (2, 5, 0, 'final'):
    raise SystemError("Requires Python v2.5+")

def write_changelog(filename):
    """
    Generate a ChangeLog from Mercurial repo

    @type filename: C{str}
    @param filename: Filename to write ChangeLog to
    """
    if os.path.isdir(".hg"):
        check_call(["hg", "log", "--exclude", ".be/", "--no-merges",
                    "--style", "changelog"],
                   stdout=open(filename, "w"))
    else:
        print("Unable to build ChangeLog, dir is not a Mercurial clone")
        return False

def gen_desc(doc):
    """
    Pull simple description from docstring

    @type doc: C{str}
    @param doc: Docstring to manipulate
    @rtype: C{str}
    @return: description string suitable for C{Command} class's description
    """
    desc = doc.splitlines()[1].lstrip()
    return desc[0].lower() + desc[1:]

class NoOptsCommand(Command):
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

class BuildDoc(NoOptsCommand):
    """
    Build project documentation

    @ivar force: Force documentation generation
    """
    description = gen_desc(__doc__)
    user_options = [
        ('force', 'f',
         "Force documentation generation"),
    ]
    boolean_options = ['force']

    def initialize_options(self):
        self.force = False

    def run(self):
        if not DOCUTILS:
            raise DistutilsModuleError("docutils import failed, "
                                       "skipping documentation generation")
        if not PYGMENTS:
            raise DistutilsModuleError("docutils import failed, "
                                       "skipping documentation generation")

        pygments_formatter = HtmlFormatter()

        def pygments_directive(name, arguments, options, content, lineno,
                               content_offset, block_text, state,
                               state_machine):
            try:
                lexer = get_lexer_by_name(arguments[0])
            except ValueError:
                # no lexer found - use the text one instead of an exception
                lexer = get_lexer_by_name('text')
            parsed = highlight(u'\n'.join(content), lexer, pygments_formatter)
            return [nodes.raw('', parsed, format='html')]
        pygments_directive.arguments = (1, 0, 1)
        pygments_directive.content = 1
        directives.register_directive('code-block', pygments_directive)

        for source in sorted(["NEWS", "README"]):
            dest = os.path.splitext(source)[0] + '.html'
            if self.force or newer(source, dest):
                print('Building file %s' % dest)
                if self.dry_run:
                    continue
                publish_cmdline(writer_name='html',
                                argv=['--source-link', '--strict',
                                      '--generator',
                                      '--stylesheet-path=docutils.css',
                                      '--link-stylesheet', source, dest])

        if not EPYDOC:
            raise DistutilsModuleError("epydoc import failed, "
                                       "skipping API documentation generation")
        files = ["ISBN.py", ]
        if self.force or any(newer(file, "html/index.html") for file in files):
            print('Building API documentation %s' % dest)
            if not self.dry_run:
                saved_args = sys.argv[1:]
                sys.argv[1:] = files
                cli.cli()
                sys.argv[1:] = saved_args
        if os.path.isdir(".hg"):
            if not MERCURIAL:
                raise DistutilsModuleError("Mercurial import failed")
            if self.force or not os.path.isfile("ChangeLog"):
                print('Building ChangeLog from Mercurial repository')
                execute(write_changelog, ("ChangeLog", ))
            else:
                cl_time = os.stat("ChangeLog").st_mtime
                repo = hg.repository(None)
                tip_time = repo.changelog.read(repo.lookup("tip"))[2][0]
                if tip_time > cl_time:
                    execute(write_changelog, ("ChangeLog", ))
        else:
            print("Unable to build ChangeLog, dir is not a Mercurial clone")

class HgSdist(sdist):
    """
    Create a source distribution tarball

    @see: C{sdist}
    @ivar repo: Mercurial repository object
    """
    description = gen_desc(__doc__)

    def initialize_options(self):
        sdist.initialize_options(self)
        if not MERCURIAL:
            raise DistutilsModuleError("Mercurial import failed")
        self.repo = hg.repository(None)

    def get_file_list(self):
        changeset = self.repo.changectx()
        self.filelist.extend(changeset.manifest().keys())
        self.filelist.extend([".hg_version", "ChangeLog"])
        self.filelist.extend(glob("*.html"))
        self.filelist.extend(glob("doc/*.html"))
        for path, dir, filenames in os.walk("html"):
            for file in filenames:
                self.filelist.append(os.path.join(path, file))
        sdist.get_file_list(self)
        self.filelist.sort()

    def make_distribution(self):
        execute(self.write_version, ())
        execute(write_changelog, ("ChangeLog", ))
        sdist.make_distribution(self)

    def write_version(self):
        """
        Store the current Mercurial changeset in a file
        """
        repo_id = hg.short((self.repo.lookup("tip")))
        write_file(".hg_version", ("%s tip\n" % repo_id, ))

class MyClean(clean):
    """
    Clean built and temporary files

    @see: C{clean}
    """
    description = gen_desc(__doc__)

    def run(self):
        clean.run(self)
        if self.all:
            for file in [".hg_version", "ChangeLog", "MANIFEST"] \
                + glob("*.html") + glob("doc/*.html") \
                + glob("*.pyc"):
                os.path.exists(file) and os.unlink(file)
            execute(shutil.rmtree, ("html", True))

class Snapshot(NoOptsCommand):
    """
    Build a daily snapshot tarball
    """
    description = gen_desc(__doc__)
    user_options = []

    def run(self):
        snapshot_name="pyisbn-%s" % strftime("%Y-%m-%d")
        execute(shutil.rmtree, ("dist/%s" % snapshot_name, True))
        execute(self.generate_tree, ("dist/%s" % snapshot_name, ))
        execute(write_changelog, ("dist/%s/ChangeLog" % snapshot_name, ))
        execute(make_archive, ("dist/%s" % snapshot_name, "bztar", "dist",
                               snapshot_name))
        execute(shutil.rmtree, ("dist/%s" % snapshot_name, ))

    def generate_tree(self, snapshot_name):
        """
        Generate a clean Mercurial clone
        """
        check_call(["hg", "archive", snapshot_name])

class MyTest(NoOptsCommand):
    user_options = [
        ('exit-on-fail', 'x',
         "Exit on first failure"),
    ]
    boolean_options = ['exit-on-fail']

    def initialize_options(self):
        self.exit_on_fail = False
        self.doctest_opts = doctest.REPORT_UDIFF|doctest.NORMALIZE_WHITESPACE
        self.extraglobs = {"test_isbns": test_isbns}

class TestDoc(MyTest):
    """
    Test documentation's code examples

    @see: C{MyTest}
    """
    description = gen_desc(__doc__)

    def run(self):
        for filename in sorted(['README', ]):
            print('Testing documentation file %s' % filename)
            fails, tests = doctest.testfile(filename,
                                            optionflags=self.doctest_opts,
                                            extraglobs=self.extraglobs)
            if self.exit_on_fail and not fails == 0:
                sys.exit(1)

class TestMod(MyTest):
    """
    Test module's doctest examples

    @see: C{MyTest}
    """
    description = gen_desc(__doc__)

    def run(self):
        for filename in sorted(["ISBN.py", ]):
            print('Testing module file %s' % filename)
            module = os.path.splitext(filename)[0].replace("/", ".")
            if module.endswith("__init__"):
                module = module[:-9]
            fails, tests = doctest.testmod(sys.modules[module],
                                           optionflags=self.doctest_opts,
                                           extraglobs=self.extraglobs)
            if self.exit_on_fail and not fails == 0:
                sys.exit(1)

if __name__ == "__main__":
    setup(
        name = "pyisbn",
        version = ISBN.__version__,
        description = ISBN.__doc__.splitlines()[1],
        long_description = sub("C{([^}]*)}", r"``\1``",
                               ISBN.__doc__[:ISBN.__doc__.rfind('\n\n')]),
        author = parseaddr(ISBN.__author__)[0],
        author_email = parseaddr(ISBN.__author__)[1],
        url = BASE_URL + "projects/pyisbn.html",
        download_url = "%sdata/pyisbn-%s.tar.bz2" \
                       % (BASE_URL, ISBN.__version__),
        py_modules = ['ISBN'],
        license = ISBN.__license__,
        keywords = ['ISBN', 'ISBN-10', 'ISBN-13', 'SBN'],
        classifiers = [
            'Development Status :: 4 - Beta',
            'Intended Audience :: Other Audience',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Other/Nonlisted Topic',
            'Topic :: Text Processing :: Indexing',
        ],
        options = {'sdist': {'formats': 'bztar'}},
        cmdclass = {
            'build_doc': BuildDoc, 'clean': MyClean, 'sdist': HgSdist,
            'snapshot': Snapshot, 'test_doc': TestDoc, 'test_mod': TestMod,
        },
)

