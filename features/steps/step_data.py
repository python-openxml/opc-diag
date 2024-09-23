from __future__ import annotations

import hashlib
import os
from difflib import unified_diff
from typing import Iterable
from zipfile import ZipFile


def Manifest(path: str):
    """Factory function for _Manifest object.

    Return |_Manifest| instance for package at *path*. *path* can point to either a zip package or
    a directory containing an extracted package.
    """
    if os.path.isdir(path):
        return _Manifest.from_dir(path)
    else:
        return _Manifest.from_zip(path)


class _Manifest:
    """A sorted sequence of (SHA1, name) pairs.

    The pairsthat unambiguously characterize the contents of an OPC package, providing a basis for
    asserting equivalence of two packages, whether stored as a zip archive or a package extracted
    into a directory.
    """

    def __init__(self, sha_names: Iterable[tuple[str, str]]):
        """`sha_names` is a list of SHA1, name 2-tuples, each of which describes a package item."""
        self.sha_names = sorted(sha_names, key=lambda t: t[1])

    def __eq__(self, other: object):
        """
        Return true if *other* is a |_Manifest| instance with exactly
        matching sha_names.
        """
        if not isinstance(other, _Manifest):
            return False
        return self.sha_names == other.sha_names

    def __getitem__(self, key: str):
        """Return SHA1 of sha_name tuple with name that matches *key*."""
        for sha, name in self.sha_names:
            if name == key:
                return sha
        raise KeyError("no item with name '%s'" % key)

    def __setitem__(self, key: str, value: str):
        """Set SHA1 of sha_name tuple with name that matches *key* to *value*."""
        for idx, (_, name) in enumerate(self.sha_names):
            if name == key:
                self.sha_names[idx] = (value, name)
                return
        raise KeyError("no item with name '%s'" % key)

    def __str__(self):
        """
        Return the Python data structure representation of the sha, name
        pairs in this manifest.
        """
        tmpl = "    ('%s',\n     '%s'),"
        lines = [tmpl % (sha, name) for sha, name in self.sha_names]
        return "manifest = [\n%s\n]" % "\n".join(lines)

    def diff(self, other: _Manifest, filename_1: str, filename_2: str):
        """diff between the sha_names of this manifest and those of `other`.

        Return value is a `diff` style unified diff listing between the sha_names of this manifest
        and `other`.
        """
        text_1, text_2 = str(self), str(other)
        lines_1 = text_1.split("\n")
        lines_2 = text_2.split("\n")
        diff = unified_diff(lines_1, lines_2, filename_1, filename_2)
        return "\n".join(line for line in diff)

    @staticmethod
    def from_dir(dirpath: str):
        """Return a |_Manifest| instance for the extracted OPC package at *dirpath*."""
        sha_names: list[tuple[str, str]] = []
        for filepath in sorted(_Manifest._filepaths_in_dir(dirpath)):
            with open(filepath, "rb") as f:
                blob = f.read()
            sha = hashlib.sha1(blob).hexdigest()
            name = os.path.relpath(filepath, dirpath).replace("\\", "/")
            sha_names.append((sha, name))
        return _Manifest(sha_names)

    @staticmethod
    def from_zip(zip_file_path: str):
        """Return a |_Manifest| instance for the zip-based OPC package at *zip_file_path*."""
        zipf = ZipFile(zip_file_path)
        sha_names: list[tuple[str, str]] = []
        for name in sorted(zipf.namelist()):
            blob = zipf.read(name)
            sha = hashlib.sha1(blob).hexdigest()
            sha_names.append((sha, name))
        zipf.close()
        return _Manifest(sha_names)

    @staticmethod
    def _filepaths_in_dir(dirpath: str):
        """Return a sorted list of relative paths.

        Contains one for each of the files under `dirpath`, recursively visiting all
        subdirectories.
        """
        return sorted(
            os.path.join(root, filename)
            for root, _, filenames in os.walk(dirpath)
            for filename in filenames
        )
