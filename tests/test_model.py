"""Unit tests for `opcdiag.model` module."""

# pyright: reportPrivateUsage=false

from __future__ import unicode_literals

import sys
from unittest.mock import call

import pytest
from lxml import etree

from opcdiag.model import Package, PkgItem
from opcdiag.phys_pkg import PhysPkg

from .unitutil import FixtureRequest, Mock, class_mock, instance_mock

DIRPATH = "dirpath"
PACKAGE_PATH = "package_path"


class DescribePackage:
    def it_can_construct_from_a_filesystem_package(
        self,
        path_: Mock,
        root_uri_: Mock,
        uri_: Mock,
        uri_2_: Mock,
        blob_: Mock,
        blob_2_: Mock,
        PhysPkg_: Mock,
        PkgItem_: Mock,
        pkg_item_: Mock,
        pkg_item_2_: Mock,
        Package_: Mock,
    ):
        # exercise ---------------------
        pkg = Package.read(path_)
        # expected values --------------
        expected_PkgItem_calls = [
            call(root_uri_, uri_, blob_),
            call(root_uri_, uri_2_, blob_2_),
        ]
        expected_items = {uri_: pkg_item_, uri_2_: pkg_item_2_}
        # verify -----------------------
        PhysPkg_.read.assert_called_once_with(path_)
        assert PkgItem_.call_count == 2
        PkgItem_.assert_has_calls(expected_PkgItem_calls, any_order=True)
        Package_.assert_called_once_with(expected_items)
        assert isinstance(pkg, Package)

    def it_can_find_one_of_its_items_by_uri_tail(self, pkg_item_: Mock):
        # fixture ----------------------
        pkg_items_ = {"head/tail": pkg_item_}
        package = Package(pkg_items_)
        # exercise ---------------------
        pkg_item = package.find_item_by_uri_tail("tail")
        # verify -----------------------
        assert pkg_item == pkg_item_
        with pytest.raises(KeyError):
            package.find_item_by_uri_tail("head")

    def it_can_pretty_format_its_xml_pkg_items(self, pkg_item_: Mock, pkg_item_2_: Mock):
        pkg_items = {"1": pkg_item_, "2": pkg_item_2_}
        package = Package(pkg_items)
        package.prettify_xml()
        pkg_item_.prettify_xml.assert_called_once_with()
        pkg_item_2_.prettify_xml.assert_called_once_with()

    def it_can_provide_a_list_of_rels_items_in_the_package(
        self, pkg_item_: Mock, pkg_item_2_: Mock, pkg_item_3_: Mock
    ):
        # fixture ----------------------
        pkg_items = {
            "foo/bar.rels": pkg_item_,  # should be sorted second
            "joe/bob.xml": pkg_item_2_,  # should be skipped
            "bar/foo.rels": pkg_item_3_,  # should be sorted first
        }
        package = Package(pkg_items)
        # exercise ---------------------
        rels_items = package.rels_items
        # verify -----------------------
        assert rels_items == [pkg_item_3_, pkg_item_]

    def it_can_provide_a_list_of_xml_parts_in_the_package(
        self, pkg_item_: Mock, pkg_item_2_: Mock, pkg_item_3_: Mock
    ):
        # fixture ----------------------
        pkg_items = {
            "foobar": pkg_item_,  # should be sorted second
            "joebob": pkg_item_2_,  # should be skipped
            "barfoo": pkg_item_3_,  # should be sorted first
        }
        package = Package(pkg_items)
        # exercise ---------------------
        xml_parts = package.xml_parts
        # verify -----------------------
        assert xml_parts == [pkg_item_3_, pkg_item_]

    def it_can_save_itself_to_a_zip(
        self, pkg_item_dict_: Mock, PhysPkg_: Mock, blob_collection_: Mock
    ):
        # fixture ----------------------
        package = Package(pkg_item_dict_)
        # exercise ---------------------
        package.save(PACKAGE_PATH)
        # verify -----------------------
        PhysPkg_.write_to_zip.assert_called_once_with(blob_collection_, PACKAGE_PATH)

    def it_can_save_an_expanded_version_of_itself_to_a_directory(
        self, pkg_item_dict_: Mock, PhysPkg_: Mock, blob_collection_: Mock
    ):
        # fixture ----------------------
        package = Package(pkg_item_dict_)
        # exercise ---------------------
        package.save_to_dir(DIRPATH)
        # verify -----------------------
        PhysPkg_.write_to_dir.assert_called_once_with(blob_collection_, DIRPATH)

    def it_can_change_one_of_its_items_to_another(self, pkg_item_: Mock, pkg_item_2_: Mock):
        # fixture ----------------------
        pkg_items = {"uri": pkg_item_}
        package = Package(pkg_items)
        pkg_item_2_.uri = "uri"
        pkg_item_2_.blob = "new blob"
        # exercise ---------------------
        package.substitute_item(pkg_item_2_)
        # verify -----------------------
        assert pkg_item_.blob == "new blob"

    # fixtures -------------------------------------------------------------

    @pytest.fixture
    def blob_(self, request: FixtureRequest):
        return instance_mock(str, request)

    @pytest.fixture
    def blob_2_(self, request: FixtureRequest):
        return instance_mock(str, request)

    @pytest.fixture
    def blob_collection_(
        self, request: FixtureRequest, uri_: Mock, uri_2_: Mock, blob_: Mock, blob_2_: Mock
    ):
        return {uri_: blob_, uri_2_: blob_2_}

    @pytest.fixture
    def Package_(self, request: FixtureRequest):
        Package_ = class_mock("opcdiag.model.Package", request)
        return Package_

    @pytest.fixture
    def path_(self, request: FixtureRequest):
        return instance_mock(str, request)

    @pytest.fixture
    def PhysPkg_(self, request: FixtureRequest, phys_pkg_: Mock):
        PhysPkg_ = class_mock("opcdiag.model.PhysPkg", request)
        PhysPkg_.read.return_value = phys_pkg_
        return PhysPkg_

    @pytest.fixture
    def phys_pkg_(
        self,
        request: FixtureRequest,
        root_uri_: Mock,
        uri_: Mock,
        uri_2_: Mock,
        blob_: Mock,
        blob_2_: Mock,
    ):
        phys_pkg = instance_mock(PhysPkg, request)
        phys_pkg.root_uri = root_uri_
        phys_pkg.__iter__.return_value = iter(((uri_, blob_), (uri_2_, blob_2_)))
        return phys_pkg

    @pytest.fixture
    def PkgItem_(self, request: FixtureRequest, pkg_item_: Mock, pkg_item_2_: Mock):
        PkgItem_ = class_mock("opcdiag.model.PkgItem", request)
        PkgItem_.side_effect = [pkg_item_, pkg_item_2_]
        return PkgItem_

    @pytest.fixture
    def pkg_item_(self, request: FixtureRequest, blob_: Mock):
        pkg_item_ = instance_mock(PkgItem, request)
        pkg_item_.blob = blob_
        pkg_item_.is_rels_item = True
        pkg_item_.is_xml_part = True
        return pkg_item_

    @pytest.fixture
    def pkg_item_2_(self, request: FixtureRequest, blob_2_: Mock):
        pkg_item_2_ = instance_mock(PkgItem, request)
        pkg_item_2_.blob = blob_2_
        pkg_item_2_.is_rels_item = False
        pkg_item_2_.is_xml_part = False
        return pkg_item_2_

    @pytest.fixture
    def pkg_item_3_(self, request: FixtureRequest):
        pkg_item_3_ = instance_mock(PkgItem, request)
        pkg_item_3_.is_rels_item = True
        pkg_item_3_.is_xml_part = True
        return pkg_item_3_

    @pytest.fixture
    def pkg_item_dict_(self, uri_: Mock, uri_2_: Mock, pkg_item_: Mock, pkg_item_2_: Mock):
        return {uri_: pkg_item_, uri_2_: pkg_item_2_}

    @pytest.fixture
    def root_uri_(self, request: FixtureRequest):
        return instance_mock(str, request)

    @pytest.fixture
    def uri_(self, request: FixtureRequest):
        return instance_mock(str, request)

    @pytest.fixture
    def uri_2_(self, request: FixtureRequest):
        return instance_mock(str, request)


class DescribePkgItem:
    @pytest.mark.parametrize(
        ("uri", "is_ct", "is_rels", "is_xml_part"),
        [
            ("[Content_Types].xml", True, False, False),
            ("foo/bar.xml.rels", False, True, False),
            ("foo/bar.xml", False, False, True),
            ("media/foobar.jpg", False, False, False),
        ],
    )
    def it_knows_what_kind_of_item_it_is(
        self, uri: str, is_ct: bool, is_rels: bool, is_xml_part: bool
    ):
        pkg_item = PkgItem("", uri, b"")
        assert pkg_item.is_content_types is is_ct
        assert pkg_item.is_rels_item is is_rels
        assert pkg_item.is_xml_part is is_xml_part

    def it_can_produce_an_etree_element_from_its_blob(self):
        blob = b"<root><child>foobar</child></root>"
        pkg_item = PkgItem("", "", blob)
        assert isinstance(pkg_item.element, etree._Element)

    def it_can_calculate_its_effective_path(self):
        pkg_item = PkgItem("root_uri", "uri", b"")
        expected_path = "root_uri\\uri" if sys.platform.startswith("win") else "root_uri/uri"
        assert pkg_item.path == expected_path

    def it_can_prettify_its_xml(self):
        blob = b"<foo><bar/></foo>"
        pkg_item = PkgItem("", "foo.xml", blob)
        pkg_item.prettify_xml()
        assert pkg_item.blob == (
            b"<?xml version='1.0' encoding='UTF-8' standalone='yes'?>\n"
            b"<foo>\n"
            b"  <bar/>\n"
            b"</foo>\n"
        )
