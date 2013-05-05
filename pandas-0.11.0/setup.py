#!/usr/bin/env python

"""
Parts of this file were taken from the pyzmq project
(https://github.com/zeromq/pyzmq) which have been permitted for use under the
BSD license. Parts are from lxml (https://github.com/lxml/lxml)
"""

import os
import sys
import shutil
import warnings

# may need to work around setuptools bug by providing a fake Pyrex
try:
    import Cython
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "fake_pyrex"))
except ImportError:
    pass

# try bootstrapping setuptools if it doesn't exist
try:
    import pkg_resources
    try:
        pkg_resources.require("setuptools>=0.6c5")
    except pkg_resources.VersionConflict:
        from ez_setup import use_setuptools
        use_setuptools(version="0.6c5")
    from setuptools import setup, Command
    _have_setuptools = True
except ImportError:
    # no setuptools installed
    from distutils.core import setup, Command
    _have_setuptools = False

setuptools_kwargs = {}
if sys.version_info[0] >= 3:

    min_numpy_ver = 1.6
    if sys.version_info[1] >= 3:  # 3.3 needs numpy 1.7+
        min_numpy_ver = "1.7.0b2"

    setuptools_kwargs = {'use_2to3': True,
                         'zip_safe': False,
                         'install_requires': ['python-dateutil >= 2',
                                              'pytz',
                                              'numpy >= %s' % min_numpy_ver],
                         'use_2to3_exclude_fixers': ['lib2to3.fixes.fix_next',
                                                     ],
                         }
    if not _have_setuptools:
        sys.exit("need setuptools/distribute for Py3k"
                 "\n$ pip install distribute")

else:
    setuptools_kwargs = {
        'install_requires': ['python-dateutil',
                             'pytz',
                             'numpy >= 1.6.1'],
        'zip_safe': False,
    }

    if not _have_setuptools:
        try:
            import numpy
            import dateutil
            setuptools_kwargs = {}
        except ImportError:
            sys.exit("install requires: 'python-dateutil < 2','numpy'."
                     "  use pip or easy_install."
                     "\n   $ pip install 'python-dateutil < 2' 'numpy'")

from distutils.extension import Extension
from distutils.command.build import build
from distutils.command.sdist import sdist
from distutils.command.build_ext import build_ext as _build_ext

try:
    from Cython.Distutils import build_ext as _build_ext
    # from Cython.Distutils import Extension # to get pyrex debugging symbols
    cython = True
except ImportError:
    cython = False

from os.path import splitext, basename, join as pjoin


class build_ext(_build_ext):
    def build_extensions(self):
        numpy_incl = pkg_resources.resource_filename('numpy', 'core/include')

        for ext in self.extensions:
            if hasattr(ext, 'include_dirs') and not numpy_incl in ext.include_dirs:
                ext.include_dirs.append(numpy_incl)
        _build_ext.build_extensions(self)


DESCRIPTION = ("Powerful data structures for data analysis, time series,"
               "and statistics")
LONG_DESCRIPTION = """
**pandas** is a Python package providing fast, flexible, and expressive data
structures designed to make working with structured (tabular, multidimensional,
potentially heterogeneous) and time series data both easy and intuitive. It
aims to be the fundamental high-level building block for doing practical,
**real world** data analysis in Python. Additionally, it has the broader goal
of becoming **the most powerful and flexible open source data analysis /
manipulation tool available in any language**. It is already well on its way
toward this goal.

pandas is well suited for many different kinds of data:

  - Tabular data with heterogeneously-typed columns, as in an SQL table or
    Excel spreadsheet
  - Ordered and unordered (not necessarily fixed-frequency) time series data.
  - Arbitrary matrix data (homogeneously typed or heterogeneous) with row and
    column labels
  - Any other form of observational / statistical data sets. The data actually
    need not be labeled at all to be placed into a pandas data structure

The two primary data structures of pandas, Series (1-dimensional) and DataFrame
(2-dimensional), handle the vast majority of typical use cases in finance,
statistics, social science, and many areas of engineering. For R users,
DataFrame provides everything that R's ``data.frame`` provides and much
more. pandas is built on top of `NumPy <http://www.numpy.org>`__ and is
intended to integrate well within a scientific computing environment with many
other 3rd party libraries.

Here are just a few of the things that pandas does well:

  - Easy handling of **missing data** (represented as NaN) in floating point as
    well as non-floating point data
  - Size mutability: columns can be **inserted and deleted** from DataFrame and
    higher dimensional objects
  - Automatic and explicit **data alignment**: objects can be explicitly
    aligned to a set of labels, or the user can simply ignore the labels and
    let `Series`, `DataFrame`, etc. automatically align the data for you in
    computations
  - Powerful, flexible **group by** functionality to perform
    split-apply-combine operations on data sets, for both aggregating and
    transforming data
  - Make it **easy to convert** ragged, differently-indexed data in other
    Python and NumPy data structures into DataFrame objects
  - Intelligent label-based **slicing**, **fancy indexing**, and **subsetting**
    of large data sets
  - Intuitive **merging** and **joining** data sets
  - Flexible **reshaping** and pivoting of data sets
  - **Hierarchical** labeling of axes (possible to have multiple labels per
    tick)
  - Robust IO tools for loading data from **flat files** (CSV and delimited),
    Excel files, databases, and saving / loading data from the ultrafast **HDF5
    format**
  - **Time series**-specific functionality: date range generation and frequency
    conversion, moving window statistics, moving window linear regressions,
    date shifting and lagging, etc.

Many of these principles are here to address the shortcomings frequently
experienced using other languages / scientific research environments. For data
scientists, working with data is typically divided into multiple stages:
munging and cleaning data, analyzing / modeling it, then organizing the results
of the analysis into a form suitable for plotting or tabular display. pandas is
the ideal tool for all of these tasks.

Note
----
Windows binaries built against NumPy 1.6.1
"""

DISTNAME = 'pandas'
LICENSE = 'BSD'
AUTHOR = "The PyData Development Team"
EMAIL = "pydata@googlegroups.com"
URL = "http://pandas.pydata.org"
DOWNLOAD_URL = ''
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Operating System :: OS Independent',
    'Intended Audience :: Science/Research',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Programming Language :: Cython',
    'Topic :: Scientific/Engineering',
]

MAJOR = 0
MINOR = 11
MICRO = 0
ISRELEASED = True
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)
QUALIFIER = ''

FULLVERSION = VERSION
if not ISRELEASED:
    FULLVERSION += '.dev'
    try:
        import subprocess
        try:
            pipe = subprocess.Popen(["git", "rev-parse", "--short", "HEAD"],
                                    stdout=subprocess.PIPE).stdout
        except OSError:
            # msysgit compatibility
            pipe = subprocess.Popen(
                ["git.cmd", "rev-parse", "--short", "HEAD"],
                stdout=subprocess.PIPE).stdout
        rev = pipe.read().strip()
        # makes distutils blow up on Python 2.7
        if sys.version_info[0] >= 3:
            rev = rev.decode('ascii')

        FULLVERSION += "-%s" % rev
    except:
        warnings.warn("WARNING: Couldn't get git revision")
else:
    FULLVERSION += QUALIFIER


def write_version_py(filename=None):
    cnt = """\
version = '%s'
short_version = '%s'
"""
    if not filename:
        filename = os.path.join(
            os.path.dirname(__file__), 'pandas', 'version.py')

    a = open(filename, 'w')
    try:
        a.write(cnt % (FULLVERSION, VERSION))
    finally:
        a.close()


class CleanCommand(Command):
    """Custom distutils command to clean the .so and .pyc files."""

    user_options = [("all", "a", "")]

    def initialize_options(self):
        self.all = True
        self._clean_me = []
        self._clean_trees = []
        self._clean_exclude = ['np_datetime.c',
                               'np_datetime_strings.c',
                               'period.c',
                               'tokenizer.c',
                               'io.c']

        for root, dirs, files in list(os.walk('pandas')):
            for f in files:
                if f in self._clean_exclude:
                    continue
                if os.path.splitext(f)[-1] in ('.pyc', '.so', '.o',
                                               '.pyo',
                                               '.pyd', '.c', '.orig'):
                    self._clean_me.append(pjoin(root, f))
            for d in dirs:
                if d == '__pycache__':
                    self._clean_trees.append(pjoin(root, d))

        for d in ('build',):
            if os.path.exists(d):
                self._clean_trees.append(d)

    def finalize_options(self):
        pass

    def run(self):
        for clean_me in self._clean_me:
            try:
                os.unlink(clean_me)
            except Exception:
                pass
        for clean_tree in self._clean_trees:
            try:
                shutil.rmtree(clean_tree)
            except Exception:
                pass


class CheckSDist(sdist):
    """Custom sdist that ensures Cython has compiled all pyx files to c."""

    _pyxfiles = ['pandas/lib.pyx',
                 'pandas/hashtable.pyx',
                 'pandas/tslib.pyx',
                 'pandas/index.pyx',
                 'pandas/algos.pyx',
                 'pandas/src/parser.pyx',
                 'pandas/src/sparse.pyx']

    def initialize_options(self):
        sdist.initialize_options(self)

        '''
        self._pyxfiles = []
        for root, dirs, files in os.walk('pandas'):
            for f in files:
                if f.endswith('.pyx'):
                    self._pyxfiles.append(pjoin(root, f))
        '''

    def run(self):
        if 'cython' in cmdclass:
            self.run_command('cython')
        else:
            for pyxfile in self._pyxfiles:
                cfile = pyxfile[:-3] + 'c'
                msg = "C-source file '%s' not found." % (cfile) +\
                    " Run 'setup.py cython' before sdist."
                assert os.path.isfile(cfile), msg
        sdist.run(self)


class CheckingBuildExt(build_ext):
    """Subclass build_ext to get clearer report if Cython is necessary."""

    def check_cython_extensions(self, extensions):
        for ext in extensions:
            for src in ext.sources:
                if not os.path.exists(src):
                    raise Exception("""Cython-generated file '%s' not found.
                Cython is required to compile pandas from a development branch.
                Please install Cython or download a release package of pandas.
                """ % src)

    def build_extensions(self):
        self.check_cython_extensions(self.extensions)
        build_ext.build_extensions(self)


class CythonCommand(build_ext):
    """Custom distutils command subclassed from Cython.Distutils.build_ext
    to compile pyx->c, and stop there. All this does is override the
    C-compile method build_extension() with a no-op."""
    def build_extension(self, ext):
        pass


class DummyBuildSrc(Command):
    """ numpy's build_src command interferes with Cython's build_ext.
    """
    user_options = []

    def initialize_options(self):
        self.py_modules_dict = {}

    def finalize_options(self):
        pass

    def run(self):
        pass

cmdclass = {'clean': CleanCommand,
            'build': build,
            'sdist': CheckSDist}

if cython:
    suffix = '.pyx'
    cmdclass['build_ext'] = CheckingBuildExt
    cmdclass['cython'] = CythonCommand
else:
    suffix = '.c'
    cmdclass['build_src'] = DummyBuildSrc
    cmdclass['build_ext'] = CheckingBuildExt

lib_depends = ['reduce', 'inference', 'properties']


def srcpath(name=None, suffix='.pyx', subdir='src'):
    return pjoin('pandas', subdir, name + suffix)

if suffix == '.pyx':
    lib_depends = [srcpath(f, suffix='.pyx') for f in lib_depends]
    lib_depends.append('pandas/src/util.pxd')
else:
    lib_depends = []
    plib_depends = []

common_include = ['pandas/src/klib', 'pandas/src']


def pxd(name):
    return os.path.abspath(pjoin('pandas', name + '.pxd'))


lib_depends = lib_depends + ['pandas/src/numpy_helper.h',
                             'pandas/src/parse_helper.h']


tseries_depends = ['pandas/src/datetime/np_datetime.h',
                   'pandas/src/datetime/np_datetime_strings.h',
                   'pandas/src/period.h']


# some linux distros require it
libraries = ['m'] if 'win32' not in sys.platform else []

ext_data = dict(
    lib={'pyxfile': 'lib',
         'pxdfiles': [],
         'depends': lib_depends},
    hashtable={'pyxfile': 'hashtable',
               'pxdfiles': ['hashtable']},
    tslib={'pyxfile': 'tslib',
           'depends': tseries_depends,
           'sources': ['pandas/src/datetime/np_datetime.c',
                       'pandas/src/datetime/np_datetime_strings.c',
                       'pandas/src/period.c']},
    index={'pyxfile': 'index',
           'sources': ['pandas/src/datetime/np_datetime.c',
                       'pandas/src/datetime/np_datetime_strings.c']},
    algos={'pyxfile': 'algos',
           'depends': [srcpath('generated', suffix='.pyx')]},
)

extensions = []

for name, data in ext_data.items():
    sources = [srcpath(data['pyxfile'], suffix=suffix, subdir='')]
    pxds = [pxd(x) for x in data.get('pxdfiles', [])]
    if suffix == '.pyx' and pxds:
        sources.extend(pxds)

    sources.extend(data.get('sources', []))

    include = data.get('include', common_include)

    obj = Extension('pandas.%s' % name,
                    sources=sources,
                    depends=data.get('depends', []),
                    include_dirs=include)

    extensions.append(obj)


sparse_ext = Extension('pandas._sparse',
                       sources=[srcpath('sparse', suffix=suffix)],
                       include_dirs=[],
                       libraries=libraries)


parser_ext = Extension('pandas._parser',
                       depends=['pandas/src/parser/tokenizer.h',
                                'pandas/src/parser/io.h',
                                'pandas/src/numpy_helper.h'],
                       sources=[srcpath('parser', suffix=suffix),
                                'pandas/src/parser/tokenizer.c',
                                'pandas/src/parser/io.c',
                                ],
                       include_dirs=common_include)

sandbox_ext = Extension('pandas._sandbox',
                        sources=[srcpath('sandbox', suffix=suffix)],
                        include_dirs=common_include)


cppsandbox_ext = Extension('pandas._cppsandbox',
                           language='c++',
                           sources=[srcpath('cppsandbox', suffix=suffix)],
                           include_dirs=[])

extensions.extend([sparse_ext, parser_ext])

# if not ISRELEASED:
#     extensions.extend([sandbox_ext])

if suffix == '.pyx' and 'setuptools' in sys.modules:
    # undo dumb setuptools bug clobbering .pyx sources back to .c
    for ext in extensions:
        if ext.sources[0].endswith('.c'):
            root, _ = os.path.splitext(ext.sources[0])
            ext.sources[0] = root + suffix


if _have_setuptools:
    setuptools_kwargs["test_suite"] = "nose.collector"

write_version_py()

# The build cache system does string matching below this point.
# if you change something, be careful.

setup(name=DISTNAME,
      version=FULLVERSION,
      maintainer=AUTHOR,
      packages=['pandas',
                'pandas.compat',
                'pandas.core',
                'pandas.io',
                'pandas.rpy',
                'pandas.sandbox',
                'pandas.sparse',
                'pandas.sparse.tests',
                'pandas.stats',
                'pandas.util',
                'pandas.tests',
                'pandas.tools',
                'pandas.tools.tests',
                'pandas.tseries',
                'pandas.tseries.tests',
                'pandas.io.tests',
                'pandas.stats.tests',
                ],
      package_data={'pandas.io': ['tests/data/legacy_hdf/*.h5',
                                  'tests/data/legacy_pickle/0.10.1/*.pickle',
                                  'tests/data/legacy_pickle/0.11.0/*.pickle',
                                  'tests/data/*.csv',
                                  'tests/data/*.txt',
                                  'tests/data/*.xls',
                                  'tests/data/*.xlsx',
                                  'tests/data/*.table'],
                    'pandas.tools': ['tests/*.csv'],
                    'pandas.tests': ['data/*.pickle',
                                     'data/*.csv'],
                    'pandas.tseries.tests': ['data/*.pickle',
                                             'data/*.csv']
                    },
      ext_modules=extensions,
      maintainer_email=EMAIL,
      description=DESCRIPTION,
      license=LICENSE,
      cmdclass=cmdclass,
      url=URL,
      download_url=DOWNLOAD_URL,
      long_description=LONG_DESCRIPTION,
      classifiers=CLASSIFIERS,
      platforms='any',
      **setuptools_kwargs)