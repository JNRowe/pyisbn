#! /usr/bin/python -tt
# vim: set sw=4 sts=4 et tw=80 fileencoding=utf-8:
#
"""setup - Generic project setup.py"""
# Copyright (C) 2007-2008  James Rowe
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
import time

try:
    from setuptools import setup
    from setuptools.command.sdist import (finders, sdist)
    from setuptools import Command
    from distutils.util import convert_path
    SETUPTOOLS = True #: True if ``setuptools`` is installed
except ImportError:
    from distutils.core import setup
    from distutils.command.sdist import sdist
    from distutils.cmd import Command
    SETUPTOOLS = False

from distutils.archive_util import make_archive
from distutils.command.clean import clean
from distutils.dep_util import newer
from distutils.errors import (DistutilsFileError, DistutilsModuleError)
from distutils.file_util import write_file
from distutils.util import execute
from email.utils import parseaddr
from glob import glob
from subprocess import (check_call, PIPE, Popen)

try:
    from docutils.core import publish_cmdline
    from docutils import nodes
    from docutils.parsers.rst import directives
    DOCUTILS = True #: True if ``docutils`` module is available
except ImportError:
    DOCUTILS = False
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import HtmlFormatter
    PYGMENTS = True #: True if ``pygments`` module is available
except ImportError:
    PYGMENTS = False
try:
    from epydoc import cli
    EPYDOC = True #: True if ``epydoc`` module is available
except ImportError:
    EPYDOC = False

import __pkg_data__
import test

BASE_URL = "http://www.jnrowe.ukfsn.org/" #: Base URL for links
PROJECT_URL = "%sprojects/%s.html" % (BASE_URL, __pkg_data__.MODULE.__name__)

if sys.version_info < (2, 5, 0, 'final'):
    raise SystemError("Requires Python v2.5+")

#{ Generated data file functions

def write_changelog(filename):
    """Generate a ChangeLog from Mercurial repo

    :Parameters:
        filename : `str`
            Filename to write ChangeLog to

    """
    if os.path.isdir(".hg"):
        print('Building ChangeLog from Mercurial repository')
        try:
            call_hg(["log", "--exclude", ".be/", "--no-merges",
                     "--style", "changelog"],
                    stdout=open(filename, "w"))
        finally:
            # Remove the ChangeLog if call_hg() failed
            if os.stat(filename).st_size == 0:
                os.unlink(filename)
    else:
        print("Unable to build ChangeLog, dir is not a Mercurial clone")
        return False

def write_manifest(files):
    """Generate a MANIFEST file

    :Parameters:
        files : `list`
            Filenames to include in MANIFEST

    """
    manifest = open("MANIFEST", "w")
    manifest.write("\n".join(sorted(files)) + "\n")
    manifest.close()

#}

#{ Implementation utilities

def call_hg(options, *args, **kwargs):
    """Call Mercurial command line tools

    :Parameters:
        options : `list`
            Mercurial command options
        *args : `list`
            Positional arguments for ``subprocess.Popen``
        **kwargs : `dict`
            Keyword arguments for ``subprocess.Popen``
    :rtype: `str`
    :return: Mercurial command output
    :raise OSError: `hg` command not found

    """
    if not "stdout" in kwargs:
        kwargs["stdout"] = PIPE
    options.insert(0, "hg")
    try:
        process = Popen(options, *args, **kwargs)
    except OSError, e:
        print("Error calling `hg`, is Mercurial installed? [%s]" % e)
        sys.exit(1)
    process.wait()
    if not process.returncode == 0:
        print("`hg' completed with %i return code" % process.returncode)
        sys.exit(process.returncode)
    return process.communicate()[0]

def gen_desc(doc):
    """Pull simple description from docstring

    :Parameters:
        doc : `str`
            Docstring to manipulate
    :rtype: str
    :return: Description string suitable for ``Command`` class's description

    """
    desc = doc.splitlines()[0].lstrip()
    return desc[0].lower() + desc[1:]


class NoOptsCommand(Command):
    """Abstract class for simple ``distutils`` command implementation"""

    def initialize_options(self):
        """Set default values for options"""
        pass

    def finalize_options(self):
        """Finalize, and test validity, of options"""
        pass

#}


class BuildDoc(NoOptsCommand):
    """Build project documentation

    :Ivariables:
        force
            Force documentation generation

    """
    description = gen_desc(__doc__)
    user_options = [
        ('force', 'f',
         "force documentation generation"),
    ] #: `BuildDoc`'s option mapping
    boolean_options = ['force'] #: `BuildDoc` class' boolean options

    def initialize_options(self):
        """Set default values for options"""
        self.force = False

    def run(self):
        """Build the required documentation"""
        if not DOCUTILS:
            raise DistutilsModuleError("docutils import failed, "
                                       "can't generate documentation")
        if not PYGMENTS:
            # This could be a warning with conditional support for users, but
            # how would coloured output be guaranteed in releases?
            raise DistutilsModuleError("pygments import failed, "
                                       "can't generate documentation")

        pygments_formatter = HtmlFormatter()

        def pygments_directive(name, arguments, options, content, lineno,
                               content_offset, block_text, state,
                               state_machine):
            """Code colourising directive for ``docutils``"""
            try:
                lexer = get_lexer_by_name(arguments[0])
            except ValueError:
                # no lexer found - use the text one instead of raising an
                # exception
                lexer = get_lexer_by_name('text')
            parsed = highlight(u'\n'.join(content), lexer, pygments_formatter)
            return [nodes.raw('', parsed, format='html')]
        pygments_directive.arguments = (1, 0, 1)
        pygments_directive.content = 1
        directives.register_directive('code-block', pygments_directive)

        for source in sorted(["NEWS", "README"] + glob('doc/*.txt')):
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
        files = glob("%s/*.py" % __pkg_data__.MODULE.__name__)
        files.extend(["%s.py" % i.__name__ for i in __pkg_data__.SCRIPTS])
        if self.force \
            or any(newer(filename, "html/index.html") for filename in files):
            print("Building API documentation")
            if not self.dry_run:
                saved_args = sys.argv[1:]
                sys.argv[1:] = ["--name", __pkg_data__.MODULE.__name__,
                                "--url", PROJECT_URL,
                                "--docformat", "restructuredtext",
                                "--no-sourcecode"]
                if __pkg_data__.GRAPH_TYPE:
                    sys.argv.append("--graph=%s" % __pkg_data__.GRAPH_TYPE)
                sys.argv.extend(files)
                cli.cli()
                sys.argv[1:] = saved_args
        if os.path.isdir(".hg"):
            if self.force or not os.path.isfile("ChangeLog"):
                execute(write_changelog, ("ChangeLog", ))
            else:
                output = call_hg(["tip", "--template", "'{date}'"])
                tip_time = float(output[1:output.find("-")])
                cl_time = os.stat("ChangeLog").st_mtime
                if tip_time > cl_time:
                    execute(write_changelog, ("ChangeLog", ))
        else:
            print("Unable to build ChangeLog, this directory is not a "
                  "Mercurial clone")

        if hasattr(__pkg_data__, "BuildDoc_run"):
            __pkg_data__.BuildDoc_run(self.dry_run, self.force)


#{ Distribution utilities

def hg_finder(dirname, none):
    """Find files for distribution tarball

    This is only used when ``setuptools`` is imported, simply to create a valid
    list of files to distribute.  Standard setuptools only works with CVS.
    Without this it *appears* to work, but only distributes a very small subset
    of the package.

    :see: `MySdist.get_file_list`

    :Parameters:
        dirname : `str`
            Base directory to search for files
        none : any
            Just for compatibility
    """
    # setuptools documentation says this shouldn't be a hard fail, but we won't
    # do that as it makes builds entirely unpredictable
    output = call_hg(["locate", ])
    # Include all but Bugs Everywhere data from repo in tarballs
    distributed_files = filter(lambda s: not s.startswith(".be/"),
                               output.splitlines())
    distributed_files.extend([".hg_version", "ChangeLog"])
    distributed_files.extend(glob("*.html"))
    distributed_files.extend(glob("doc/*.html"))
    for path, directory, filenames in os.walk("html"):
        for filename in filenames:
            distributed_files.append(os.path.join(path, filename))
    return distributed_files
if SETUPTOOLS:
    finders.append((convert_path('.hg/dirstate'), hg_finder))

class HgSdist(sdist):
    """Create a source distribution tarball

    :see: `sdist`

    :Ivariables:
        repo
            Mercurial repository object

    """
    description = gen_desc(__doc__)
    user_options = [
        ('force-build', 'b', "force build with stale version numbere"),
    ] + sdist.user_options #: `HgSdist`'s option mapping
    boolean_options = ['force-build']

    def initialize_options(self):
        """Set default values for options"""
        sdist.initialize_options(self)
        self.force_build = False
        output = call_hg(["status", "-mard"])
        if not len(output) == 0:
            raise DistutilsFileError("Uncommitted changes!")

    def get_file_list(self):
        """Generate MANIFEST file contents from Mercurial tree"""
        output = call_hg(["locate", ])
        # Include all but Bugs Everywhere data from repo in tarballs
        manifest_files = filter(lambda s: not s.startswith(".be/"),
                                output.splitlines())
        manifest_files.extend([".hg_version", "ChangeLog"])
        manifest_files.extend(glob("*.html"))
        manifest_files.extend(glob("doc/*.html"))
        for path, directory, filenames in os.walk("html"):
            for filename in filenames:
                manifest_files.append(os.path.join(path, filename))
        execute(write_manifest, [manifest_files], "writing MANIFEST")
        sdist.get_file_list(self)

    def make_distribution(self):
        """Update versioning data and build distribution"""
        news_format = "%s - " % __pkg_data__.MODULE.__version__
        news_matches = filter(lambda s: s.startswith(news_format), open("NEWS"))
        if not any(news_matches):
            print("NEWS entry for `%s' missing"
                  % __pkg_data__.MODULE.__version__)
            sys.exit(1)
        news_time = time.mktime(time.strptime(news_matches[0].split()[-1],
                                "%Y-%m-%d"))
        if time.time() - news_time > 86400 and not self.force_build:
            print("NEWS entry is older than a day, version may not have been "
                  "updated")
            sys.exit(1)
        execute(self.write_version, ())
        sdist.make_distribution(self)

    def write_version(self):
        """Store the current Mercurial changeset in a file"""
        # This could use `hg identify' but that output other unused information
        output = call_hg(["tip", "--template", "'{node|short}'"])
        repo_id = output[1:-1]
        write_file(".hg_version", ("%s tip\n" % repo_id, ))


class Snapshot(NoOptsCommand):
    """Build a daily snapshot tarball"""
    description = gen_desc(__doc__)
    user_options = [] #: `Snapshot`'s option mapping

    def run(self):
        """Prepare and create tarball"""
        snapshot_name = "%s-%s" % (__pkg_data__.MODULE.__name__,
                                   time.strftime("%Y-%m-%d"))
        snapshot_location = "dist/%s" % snapshot_name
        if os.path.isdir(snapshot_location):
            execute(shutil.rmtree, (snapshot_location, ))
        execute(self.generate_tree, (snapshot_location, ))
        execute(write_changelog, ("%s/ChangeLog" % snapshot_location, ))
        execute(make_archive, (snapshot_location, "bztar", "dist",
                               snapshot_name))
        execute(shutil.rmtree, (snapshot_location, ))

    @staticmethod
    def generate_tree(snapshot_name):
        """Generate a clean Mercurial clone"""
        check_call(["hg", "archive", snapshot_name])
        shutil.rmtree("%s/.be" % snapshot_name)

#}


class MyClean(clean):
    """Clean built and temporary files

    :see: `clean`

    """
    description = gen_desc(__doc__)

    def run(self):
        """Remove built and temporary files"""
        clean.run(self)
        if self.all:
            for filename in [".hg_version", "ChangeLog", "MANIFEST"] \
                + glob("*.html") + glob("doc/*.html") \
                + glob("%s/*.pyc" % __pkg_data__.MODULE.__name__):
                if os.path.exists(filename):
                    os.unlink(filename)
            execute(shutil.rmtree, ("html", True))
        if hasattr(__pkg_data__, "MyClean_run"):
            __pkg_data__.MyClean_run(self.dry_run, self.force)


#{ Testing utilities

class MyTest(NoOptsCommand):
    """Abstract class for test command implementations"""
    user_options = [
        ('exit-on-fail', 'x',
         "exit on first failure"),
    ] #: `MyTest`'s option mapping
    boolean_options = ['exit-on-fail']

    def initialize_options(self):
        """Set default values for options"""
        self.exit_on_fail = False
        self.doctest_opts = doctest.REPORT_UDIFF|doctest.NORMALIZE_WHITESPACE
        self.extraglobs = {
            "test_isbns": test.test_isbns,
        } #: Mock objects to include for test framework
        if hasattr(__pkg_data__, "TEST_EXTRAGLOBS"):
            for value in __pkg_data__.TEST_EXTRAGLOBS:
                self.extraglobs[value] = getattr(test.mock, value)


class TestDoc(MyTest):
    """Test documentation's code examples

    :see: `MyTest`

    """
    description = gen_desc(__doc__)

    def run(self):
        """Run the documentation code examples"""
        tot_fails = 0
        tot_tests = 0
        for filename in sorted(['README'] + glob("doc/*.txt")):
            print('  Testing documentation file %s' % filename)
            fails, tests = doctest.testfile(filename,
                                            optionflags=self.doctest_opts,
                                            extraglobs=self.extraglobs)
            print("    %i tests run, %i failed" % (tests, fails))
            if self.exit_on_fail and not fails == 0:
                sys.exit(1)
            tot_fails += fails
            tot_tests += tests
        print("Total of %i tests run, %i failed" % (tot_tests, tot_fails))
        if hasattr(__pkg_data__, "TestDoc_run"):
            __pkg_data__.TestDoc_run(self.dry_run, self.force)


class TestCode(MyTest):
    """Test script and module's ``doctest`` examples

    :see: `MyTest`

    """
    description = gen_desc(__doc__)

    def run(self):
        """Run the source's docstring code examples"""
        files = glob("%s/*.py" % __pkg_data__.MODULE.__name__)
        files.extend(["%s.py" % i.__name__ for i in __pkg_data__.SCRIPTS])
        tot_fails = 0
        tot_tests = 0
        for filename in sorted(files):
            print('  Testing python file %s' % filename)
            module = os.path.splitext(filename)[0].replace("/", ".")
            if module.endswith("__init__"):
                module = module[:-9]
            fails, tests = doctest.testmod(sys.modules[module],
                                           optionflags=self.doctest_opts,
                                           extraglobs=self.extraglobs)
            print("    %i tests run, %i failed" % (tests, fails))
            if self.exit_on_fail and not fails == 0:
                sys.exit(1)
            tot_fails += fails
            tot_tests += tests
        print("Total of %i tests run, %i failed" % (tot_tests, tot_fails))
        if hasattr(__pkg_data__, "TestCode_run"):
            __pkg_data__.TestCode_run(self.dry_run, self.force)

#}

def main():
    # Force tests to be run, and documentation to be built, before creating a
    # release.
    if "sdist" in sys.argv:
        for test in ("test_code", "test_doc"):
            if not test in sys.argv:
                sys.argv = [sys.argv[0], ] + [test, "-x"] + sys.argv[1:]
        if not "build_doc" in sys.argv:
            sys.argv.insert(1, "build_doc")

    setup(
        name=__pkg_data__.MODULE.__name__,
        version=__pkg_data__.MODULE.__version__,
        description=__pkg_data__.DESCRIPTION,
        long_description=__pkg_data__.LONG_DESCRIPTION,
        author=parseaddr(__pkg_data__.MODULE.__author__)[0],
        author_email=parseaddr(__pkg_data__.MODULE.__author__)[1],
        url=PROJECT_URL,
        download_url="%sdata/%s-%s.tar.bz2" \
            % (BASE_URL, __pkg_data__.MODULE.__name__,
               __pkg_data__.MODULE.__version__),
        packages=[__pkg_data__.MODULE.__name__],
        scripts=["%s.py" % i.__name__ for i in __pkg_data__.SCRIPTS],
        license=__pkg_data__.MODULE.__license__,
        keywords=__pkg_data__.KEYWORDS,
        classifiers=__pkg_data__.CLASSIFIERS,
        obsoletes=__pkg_data__.OBSOLETES,
        options={'sdist': {'formats': 'bztar'}},
        cmdclass={
            'build_doc': BuildDoc, 'clean': MyClean, 'sdist': HgSdist,
            'snapshot': Snapshot, 'test_doc': TestDoc, 'test_code': TestCode,
        },
    )

if __name__ == "__main__":
    main()

