# -*- coding: utf-8 -*-
#
# test_model.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of opc-diag and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Unit tests for model module"""

from __future__ import unicode_literals

import sys

from lxml import etree

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
    pkg_item_.is_rels_item = True
    return pkg_item_


@pytest.fixture
def pkg_item_2_(request):
    pkg_item_2_ = instance_mock(PkgItem, request)
    pkg_item_2_.is_rels_item = False
    return pkg_item_2_


@pytest.fixture
def pkg_item_3_(request):
    pkg_item_3_ = instance_mock(PkgItem, request)
    pkg_item_3_.is_rels_item = True
    return pkg_item_3_


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

    def it_can_find_one_of_its_items_by_uri_tail(self, pkg_item_):
        # fixture ----------------------
        pkg_items_ = {'head/tail': pkg_item_}
        package = Package(pkg_items_)
        # exercise ---------------------
        pkg_item = package.find_item_by_uri_tail('tail')
        # verify -----------------------
        assert pkg_item == pkg_item_
        with pytest.raises(KeyError):
            package.find_item_by_uri_tail('head')

    def it_can_provide_a_list_of_rels_items_in_the_package(
            self, pkg_item_, pkg_item_2_, pkg_item_3_):
        # fixture ----------------------
        pkg_items = {
            'foo/bar.rels': pkg_item_,    # should be sorted second
            'joe/bob.xml':  pkg_item_2_,  # should be skipped
            'bar/foo.rels': pkg_item_3_,  # should be sorted first
        }
        package = Package(pkg_items)
        # exercise ---------------------
        rels_items = package.rels_items
        # verify -----------------------
        assert rels_items == [pkg_item_3_, pkg_item_]


class DescribePkgItem(object):

    @pytest.mark.parametrize(('uri', 'is_ct', 'is_rels', 'is_xml_part'), [
        ('[Content_Types].xml', True,  False, False),
        ('foo/bar.xml.rels',    False, True,  False),
        ('foo/bar.xml',         False, False, True),
        ('media/foobar.jpg',    False, False, False),
    ])
    def it_knows_what_kind_of_item_it_is(
            self, uri, is_ct, is_rels, is_xml_part):
        pkg_item = PkgItem(None, uri, None)
        assert pkg_item.is_content_types is is_ct
        assert pkg_item.is_rels_item is is_rels
        assert pkg_item.is_xml_part is is_xml_part

    def it_can_produce_an_etree_element_from_its_blob(self):
        blob = '<root><child>foobar</child></root>'
        pkg_item = PkgItem(None, None, blob)
        assert isinstance(pkg_item.element, etree._Element)

    def it_can_calculate_its_effective_path(self):
        pkg_item = PkgItem('root_uri', 'uri', None)
        expected_path = ('root_uri\\uri' if sys.platform.startswith('win')
                         else 'root_uri/uri')
        assert pkg_item.path == expected_path
