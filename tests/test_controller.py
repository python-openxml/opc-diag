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

from .unitutil import class_mock, instance_mock


PKG_PATH = 'pkg_path'
URI_TAIL = 'uri_tail'


@pytest.fixture
def ItemPresenter_(request, item_presenter_):
    ItemPresenter_ = class_mock('opcdiag.controller.ItemPresenter', request)
    ItemPresenter_.return_value = item_presenter_
    return ItemPresenter_


@pytest.fixture
def item_presenter_(request):
    item_presenter_ = instance_mock(ItemPresenter, request)
    return item_presenter_


@pytest.fixture
def OpcView_(request):
    OpcView_ = class_mock('opcdiag.controller.OpcView', request)
    return OpcView_


@pytest.fixture
def Package_(request, package_):
    Package_ = class_mock('opcdiag.controller.Package', request)
    Package_.read.return_value = package_
    return Package_


@pytest.fixture
def package_(request, pkg_item_):
    package_ = instance_mock(Package, request)
    package_.find_item_by_uri_tail.return_value = pkg_item_
    return package_


@pytest.fixture
def pkg_item_(request):
    pkg_item_ = instance_mock(PkgItem, request)
    return pkg_item_


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
