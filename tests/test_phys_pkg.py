# -*- coding: utf-8 -*-
#
# test_phys_pkg.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of opc-diag and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Unit tests for phys_pkg module"""

from zipfile import ZipFile

from opcdiag.phys_pkg import BlobCollection, DirPhysPkg, PhysPkg, ZipPhysPkg

import pytest

from .unitutil import class_mock, instance_mock, relpath


MINI_DIR_PKG_PATH = relpath('test_files/mini_pkg')
MINI_ZIP_PKG_PATH = relpath('test_files/mini_pkg.zip')
ROOT_URI = relpath('test_files/mini_pkg')


@pytest.fixture
def ZipFile_(request, zip_file_):
    ZipFile_ = class_mock('opcdiag.phys_pkg.ZipFile', request)
    ZipFile_.return_value = zip_file_
    return ZipFile_


@pytest.fixture
def zip_file_(request):
    zip_file_ = instance_mock(ZipFile, request)
    return zip_file_


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


class DescribeDirPhysPkg(object):

    def it_can_construct_from_a_filesystem_package(self):
        """
        Note: integration test, allowing PhysPkg to hit the local filesystem.
        """
        # exercise ---------------------
        dir_phys_pkg = DirPhysPkg.read(MINI_DIR_PKG_PATH)
        # verify -----------------------
        expected_blobs = {'uri_1': b'blob_1\n', 'uri_2': b'blob_2\n'}
        assert dir_phys_pkg._blobs == expected_blobs
        assert dir_phys_pkg._root_uri == ROOT_URI
        assert isinstance(dir_phys_pkg, DirPhysPkg)


class DescribeZipPhysPkg(object):

    def it_can_construct_from_a_filesystem_package(self):
        """
        Note: integration test, allowing PhysPkg to hit ZipFile on the local
        filesystem
        """
        # exercise ---------------------
        zip_phys_pkg = ZipPhysPkg.read(MINI_ZIP_PKG_PATH)
        # verify -----------------------
        expected_blobs = {'uri_1': b'blob_1\n', 'uri_2': b'blob_2\n'}
        assert zip_phys_pkg._blobs == expected_blobs
        assert zip_phys_pkg._root_uri == ROOT_URI
        assert isinstance(zip_phys_pkg, ZipPhysPkg)

    def it_should_close_zip_file_after_use(self, ZipFile_, zip_file_):
        # exercise ---------------------
        PhysPkg.read(MINI_ZIP_PKG_PATH)
        # verify -----------------------
        ZipFile_.assert_called_once_with(MINI_ZIP_PKG_PATH, 'r')
        zip_file_.close.assert_called_with()
