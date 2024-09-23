"""Unit tests for `opcdiag.phys_pkg` module."""

# pyright: reportPrivateUsage=false

import os
import shutil
from unittest.mock import call
from zipfile import ZIP_DEFLATED, ZipFile

import pytest

from opcdiag.phys_pkg import BlobCollection, DirPhysPkg, PhysPkg, ZipPhysPkg

from .unitutil import FixtureRequest, Mock, class_mock, instance_mock, relpath

DIRPATH = "DIRPATH"
DELETEME_DIR = relpath("test-files/deleteme")
FOOBAR_DIR = relpath("test-files/deleteme/foobar_dir")
FOOBAR_FILEPATH = relpath("test-files/deleteme/foobar_dir/foobar_file")
MINI_DIR_PKG_PATH = relpath("test-files/mini_pkg")
MINI_ZIP_PKG_PATH = relpath("test-files/mini_pkg.zip")
ROOT_URI = relpath("test-files/mini_pkg")


@pytest.fixture
def blob_(request: FixtureRequest):
    return instance_mock(str, request)


@pytest.fixture
def blob_2_(request: FixtureRequest):
    return instance_mock(str, request)


@pytest.fixture
def PhysPkg_(request: FixtureRequest):
    PhysPkg_ = class_mock("opcdiag.phys_pkg.PhysPkg", request)
    return PhysPkg_


@pytest.fixture
def uri_(request: FixtureRequest):
    return instance_mock(str, request)


@pytest.fixture
def uri_2_(request: FixtureRequest):
    return instance_mock(str, request)


@pytest.fixture
def ZipFile_(request: FixtureRequest, zip_file_: Mock):
    ZipFile_ = class_mock("opcdiag.phys_pkg.ZipFile", request)
    ZipFile_.return_value = zip_file_
    return ZipFile_


@pytest.fixture
def zip_file_(request: FixtureRequest):
    zip_file_ = instance_mock(ZipFile, request)
    return zip_file_


class DescribePhysPkg:
    def it_should_construct_the_appropriate_subclass(self):
        pkg = PhysPkg.read(MINI_ZIP_PKG_PATH)
        assert isinstance(pkg, ZipPhysPkg)
        pkg = PhysPkg.read(MINI_DIR_PKG_PATH)
        assert isinstance(pkg, DirPhysPkg)

    def it_can_iterate_over_pkg_blobs(self):
        # fixture ----------------------
        blobs = BlobCollection((("foo", b"bar"), ("baz", b"zam")))
        phys_pkg = PhysPkg(blobs, "")
        # exercise ---------------------
        actual_blobs = dict(item for item in phys_pkg)
        # verify -----------------------
        assert actual_blobs == blobs

    def it_can_write_a_blob_collection_to_a_zip(self, tmpdir: str):
        # fixture ----------------------
        uri, uri_2 = "foo/bar.xml", "foo/_rels/bar.xml.rels"
        blob, blob_2 = b"blob", b"blob_2"
        blobs_in = BlobCollection(((uri, blob), (uri_2, blob_2)))
        zip_path = str(tmpdir.join("foobar.xml"))
        # exercise ---------------------
        PhysPkg.write_to_zip(blobs_in, zip_path)
        # verify -----------------------
        assert os.path.isfile(zip_path)
        zipf = ZipFile(zip_path, "r")
        blobs_out = {name: zipf.read(name) for name in zipf.namelist()}
        zipf.close()
        assert blobs_out == blobs_in

    def it_should_close_zip_file_after_use(self, ZipFile_: Mock, zip_file_: Mock):
        # exercise ---------------------
        PhysPkg.write_to_zip(BlobCollection(()), "foobar")
        # verify -----------------------
        ZipFile_.assert_called_once_with("foobar", "w", ZIP_DEFLATED)
        zip_file_.close.assert_called_with()

    def it_can_write_a_blob_collection_to_a_directory(
        self, uri_: Mock, uri_2_: Mock, blob_: Mock, blob_2_: Mock, PhysPkg_: Mock
    ):
        # fixture ----------------------
        blobs = BlobCollection(((uri_, blob_), (uri_2_, blob_2_)))
        # exercise ---------------------
        PhysPkg.write_to_dir(blobs, DIRPATH)
        # verify -----------------------
        PhysPkg_._clear_or_make_dir.assert_called_once_with(DIRPATH)
        PhysPkg_._write_blob_to_dir.assert_has_calls(
            (call(DIRPATH, uri_, blob_), call(DIRPATH, uri_2_, blob_2_)), any_order=True
        )

    def it_can_create_a_new_empty_directory(self):
        """Note: tests integration with filesystem"""
        # case: created if does not exist
        # ------------------------------
        if os.path.exists(DELETEME_DIR):  # pragma: no cover
            shutil.rmtree(DELETEME_DIR)
        PhysPkg._clear_or_make_dir(FOOBAR_DIR)
        assert os.path.exists(FOOBAR_DIR)

        # case: re-created if exists
        # ------------------------------
        if os.path.exists(DELETEME_DIR):  # pragma: no cover
            shutil.rmtree(DELETEME_DIR)
        os.makedirs(FOOBAR_DIR)
        with open(FOOBAR_FILEPATH, "w") as f:
            f.write("foobar file")
        PhysPkg._clear_or_make_dir(FOOBAR_DIR)
        assert os.path.exists(FOOBAR_DIR)
        assert not os.path.exists(FOOBAR_FILEPATH)

        # case: raises if dirpath is file
        # ------------------------------
        shutil.rmtree(DELETEME_DIR)
        os.makedirs(DELETEME_DIR)
        with open(FOOBAR_DIR, "w") as f:
            f.write("foobar file at FOOBAR_DIR path")
        with pytest.raises(ValueError, match="target path .* is not a directory"):
            PhysPkg._clear_or_make_dir(FOOBAR_DIR)

    def it_can_write_a_blob_to_a_file_in_a_directory(self, tmpdir: str):
        """Note: tests integration with filesystem"""
        # fixture ----------------------
        uri = "foo/bar.xml"
        blob = b"blob"
        dirpath = str(tmpdir)
        filepath = os.path.join(dirpath, "foo", "bar.xml")
        # exercise ---------------------
        PhysPkg._write_blob_to_dir(str(tmpdir), uri, blob)
        # verify -----------------------
        assert os.path.isfile(filepath)
        with open(filepath, "rb") as f:
            actual_blob = f.read()
        assert actual_blob == blob


class DescribeDirPhysPkg:
    def it_can_construct_from_a_filesystem_package(self):
        """
        Note: integration test, allowing PhysPkg to hit the local filesystem.
        """
        # exercise ---------------------
        dir_phys_pkg = DirPhysPkg.read(MINI_DIR_PKG_PATH)
        # verify -----------------------
        expected_blobs = {"uri_1": b"blob_1\n", "uri_2": b"blob_2\n"}
        assert dir_phys_pkg._blobs == expected_blobs
        assert dir_phys_pkg._root_uri == ROOT_URI
        assert isinstance(dir_phys_pkg, DirPhysPkg)


class DescribeZipPhysPkg:
    def it_can_construct_from_a_filesystem_package(self):
        """
        Note: integration test, allowing PhysPkg to hit ZipFile on the local
        filesystem
        """
        # exercise ---------------------
        zip_phys_pkg = ZipPhysPkg.read(MINI_ZIP_PKG_PATH)
        # verify -----------------------
        expected_blobs = {"uri_1": b"blob_1\n", "uri_2": b"blob_2\n"}
        assert zip_phys_pkg._blobs == expected_blobs
        assert zip_phys_pkg._root_uri == ROOT_URI
        assert isinstance(zip_phys_pkg, ZipPhysPkg)

    def it_should_close_zip_file_after_use(self, ZipFile_: Mock, zip_file_: Mock):
        # exercise ---------------------
        PhysPkg.read(MINI_ZIP_PKG_PATH)
        # verify -----------------------
        ZipFile_.assert_called_once_with(MINI_ZIP_PKG_PATH, "r")
        zip_file_.close.assert_called_with()
