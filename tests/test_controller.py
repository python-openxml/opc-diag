"""Unit tests for `opcdiag.controller` module."""

from unittest.mock import call

import pytest

from opcdiag.controller import OpcController
from opcdiag.model import Package, PkgItem
from opcdiag.presenter import ItemPresenter

from .unitutil import FixtureRequest, Mock, class_mock, instance_mock

DIRPATH = "dirpath"
NEW_PKG_PATH = "new_pkg_path"
PKG_PATH = "pkg_path"
PKG_2_PATH = "pkg_2_path"
PKG_3_PATH = "pkg_3_path"
URI_CONTENT_TYPES = "[Content_Types].xml"
URI_TAIL = "uri_tail"


class DescribeOpcController:
    def it_can_execute_a_browse_command(
        self,
        Package_: Mock,
        package_: Mock,
        pkg_item_: Mock,
        ItemPresenter_: Mock,
        item_presenter_: Mock,
        OpcView_: Mock,
    ):
        # exercise ---------------------
        OpcController().browse(PKG_PATH, URI_TAIL)
        # verify -----------------------
        Package_.read.assert_called_once_with(PKG_PATH)
        package_.find_item_by_uri_tail.assert_called_once_with(URI_TAIL)
        ItemPresenter_.assert_called_once_with(pkg_item_)
        OpcView_.pkg_item.assert_called_once_with(item_presenter_)

    def it_can_execute_a_diff_pkg_command(
        self,
        Package_: Mock,
        DiffPresenter_: Mock,
        package_: Mock,
        package_2_: Mock,
        item_diff_: Mock,
        rels_diffs_: Mock,
        xml_part_diffs_: Mock,
        OpcView_: Mock,
    ):
        # exercise ---------------------
        OpcController().diff_pkg(PKG_PATH, PKG_2_PATH)
        # expected values --------------
        expected_Package_read_calls = [call(PKG_PATH), call(PKG_2_PATH)]
        Package_.read.assert_has_calls(expected_Package_read_calls)
        DiffPresenter_.named_item_diff.assert_called_once_with(
            package_, package_2_, URI_CONTENT_TYPES
        )
        DiffPresenter_.rels_diffs.assert_called_once_with(package_, package_2_)
        DiffPresenter_.xml_part_diffs.assert_called_once_with(package_, package_2_)
        OpcView_.package_diff.assert_called_once_with(item_diff_, rels_diffs_, xml_part_diffs_)

    def it_can_execute_a_diff_item_command(
        self,
        Package_: Mock,
        package_: Mock,
        package_2_: Mock,
        DiffPresenter_: Mock,
        item_diff_: Mock,
        OpcView_: Mock,
    ):
        # exercise ---------------------
        OpcController().diff_item(PKG_PATH, PKG_2_PATH, URI_TAIL)
        # expected values --------------
        expected_Package_read_calls = [call(PKG_PATH), call(PKG_2_PATH)]
        # verify -----------------------
        Package_.read.assert_has_calls(expected_Package_read_calls)
        DiffPresenter_.named_item_diff.assert_called_once_with(package_, package_2_, URI_TAIL)
        OpcView_.item_diff.assert_called_once_with(item_diff_)

    def it_can_execute_an_extract_package_command(self, Package_: Mock, package_: Mock):
        # exercise ---------------------
        OpcController().extract_package(PKG_PATH, DIRPATH)
        # verify -----------------------
        Package_.read.assert_called_once_with(PKG_PATH)
        package_.prettify_xml.assert_called_once_with()
        package_.save_to_dir.assert_called_once_with(DIRPATH)

    def it_can_execute_a_repackage_command(self, Package_: Mock, package_: Mock):
        # exercise ---------------------
        OpcController().repackage(PKG_PATH, NEW_PKG_PATH)
        # verify -----------------------
        Package_.read.assert_called_once_with(PKG_PATH)
        package_.save.assert_called_once_with(NEW_PKG_PATH)

    def it_can_execute_a_substitute_command(
        self, Package_: Mock, package_: Mock, package_2_: Mock, pkg_item_: Mock, OpcView_: Mock
    ):
        # exercise ---------------------
        OpcController().substitute(URI_TAIL, PKG_PATH, PKG_2_PATH, PKG_3_PATH)
        # expected values --------------
        expected_Package_read_calls = [call(PKG_PATH), call(PKG_2_PATH)]
        Package_.read.assert_has_calls(expected_Package_read_calls)
        package_.find_item_by_uri_tail.assert_called_once_with(URI_TAIL)
        package_2_.substitute_item.assert_called_once_with(pkg_item_)
        package_2_.save.assert_called_once_with(PKG_3_PATH)
        OpcView_.substitute.assert_called_once_with(pkg_item_.uri, PKG_PATH, PKG_2_PATH, PKG_3_PATH)

    # fixtures -------------------------------------------------------------

    @pytest.fixture
    def DiffPresenter_(
        self, request: FixtureRequest, item_diff_: Mock, rels_diffs_: Mock, xml_part_diffs_: Mock
    ):
        DiffPresenter_ = class_mock("opcdiag.controller.DiffPresenter", request)
        DiffPresenter_.named_item_diff.return_value = item_diff_
        DiffPresenter_.rels_diffs.return_value = rels_diffs_
        DiffPresenter_.xml_part_diffs.return_value = xml_part_diffs_
        return DiffPresenter_

    @pytest.fixture
    def ItemPresenter_(self, request: FixtureRequest, item_presenter_: Mock):
        ItemPresenter_ = class_mock("opcdiag.controller.ItemPresenter", request)
        ItemPresenter_.return_value = item_presenter_
        return ItemPresenter_

    @pytest.fixture
    def item_diff_(self, request: FixtureRequest):
        item_diff_ = instance_mock(str, request)
        return item_diff_

    @pytest.fixture
    def item_presenter_(self, request: FixtureRequest):
        item_presenter_ = instance_mock(ItemPresenter, request)
        return item_presenter_

    @pytest.fixture
    def OpcView_(self, request: FixtureRequest):
        OpcView_ = class_mock("opcdiag.controller.OpcView", request)
        return OpcView_

    @pytest.fixture
    def Package_(self, request: FixtureRequest, package_: Mock, package_2_: Mock):
        Package_ = class_mock("opcdiag.controller.Package", request)
        Package_.read.side_effect = (package_, package_2_)
        return Package_

    @pytest.fixture
    def package_(self, request: FixtureRequest, pkg_item_: Mock):
        package_ = instance_mock(Package, request)
        package_.find_item_by_uri_tail.return_value = pkg_item_
        return package_

    @pytest.fixture
    def package_2_(self, request: FixtureRequest, pkg_item_2_: Mock):
        package_2_ = instance_mock(Package, request)
        package_2_.find_item_by_uri_tail.return_value = pkg_item_2_
        return package_2_

    @pytest.fixture
    def pkg_item_(self, request: FixtureRequest):
        pkg_item_ = instance_mock(PkgItem, request)
        return pkg_item_

    @pytest.fixture
    def pkg_item_2_(self, request: FixtureRequest):
        pkg_item_2_ = instance_mock(PkgItem, request)
        return pkg_item_2_

    @pytest.fixture
    def rels_diffs_(self, request: FixtureRequest):
        rels_diffs_ = instance_mock(list, request)
        return rels_diffs_

    @pytest.fixture
    def xml_part_diffs_(self, request: FixtureRequest):
        xml_part_diffs_ = instance_mock(list, request)
        return xml_part_diffs_
