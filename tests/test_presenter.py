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

from opcdiag.model import Package, PkgItem
from opcdiag.presenter import DiffPresenter, diff, ItemPresenter

import pytest

from mock import call, PropertyMock

from .unitutil import (
    class_mock,
    function_mock,
    instance_mock,
    loose_mock,
    property_mock,
)


URI_TAIL = "uri_tail"


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
def DiffPresenter_(request, pkg_item_diffs_):
    DiffPresenter_ = class_mock("opcdiag.presenter.DiffPresenter", request)
    DiffPresenter_._pkg_item_diff.side_effect = pkg_item_diffs_
    DiffPresenter_._pkg_item_diffs.return_value = pkg_item_diffs_
    return DiffPresenter_


@pytest.fixture
def diff_(request, diff_text_):
    diff_ = function_mock("opcdiag.presenter.diff", request)
    diff_.return_value = diff_text_
    return diff_


@pytest.fixture
def diff_text_(request):
    return loose_mock(request)


@pytest.fixture
def filename_(request):
    return loose_mock(request)


@pytest.fixture
def filename_2_(request):
    return loose_mock(request)


@pytest.fixture
def ItemPresenter_(request, item_presenter_, item_presenter_2_):
    ItemPresenter_ = class_mock("opcdiag.presenter.ItemPresenter", request)
    ItemPresenter_.side_effect = (item_presenter_, item_presenter_2_)
    return ItemPresenter_


@pytest.fixture
def ItemPresenter_xml_(request):
    return property_mock("opcdiag.presenter.ItemPresenter.xml", request)


@pytest.fixture
def item_presenter_(request, filename_, item_presenter_text_):
    item_presenter_ = instance_mock(ItemPresenter, request)
    item_presenter_.filename = filename_
    type(item_presenter_).text = item_presenter_text_
    return item_presenter_


@pytest.fixture
def item_presenter_2_(request, filename_2_, item_presenter_2_text_):
    item_presenter_2_ = instance_mock(ItemPresenter, request)
    item_presenter_2_.filename = filename_2_
    type(item_presenter_2_).text = item_presenter_2_text_
    return item_presenter_2_


@pytest.fixture
def item_presenter_text_(request, text_):
    return PropertyMock(name=request.fixturename, return_value=text_)


@pytest.fixture
def item_presenter_2_text_(request, text_2_):
    return PropertyMock(name=request.fixturename, return_value=text_2_)


@pytest.fixture
def package_(request, pkg_item_, rels_items_, xml_parts_):
    package_ = instance_mock(Package, request)
    package_.find_item_by_uri_tail.return_value = pkg_item_
    package_.rels_items = rels_items_
    package_.xml_parts = xml_parts_
    return package_


@pytest.fixture
def package_2_(request, pkg_item_, pkg_item_2_):
    package_2_ = instance_mock(Package, request)
    package_2_.find_item_by_uri_tail.side_effect = (pkg_item_2_, pkg_item_)
    return package_2_


@pytest.fixture
def pkg_item_(request, uri_):
    pkg_item_ = instance_mock(PkgItem, request)
    pkg_item_.uri = uri_
    return pkg_item_


@pytest.fixture
def pkg_item_2_(request, uri_2_):
    pkg_item_2_ = instance_mock(PkgItem, request)
    pkg_item_2_.uri = uri_2_
    return pkg_item_2_


@pytest.fixture
def pkg_items_(request, pkg_item_, pkg_item_2_):
    return [pkg_item_, pkg_item_2_]


@pytest.fixture
def pkg_item_diff_(request):
    return "diff_"


@pytest.fixture
def pkg_item_diff_2_(request):
    return "diff_2_"


@pytest.fixture
def pkg_item_diffs_(request, pkg_item_diff_, pkg_item_diff_2_):
    return [pkg_item_diff_, pkg_item_diff_2_]


@pytest.fixture
def rels_item_(request):
    rels_item_ = instance_mock(PkgItem, request)
    rels_item_.is_content_types = False
    rels_item_.is_rels_item = True
    rels_item_.is_xml_part = False
    return rels_item_


@pytest.fixture
def rels_items_(request):
    rels_items_ = instance_mock(list, request)
    return rels_items_


@pytest.fixture
def text_(request):
    return "text_"


@pytest.fixture
def text_2_(request):
    return "text_2_"


@pytest.fixture
def uri_(request):
    return "/word/document.xml"


@pytest.fixture
def uri_2_(request):
    return "/_rels/.rels"


@pytest.fixture
def xml_parts_(request):
    xml_parts_ = instance_mock(list, request)
    return xml_parts_


@pytest.fixture
def xml_part_(request):
    xml_part_ = instance_mock(PkgItem, request)
    xml_part_.is_content_types = False
    xml_part_.is_rels_item = False
    xml_part_.is_xml_part = True
    return xml_part_


class DescribeDiff(object):
    def it_calculates_a_diff_between_two_texts(self):
        """Integrates with difflib"""
        # fixture ----------------------
        text = "foobar\nnoobar\nzoobar"
        text_2 = "foobar\ngoobar\nnoobar"
        filename, filename_2 = "filename", "filename_2"
        expected_diff_text = (
            "--- filename\n"
            "\n"
            "+++ filename_2\n"
            "\n"
            "@@ -1,3 +1,3 @@\n"
            "\n"
            " foobar\n"
            "+goobar\n"
            " noobar\n"
            "-zoobar"
        )
        # exercise ---------------------
        diff_text = diff(text, text_2, filename, filename_2)
        print("actual diff text:")
        for line in diff_text.splitlines():
            print("'%s'" % line)
        print("\nexpected diff text:")
        for line in expected_diff_text.splitlines():
            print("'%s'" % line)
        assert diff_text == expected_diff_text


class DescribeDiffPresenter(object):
    def it_can_diff_a_named_item_between_two_packages(
        self, package_, package_2_, DiffPresenter_, pkg_item_, pkg_item_2_
    ):
        # exercise ---------------------
        DiffPresenter.named_item_diff(package_, package_2_, URI_TAIL)
        # verify -----------------------
        package_.find_item_by_uri_tail.assert_called_once_with(URI_TAIL)
        package_2_.find_item_by_uri_tail.assert_called_once_with(URI_TAIL)
        DiffPresenter_._pkg_item_diff.assert_called_once_with(pkg_item_, pkg_item_2_)

    def it_can_diff_two_package_items(
        self,
        pkg_item_,
        pkg_item_2_,
        ItemPresenter_,
        item_presenter_text_,
        item_presenter_2_text_,
        diff_,
        text_,
        text_2_,
        filename_,
        filename_2_,
        diff_text_,
    ):
        # exercise ---------------------
        item_diff = DiffPresenter._pkg_item_diff(pkg_item_, pkg_item_2_)
        # expected values --------------
        expected_ItemPresenter_calls = [call(pkg_item_), call(pkg_item_2_)]
        # verify -----------------------
        ItemPresenter_.assert_has_calls(expected_ItemPresenter_calls)
        item_presenter_text_.assert_called_once_with()
        item_presenter_2_text_.assert_called_once_with()
        diff_.assert_called_once_with(text_, text_2_, filename_, filename_2_)
        assert item_diff is diff_text_

    def it_can_gather_rels_diffs_between_two_packages(
        self, package_, package_2_, DiffPresenter_, rels_items_, pkg_item_diffs_
    ):
        # exercise ---------------------
        rels_diffs = DiffPresenter.rels_diffs(package_, package_2_)
        # verify -----------------------
        DiffPresenter_._pkg_item_diffs.assert_called_once_with(rels_items_, package_2_)
        assert rels_diffs is pkg_item_diffs_

    def it_can_gather_xml_part_diffs_between_two_packages(
        self, package_, package_2_, DiffPresenter_, xml_parts_, pkg_item_diffs_
    ):
        # exercise ---------------------
        xml_part_diffs = DiffPresenter.xml_part_diffs(package_, package_2_)
        # verify -----------------------
        DiffPresenter_._pkg_item_diffs.assert_called_once_with(xml_parts_, package_2_)
        assert xml_part_diffs is pkg_item_diffs_

    def it_can_diff_a_list_of_pkg_items_against_another_package(
        self,
        pkg_items_,
        package_2_,
        uri_,
        uri_2_,
        DiffPresenter_,
        pkg_item_,
        pkg_item_2_,
        pkg_item_diff_,
        pkg_item_diff_2_,
    ):
        # exercise ---------------------
        diffs = DiffPresenter._pkg_item_diffs(pkg_items_, package_2_)
        # verify -----------------------
        assert package_2_.find_item_by_uri_tail.call_args_list == [
            call(uri_),
            call(uri_2_),
        ]
        assert DiffPresenter_._pkg_item_diff.call_args_list == [
            call(pkg_item_, pkg_item_2_),
            call(pkg_item_2_, pkg_item_),
        ]
        assert diffs == [pkg_item_diff_, pkg_item_diff_2_]


class DescribeItemPresenter(object):

    FOOBAR_XML = (
        "<?xml version='1.0' encoding='UTF-8' standalone='yes'?>\n"
        "<foobar>\n"
        '  <foo val="bar"/>\n'
        '  <bar val="foo"/>\n'
        "</foobar>"
    )

    @pytest.fixture
    def foobar_elm_(self):
        foobar_xml_bytes = self.FOOBAR_XML.encode("utf-8")
        return etree.fromstring(foobar_xml_bytes)

    def it_constructs_subclass_based_on_item_type(
        self, content_types_item_, rels_item_, xml_part_, binary_part_
    ):
        cases = (
            (content_types_item_, "ContentTypesPresenter"),
            (rels_item_, "RelsItemPresenter"),
            (xml_part_, "XmlPartPresenter"),
            (binary_part_, "ItemPresenter"),
        )
        for pkg_item, expected_type_name in cases:
            item_presenter = ItemPresenter(pkg_item)
            assert type(item_presenter).__name__ == expected_type_name

    def it_provides_a_normalized_path_string_for_the_pkg_item(self, pkg_item_):
        pkg_item_.path = "foo\\bar"
        item_presenter = ItemPresenter(pkg_item_)
        assert item_presenter.filename == "foo/bar"

    def it_should_raise_if_text_property_not_implemented_on_subclass(
        self, binary_part_
    ):
        item_presenter = object.__new__(ItemPresenter)
        with pytest.raises(NotImplementedError):
            item_presenter.text

    def it_can_pretty_format_the_xml_of_its_item(
        self, content_types_item_, foobar_elm_
    ):
        """Note: tests integration with lxml.etree"""
        content_types_item_.element = foobar_elm_
        item_presenter = ItemPresenter(content_types_item_)
        assert item_presenter.xml == self.FOOBAR_XML


class DescribeContentTypesPresenter(object):
    def it_can_format_cti_xml(self, ItemPresenter_xml_, content_types_item_):
        # fixture ----------------------
        ItemPresenter_xml_.return_value = (
            "<?xml version='1.0' encoding='UTF-8' standalone='yes'?>\n"
            "<Types>\n"
            '  <Default Extension="foo" ContentType="bar"/>\n'
            '  <Override PartName="foobar" ContentType="barfoo"/>\n'
            '  <Default Extension="bar" ContentType="foo"/>\n'
            '  <Override PartName="barfoo" ContentType="foobar"/>\n'
            "</Types>"
        )
        content_types_presenter = ItemPresenter(content_types_item_)
        # verify -----------------------
        expected_text = (
            "<?xml version='1.0' encoding='UTF-8' standalone='yes'?>\n"
            "<Types>\n"
            '  <Default Extension="bar" ContentType="foo"/>\n'
            '  <Default Extension="foo" ContentType="bar"/>\n'
            '  <Override PartName="barfoo" ContentType="foobar"/>\n'
            '  <Override PartName="foobar" ContentType="barfoo"/>\n'
            "</Types>"
        )
        assert content_types_presenter.text == expected_text


class DescribeRelsItemPresenter(object):
    def it_can_format_rels_xml(self, ItemPresenter_xml_, rels_item_):
        # fixture ----------------------
        ItemPresenter_xml_.return_value = (
            "<?xml version='1.0' encoding='UTF-8' standalone='yes'?>\n"
            "<Relationships>\n"
            '  <Relationship Id="rId1" Type="xyz" Target="foo"/>\n'
            '  <Relationship Id="rId2" Type="abc" Target="bar"/>\n'
            '  <Relationship Id="rId3" Type="mno" Target="baz"/>\n'
            "</Relationships>"
        )
        rels_presenter = ItemPresenter(rels_item_)
        # verify -----------------------
        expected_text = (
            "<?xml version='1.0' encoding='UTF-8' standalone='yes'?>\n"
            "<Relationships>\n"
            '  <Relationship Id="x" Type="abc" Target="bar"/>\n'
            '  <Relationship Id="x" Type="mno" Target="baz"/>\n'
            '  <Relationship Id="x" Type="xyz" Target="foo"/>\n'
            "</Relationships>"
        )
        assert rels_presenter.text == expected_text


class DescribeXmlPartPresenter(object):
    def it_can_format_part_xml(self, ItemPresenter_xml_, xml_part_):
        # fixture ----------------------
        cases = (
            # root w/no attrs is unchanged -----------------
            (("<?xml?>\n" "<foobar/>"), ("<?xml?>\n" "<foobar/>")),
            # sort order: def_ns, nsdecls, attrs -----------
            (
                (
                    "<?xml?>\n"
                    '<foobar foo="bar" xmlns:f="foo" xmlns:b="bar" xmlns="zoo" boo'
                    '="far"/>'
                ),
                (
                    "<?xml?>\n"
                    "<foobar\n"
                    '    xmlns="zoo"\n'
                    '    xmlns:b="bar"\n'
                    '    xmlns:f="foo"\n'
                    '    boo="far"\n'
                    '    foo="bar"\n'
                    "    />"
                ),
            ),
        )
        # verify -----------------------
        for part_xml, expected_xml in cases:
            ItemPresenter_xml_.return_value = part_xml
            part_presenter = ItemPresenter(xml_part_)
            assert part_presenter.text == expected_xml
