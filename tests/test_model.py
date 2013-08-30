# -*- coding: utf-8 -*-
#
# test_model.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of opc-diag and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Unit tests for model module"""

from opcdiag.model import Package, PkgItem
from opcdiag.phys_pkg import PhysPkg

import pytest

from mock import call

from .unitutil import class_mock, instance_mock


@pytest.fixture
def blob_(request):
    return instance_mock(str, request)


@pytest.fixture
def blob_2_(request):
    return instance_mock(str, request)


@pytest.fixture
def Package_(request):
    Package_ = class_mock('opcdiag.model.Package', request)
    return Package_


@pytest.fixture
def path_(request):
    return instance_mock(str, request)


@pytest.fixture
def PhysPkg_(request, phys_pkg_):
    PhysPkg_ = class_mock('opcdiag.model.PhysPkg', request)
    PhysPkg_.read.return_value = phys_pkg_
    return PhysPkg_


@pytest.fixture
def phys_pkg_(request, root_uri_, uri_, uri_2_, blob_, blob_2_):
    phys_pkg = instance_mock(PhysPkg, request)
    phys_pkg.root_uri = root_uri_
    phys_pkg.__iter__.return_value = iter(((uri_,   blob_),
                                           (uri_2_, blob_2_)))
    return phys_pkg


@pytest.fixture
def PkgItem_(request, pkg_item_, pkg_item_2_):
    PkgItem_ = class_mock('opcdiag.model.PkgItem', request)
    PkgItem_.side_effect = [pkg_item_, pkg_item_2_]
    return PkgItem_


@pytest.fixture
def pkg_item_(request):
    pkg_item_ = instance_mock(PkgItem, request)
    return pkg_item_


@pytest.fixture
def pkg_item_2_(request):
    pkg_item_2_ = instance_mock(PkgItem, request)
    return pkg_item_2_


@pytest.fixture
def root_uri_(request):
    return instance_mock(str, request)


@pytest.fixture
def uri_(request):
    return instance_mock(str, request)


@pytest.fixture
def uri_2_(request):
    return instance_mock(str, request)


class DescribePackage(object):

    def it_can_construct_from_a_filesystem_package(
            self, path_, root_uri_, uri_, uri_2_, blob_, blob_2_, PhysPkg_,
            PkgItem_, pkg_item_, pkg_item_2_, Package_):
        # exercise ---------------------
        pkg = Package.read(path_)
        # expected values --------------
        expected_PkgItem_calls = [
            call(root_uri_, uri_,   blob_),
            call(root_uri_, uri_2_, blob_2_)
        ]
        expected_items = {uri_:   pkg_item_,
                          uri_2_: pkg_item_2_}
        # verify -----------------------
        PhysPkg_.read.assert_called_once_with(path_)
        assert PkgItem_.call_count == 2
        PkgItem_.assert_has_calls(expected_PkgItem_calls, any_order=True)
        Package_.assert_called_once_with(expected_items)
        assert isinstance(pkg, Package)
