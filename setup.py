#!/usr/bin/env python

import os
import re

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup

MAIN_PKG = 'opcdiag'

thisdir = os.path.dirname(__file__)

history_path = os.path.join(thisdir, 'HISTORY.rst')
init_py_path = os.path.join(thisdir, MAIN_PKG, '__init__.py')
license_path = os.path.join(thisdir, 'LICENSE')
readme_path = os.path.join(thisdir, 'README.rst')

with open(history_path) as f:
    history = f.read()
with open(license_path) as f:
    license = f.read()
with open(readme_path) as f:
    readme = f.read()
with open(init_py_path) as f:
    version = re.search("__version__ = '([^']+)'", f.read()).group(1)

NAME = 'opc-diag'
VERSION = version
DESCRIPTION = (
    'Browse and diff Microsoft Office .docx, .xlsx, and .pptx files.'
)

LONG_DESCRIPTION = '%s\n\n%s' % (readme, history)

KEYWORDS = 'opc open xml diff docx pptx xslx office'
AUTHOR = 'Steve Canny'
AUTHOR_EMAIL = 'python-opc@googlegroups.com'
URL = 'https://github.com/python-openxml/opc-diag'
LICENSE = license

MODULES = ['ez_setup']
PACKAGES = ['opcdiag']

ENTRY_POINTS = {
    'console_scripts': [
        'opc = opcdiag.cli:main'
    ]
}

INSTALL_REQUIRES = [
    'lxml >= 3.0',
]

TEST_SUITE = 'tests'
TESTS_REQUIRE = [
    'behave >= 1.2.3',
    'mock >= 1.0.1',
    'pytest >= 2.3.4'
]

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Topic :: Office/Business :: Office Suites',
    'Topic :: Software Development :: Libraries'
]

params = {
    'name':             NAME,
    'version':          VERSION,
    'description':      DESCRIPTION,
    'keywords':         KEYWORDS,
    'long_description': LONG_DESCRIPTION,
    'author':           AUTHOR,
    'author_email':     AUTHOR_EMAIL,
    'url':              URL,
    'license':          LICENSE,
    'packages':         PACKAGES,
    'py_modules':       MODULES,
    'entry_points':     ENTRY_POINTS,
    'install_requires': INSTALL_REQUIRES,
    'tests_require':    TESTS_REQUIRE,
    'test_suite':       TEST_SUITE,
    'classifiers':      CLASSIFIERS,
}

setup(**params)
