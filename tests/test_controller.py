# -*- coding: utf-8 -*-
#
# test_controller.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of opc-diag and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Unit tests for controller module"""

from opcdiag.controller import OpcController
from opcdiag.model import Package, PkgItem
from opcdiag.presenter import ItemPresenter

import pytest

from mock import call

from .unitutil import class_mock, instance_mock


PKG_PATH = 'pkg_path'
PKG_2_PATH = 'pkg_2_path'
URI_CONTENT_TYPES = '[Content_Types].xml'
URI_TAIL = 'uri_tail'


@pytest.fixture
def DiffPresenter_(request, item_diff_, rels_diffs_, xml_part_diffs_):
    DiffPresenter_ = class_mock('opcdiag.controller.DiffPresenter', request)
    DiffPresenter_.named_item_diff.return_value = item_diff_
    DiffPresenter_.rels_diffs.return_value = rels_diffs_
    DiffPresenter_.xml_part_diffs.return_value = xml_part_diffs_
    return DiffPresenter_


@pytest.fixture
def ItemPresenter_(request, item_presenter_):
    ItemPresenter_ = class_mock('opcdiag.controller.ItemPresenter', request)
    ItemPresenter_.return_value = item_presenter_
    return ItemPresenter_


@pytest.fixture
def item_diff_(request):
    item_diff_ = instance_mock(str, request)
    return item_diff_


@pytest.fixture
def item_presenter_(request):
    item_presenter_ = instance_mock(ItemPresenter, request)
    return item_presenter_


@pytest.fixture
def OpcView_(request):
    OpcView_ = class_mock('opcdiag.controller.OpcView', request)
    return OpcView_


@pytest.fixture
def Package_(request, package_, package_2_):
    Package_ = class_mock('opcdiag.controller.Package', request)
    Package_.read.side_effect = (package_, package_2_)
    return Package_


@pytest.fixture
def package_(request, pkg_item_):
    package_ = instance_mock(Package, request)
    package_.find_item_by_uri_tail.return_value = pkg_item_
    return package_


@pytest.fixture
def package_2_(request, pkg_item_2_):
    package_2_ = instance_mock(Package, request)
    package_2_.find_item_by_uri_tail.return_value = pkg_item_2_
    return package_2_


@pytest.fixture
def pkg_item_(request):
    pkg_item_ = instance_mock(PkgItem, request)
    return pkg_item_


@pytest.fixture
def pkg_item_2_(request):
    pkg_item_2_ = instance_mock(PkgItem, request)
    return pkg_item_2_


@pytest.fixture
def rels_diffs_(request):
    rels_diffs_ = instance_mock(list, request)
    return rels_diffs_


@pytest.fixture
def xml_part_diffs_(request):
    xml_part_diffs_ = instance_mock(list, request)
    return xml_part_diffs_


class DescribeOpcController(object):

    def it_can_execute_a_browse_command(
            self, Package_, package_, pkg_item_, ItemPresenter_,
            item_presenter_, OpcView_):
        # exercise ---------------------
        OpcController().browse(PKG_PATH, URI_TAIL)
        # verify -----------------------
        Package_.read.assert_called_once_with(PKG_PATH)
        package_.find_item_by_uri_tail.assert_called_once_with(URI_TAIL)
        ItemPresenter_.assert_called_once_with(pkg_item_)
        OpcView_.pkg_item.assert_called_once_with(item_presenter_)

    def it_can_execute_a_diff_pkg_command(
            self, Package_, DiffPresenter_, package_, package_2_,
            item_diff_, rels_diffs_, xml_part_diffs_, OpcView_):
        # exercise ---------------------
        OpcController().diff_pkg(PKG_PATH, PKG_2_PATH)
        # expected values --------------
        expected_Package_read_calls = [call(PKG_PATH), call(PKG_2_PATH)]
        Package_.read.assert_has_calls(expected_Package_read_calls)
        DiffPresenter_.named_item_diff.assert_called_once_with(
            package_, package_2_, URI_CONTENT_TYPES)
        DiffPresenter_.rels_diffs.assert_called_once_with(
            package_, package_2_)
        DiffPresenter_.xml_part_diffs.assert_called_once_with(
            package_, package_2_)
        OpcView_.package_diff.assert_called_once_with(
            item_diff_, rels_diffs_, xml_part_diffs_)

    def it_can_execute_a_diff_item_command(
            self, Package_, package_, package_2_, DiffPresenter_, item_diff_,
            OpcView_):
        # exercise ---------------------
        OpcController().diff_item(PKG_PATH, PKG_2_PATH, URI_TAIL)
        # expected values --------------
        expected_Package_read_calls = [call(PKG_PATH), call(PKG_2_PATH)]
        # verify -----------------------
        Package_.read.assert_has_calls(expected_Package_read_calls)
        DiffPresenter_.named_item_diff.assert_called_once_with(
            package_, package_2_, URI_TAIL)
        OpcView_.item_diff.assert_called_once_with(item_diff_)
