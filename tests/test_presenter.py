# -*- coding: utf-8 -*-
#
# test_presenter.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of opc-diag and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Unit tests for presenter module"""

from __future__ import unicode_literals

from opcdiag.model import PkgItem
from opcdiag.presenter import ItemPresenter

import pytest

from .unitutil import instance_mock, property_mock


@pytest.fixture
def binary_part_(request):
    binary_part_ = instance_mock(PkgItem, request)
    binary_part_.is_content_types = False
    binary_part_.is_rels_item = False
    binary_part_.is_xml_part = False
    return binary_part_


@pytest.fixture
def content_types_item_(request):
    content_types_item_ = instance_mock(PkgItem, request)
    content_types_item_.is_content_types = True
    content_types_item_.is_rels_item = False
    content_types_item_.is_xml_part = False
    return content_types_item_


@pytest.fixture
def ItemPresenter_xml_(request):
    return property_mock('opcdiag.presenter.ItemPresenter.xml', request)


@pytest.fixture
def rels_item_(request):
    rels_item_ = instance_mock(PkgItem, request)
    rels_item_.is_content_types = False
    rels_item_.is_rels_item = True
    rels_item_.is_xml_part = False
    return rels_item_


@pytest.fixture
def xml_part_(request):
    xml_part_ = instance_mock(PkgItem, request)
    xml_part_.is_content_types = False
    xml_part_.is_rels_item = False
    xml_part_.is_xml_part = True
    return xml_part_


class DescribeItemPresenter(object):

    def it_constructs_subclass_based_on_item_type(
            self, content_types_item_, rels_item_, xml_part_, binary_part_):
        cases = (
            (content_types_item_, 'ContentTypesPresenter'),
            (rels_item_,          'RelsItemPresenter'),
            (xml_part_,           'XmlPartPresenter'),
            (binary_part_,        'ItemPresenter'),
        )
        for pkg_item, expected_type_name in cases:
            item_presenter = ItemPresenter(pkg_item)
            assert type(item_presenter).__name__ == expected_type_name

    def it_should_raise_if_text_property_not_implemented_on_subclass(
            self, binary_part_):
        item_presenter = object.__new__(ItemPresenter)
        with pytest.raises(NotImplementedError):
            item_presenter.text


class DescribeContentTypesPresenter(object):

    def it_can_format_cti_xml(self, ItemPresenter_xml_, content_types_item_):
        # fixture ----------------------
        ItemPresenter_xml_.return_value = (
            '<?xml version=\'1.0\' encoding=\'UTF-8\' standalone=\'yes\'?>\n'
            '<Types>\n'
            '  <Default Extension="foo" ContentType="bar"/>\n'
            '  <Override PartName="foobar" ContentType="barfoo"/>\n'
            '  <Default Extension="bar" ContentType="foo"/>\n'
            '  <Override PartName="barfoo" ContentType="foobar"/>\n'
            '</Types>'
        )
        content_types_presenter = ItemPresenter(content_types_item_)
        # verify -----------------------
        expected_text = (
            '<?xml version=\'1.0\' encoding=\'UTF-8\' standalone=\'yes\'?>\n'
            '<Types>\n'
            '  <Default Extension="bar" ContentType="foo"/>\n'
            '  <Default Extension="foo" ContentType="bar"/>\n'
            '  <Override PartName="barfoo" ContentType="foobar"/>\n'
            '  <Override PartName="foobar" ContentType="barfoo"/>\n'
            '</Types>'
        )
        assert content_types_presenter.text == expected_text
