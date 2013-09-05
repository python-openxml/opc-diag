# -*- coding: utf-8 -*-
#
# phys_pkg.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of opc-diag and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Interface to a physical OPC package, either a zip archive or directory"""

import os

from zipfile import ZipFile


class BlobCollection(dict):
    """
    Structures a set of blobs, like a set of files in an OPC package.
    It can add and retrieve items by URI (relative path, roughly) and can
    also retrieve items by uri_tail, the trailing portion of the URI.
    """


class PhysPkg(object):
    """
    Provides read and write services for packages on the filesystem. Suitable
    for use with OPC packages in either Zip or expanded directory form.
    |PhysPkg| objects are iterable, generating a (uri, blob) 2-tuple for each
    item in the package.
    """
    def __init__(self, blobs, root_uri):
        super(PhysPkg, self).__init__()
        self._blobs = blobs
        self._root_uri = root_uri

    def __iter__(self):
        """
        Generate a (uri, blob) 2-tuple for each of the items in the package.
        """
        return iter(self._blobs.items())

    @staticmethod
    def read(path):
        """
        Return a |PhysPkg| instance loaded with contents of OPC package at
        *path*, where *path* can be either a regular zip package or a
        directory containing an expanded package.
        """
        if os.path.isdir(path):
            return DirPhysPkg.read(path)
        else:
            return ZipPhysPkg.read(path)

    @property
    def root_uri(self):
        return self._root_uri  # pragma: no cover


class DirPhysPkg(PhysPkg):
    """
    An OPC physical package that has been expanded into individual files in
    a directory structure that mirrors the pack URI.
    """
    def __init__(self, blobs, root_uri):
        super(DirPhysPkg, self).__init__(blobs, root_uri)

    @classmethod
    def read(cls, pkg_dir):
        """
        Return a |BlobCollection| instance loaded from *pkg_dir*.
        """
        blobs = BlobCollection()
        pfx_len = len(pkg_dir)+1
        for filepath in cls._filepaths_in_dir(pkg_dir):
            uri = filepath[pfx_len:]
            with open(filepath, 'r') as f:
                blob = f.read()
            blobs[uri] = blob
        root_uri = pkg_dir
        return cls(blobs, root_uri)

    @staticmethod
    def _filepaths_in_dir(dirpath):
        """
        Return a sorted list of relative paths, one for each of the files
        under *dirpath*, recursively visiting all subdirectories.
        """
        filepaths = []
        for root, dirnames, filenames in os.walk(dirpath):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                filepaths.append(filepath)
        return sorted(filepaths)


class ZipPhysPkg(PhysPkg):
    """
    An OPC physical package in the typically encountered form, a zip archive.
    """
    def __init__(self, blobs, root_uri):
        super(ZipPhysPkg, self).__init__(blobs, root_uri)

    @classmethod
    def read(cls, pkg_zip_path):
        """
        Return a |BlobCollection| instance loaded from *pkg_zip_path*.
        """
        blobs = BlobCollection()
        zipf = ZipFile(pkg_zip_path, 'r')
        for name in zipf.namelist():
            blobs[name] = zipf.read(name)
        zipf.close()
        root_uri = os.path.splitext(pkg_zip_path)[0]
        return cls(blobs, root_uri)
