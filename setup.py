#!/usr/bin/env python

import codecs
import os
import re
import sys

from ez_setup import use_setuptools

use_setuptools()

from setuptools import setup

MAIN_PKG = "opcdiag"


def _read_from_file(relpath):
    """
    Return the text contained in the file at *relpath* as unicode.
    """
    thisdir = os.path.dirname(__file__)
    path = os.path.join(thisdir, relpath)
    with codecs.open(path, encoding="utf8") as f:
        text = f.read()
    return text


NAME = "opc-diag"

DESCRIPTION = "Browse and diff Microsoft Office .docx, .xlsx, and .pptx files."

KEYWORDS = "opc open xml diff docx pptx xslx office"
AUTHOR = "Steve Canny"
AUTHOR_EMAIL = "python-opc@googlegroups.com"
URL = "https://github.com/python-openxml/opc-diag"

MODULES = ["ez_setup"]
PACKAGES = [MAIN_PKG]

ENTRY_POINTS = {"console_scripts": ["opc = opcdiag.cli:main"]}

INSTALL_REQUIRES = ["lxml >= 3.0"]
if sys.hexversion < 0x02070000:  # argparse only included from Python 2.7
    INSTALL_REQUIRES.append("argparse >= 1.2")

TESTS_REQUIRE = ["behave >= 1.2.3", "mock >= 1.0.1", "pytest >= 2.3.4"]

CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.2",
    "Programming Language :: Python :: 3.3",
    "Topic :: Office/Business :: Office Suites",
    "Topic :: Software Development :: Libraries",
]


# ---------------------------------------------------------------------------
# Everything below is calculated and shouldn't normally need editing
# ---------------------------------------------------------------------------

# read version from main package __init__.py
init_py = _read_from_file(os.path.join(MAIN_PKG, "__init__.py"))
VERSION = re.search("__version__ = '([^']+)'", init_py).group(1)

# license is documented in LICENSE file
LICENSE = _read_from_file("LICENSE")

# compile PyPI page text from README and HISTORY
read_me = _read_from_file("README.rst")
history = _read_from_file("HISTORY.rst")
LONG_DESCRIPTION = "%s\n\n%s" % (read_me, history)

TEST_SUITE = "tests"

params = {
    "name": NAME,
    "version": VERSION,
    "description": DESCRIPTION,
    "keywords": KEYWORDS,
    "long_description": LONG_DESCRIPTION,
    "author": AUTHOR,
    "author_email": AUTHOR_EMAIL,
    "url": URL,
    "license": LICENSE,
    "packages": PACKAGES,
    "py_modules": MODULES,
    "entry_points": ENTRY_POINTS,
    "install_requires": INSTALL_REQUIRES,
    "tests_require": TESTS_REQUIRE,
    "test_suite": TEST_SUITE,
    "classifiers": CLASSIFIERS,
}

setup(**params)
