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

from lxml import etree

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

    FOOBAR_XML = (
        '<?xml version=\'1.0\' encoding=\'UTF-8\' standalone=\'yes\'?>\n'
        '<foobar>\n'
        '  <foo val="bar"/>\n'
        '  <bar val="foo"/>\n'
        '</foobar>'
    )

    @pytest.fixture
    def foobar_elm_(self):
        foobar_xml_bytes = self.FOOBAR_XML.encode('utf-8')
        return etree.fromstring(foobar_xml_bytes)

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

    def it_can_pretty_format_the_xml_of_its_item(
            self, content_types_item_, foobar_elm_):
        """Note: tests integration with lxml.etree"""
        content_types_item_.element = foobar_elm_
        item_presenter = ItemPresenter(content_types_item_)
        assert item_presenter.xml == self.FOOBAR_XML


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


class DescribeRelsItemPresenter(object):

    def it_can_format_rels_xml(self, ItemPresenter_xml_, rels_item_):
        # fixture ----------------------
        ItemPresenter_xml_.return_value = (
            '<?xml version=\'1.0\' encoding=\'UTF-8\' standalone=\'yes\'?>\n'
            '<Relationships>\n'
            '  <Relationship Id="rId1" Type="xyz" Target="foo"/>\n'
            '  <Relationship Id="rId2" Type="abc" Target="bar"/>\n'
            '  <Relationship Id="rId3" Type="mno" Target="baz"/>\n'
            '</Relationships>'
        )
        rels_presenter = ItemPresenter(rels_item_)
        # verify -----------------------
        expected_text = (
            '<?xml version=\'1.0\' encoding=\'UTF-8\' standalone=\'yes\'?>\n'
            '<Relationships>\n'
            '  <Relationship Id="x" Type="abc" Target="bar"/>\n'
            '  <Relationship Id="x" Type="mno" Target="baz"/>\n'
            '  <Relationship Id="x" Type="xyz" Target="foo"/>\n'
            '</Relationships>'
        )
        assert rels_presenter.text == expected_text


class DescribeXmlPartPresenter(object):

    def it_can_format_part_xml(self, ItemPresenter_xml_, xml_part_):
        # fixture ----------------------
        cases = (
            # root w/no attrs is unchanged -----------------
            (('<?xml?>\n'
              '<foobar/>'),
             ('<?xml?>\n'
              '<foobar/>')),
            # sort order: def_ns, nsdecls, attrs -----------
            (('<?xml?>\n'
              '<foobar foo="bar" xmlns:f="foo" xmlns:b="bar" xmlns="zoo" boo'
              '="far"/>'),
             ('<?xml?>\n'
              '<foobar\n'
              '    xmlns="zoo"\n'
              '    xmlns:b="bar"\n'
              '    xmlns:f="foo"\n'
              '    boo="far"\n'
              '    foo="bar"\n'
              '    />')),
        )
        # verify -----------------------
        for part_xml, expected_xml in cases:
            ItemPresenter_xml_.return_value = part_xml
            part_presenter = ItemPresenter(xml_part_)
            assert part_presenter.text == expected_xml
