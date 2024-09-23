"""Interface to a physical OPC package, either a zip archive or directory."""

from __future__ import annotations

import os
import shutil
from typing import Iterator
from zipfile import ZIP_DEFLATED, ZipFile


class BlobCollection(dict[str, bytes]):
    """Structures a set of blobs, like a set of files in an OPC package.

    It can add and retrieve items by URI (relative path, roughly) and can also retrieve items by
    uri_tail, the trailing portion of the URI.
    """


class PhysPkg:
    """Provides read and write services for packages on the filesystem.

    Suitable for use with OPC packages in either Zip or expanded directory form. |PhysPkg| objects
    are iterable, generating a (uri, blob) 2-tuple for each item in the package.
    """

    def __init__(self, blobs: dict[str, bytes], root_uri: str):
        super(PhysPkg, self).__init__()
        self._blobs = blobs
        self._root_uri = root_uri

    def __iter__(self) -> Iterator[tuple[str, bytes]]:
        """Generate a (uri, blob) 2-tuple for each of the items in the package."""
        return iter(self._blobs.items())

    @classmethod
    def read(cls, path: str, /):
        """Return a |PhysPkg| instance loaded with contents of OPC package at *path*.

        *path* can be either a regular zip package or a directory containing an expanded package.
        """
        if os.path.isdir(path):
            return DirPhysPkg.read(path)
        else:
            return ZipPhysPkg.read(path)

    @property
    def root_uri(self) -> str:
        return self._root_uri  # pragma: no cover

    @staticmethod
    def write_to_dir(blobs: BlobCollection, dirpath: str):
        """Write the contents of the |BlobCollection| instance *blobs* to a directory at *dirpath*.

        If a directory already exists at *dirpath*, it is deleted before being recreated. If a
        file exists at *dirpath*, |ValueError| is raised, to prevent unintentional overwriting.
        """
        PhysPkg._clear_or_make_dir(dirpath)
        for uri, blob in blobs.items():
            PhysPkg._write_blob_to_dir(dirpath, uri, blob)

    @staticmethod
    def write_to_zip(blobs: BlobCollection, pkg_zip_path: str):
        """Write "files" in |BlobCollection| instance *blobs* to zip archive at *pkg_zip_path*."""
        zipf = ZipFile(pkg_zip_path, "w", ZIP_DEFLATED)
        for uri in sorted(blobs.keys()):
            blob = blobs[uri]
            zipf.writestr(uri, blob)
        zipf.close()

    @staticmethod
    def _clear_or_make_dir(dirpath: str):
        """Create a new, empty directory at *dirpath*.

        Removes and recreates any directory found there. Raises |ValueError| if *dirpath* exists
        but is not a directory.
        """
        # -- raise if *dirpath* is a file --
        if os.path.exists(dirpath) and not os.path.isdir(dirpath):
            tmpl = "target path '%s' is not a directory"
            raise ValueError(tmpl % dirpath)
        # -- remove any existing directory tree at *dirpath* --
        if os.path.exists(dirpath):
            shutil.rmtree(dirpath)
        # -- create dir at dirpath, as well as any intermediate-level dirs --
        os.makedirs(dirpath)

    @staticmethod
    def _write_blob_to_dir(dirpath: str, uri: str, blob: bytes):
        """Write *blob* to a file under *dirpath*.

        The segments of *uri* that precede the filename are created, as required, as intermediate
        directories.
        """
        # -- In general, uri will contain forward slashes as segment separators.
        # -- This next line converts them to backslashes on Windows.
        item_relpath = os.path.normpath(uri)
        fullpath = os.path.join(dirpath, item_relpath)
        dirpath, _ = os.path.split(fullpath)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        with open(fullpath, "wb") as f:
            f.write(blob)


class DirPhysPkg(PhysPkg):
    """An OPC physical package that has been expanded into individual files in a directory.

    The directory structure mirrors the pack URIs.
    """

    def __init__(self, blobs: dict[str, bytes], root_uri: str):
        super(DirPhysPkg, self).__init__(blobs, root_uri)

    @classmethod
    def read(cls, pkg_dir: str):
        """Return a |BlobCollection| instance loaded from *pkg_dir*."""
        blobs = BlobCollection()
        pfx_len = len(pkg_dir) + 1
        for filepath in cls._filepaths_in_dir(pkg_dir):
            uri = filepath[pfx_len:].replace("\\", "/")
            with open(filepath, "rb") as f:
                blob = f.read()
            blobs[uri] = blob
        root_uri = pkg_dir
        return cls(blobs, root_uri)

    @staticmethod
    def _filepaths_in_dir(dirpath: str) -> list[str]:
        """A sorted list of relative paths, one for each of the files under *dirpath*.

        Recursively visits all subdirectories.
        """
        file_paths = [
            os.path.join(root, filename)
            for root, _, filenames in os.walk(dirpath)
            for filename in filenames
        ]
        return sorted(file_paths)


class ZipPhysPkg(PhysPkg):
    """An OPC physical package in the typically encountered form, a zip archive."""

    def __init__(self, blobs: dict[str, bytes], root_uri: str):
        super(ZipPhysPkg, self).__init__(blobs, root_uri)

    @classmethod
    def read(cls, pkg_zip_path: str):
        """Return a |BlobCollection| instance loaded from *pkg_zip_path*."""
        blobs = BlobCollection()
        zipf = ZipFile(pkg_zip_path, "r")
        for name in zipf.namelist():
            blobs[name] = zipf.read(name)
        zipf.close()
        root_uri = os.path.splitext(pkg_zip_path)[0]
        return cls(blobs, root_uri)
