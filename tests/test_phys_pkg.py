# -*- coding: utf-8 -*-
#
# test_phys_pkg.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of opc-diag and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Unit tests for phys_pkg module"""

from opcdiag.phys_pkg import BlobCollection, DirPhysPkg, PhysPkg, ZipPhysPkg

from .unitutil import relpath


MINI_DIR_PKG_PATH = relpath('test_files/mini_pkg')
MINI_ZIP_PKG_PATH = relpath('test_files/mini_pkg.zip')


class DescribePhysPkg(object):

    def it_should_construct_the_appropriate_subclass(self):
        pkg = PhysPkg.read(MINI_ZIP_PKG_PATH)
        assert isinstance(pkg, ZipPhysPkg)
        pkg = PhysPkg.read(MINI_DIR_PKG_PATH)
        assert isinstance(pkg, DirPhysPkg)

    def it_can_iterate_over_pkg_blobs(self):
        # fixture ----------------------
        blobs = BlobCollection((('foo', 'bar'), ('baz', 'zam')))
        phys_pkg = PhysPkg(blobs, None)
        # exercise ---------------------
        actual_blobs = dict([item for item in phys_pkg])
        # verify -----------------------
        assert actual_blobs == blobs
