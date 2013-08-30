# -*- coding: utf-8 -*-
#
# model.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of opc-diag and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Package and package items model"""

from opcdiag.phys_pkg import PhysPkg


class Package(object):
    """
    Root of package graph and main model API class.
    """
    def __init__(self, pkg_items):
        super(Package, self).__init__()
        self._pkg_items = pkg_items

    @staticmethod
    def read(path):
        """
        Factory method to construct a new |Package| instance from package
        at *path*. The package can be either a zip archive (e.g. .docx file)
        or a directory containing an extracted package.
        """
        phys_pkg = PhysPkg.read(path)
        pkg_items = {}
        for uri, blob in phys_pkg:
            pkg_items[uri] = PkgItem(phys_pkg.root_uri, uri, blob)
        return Package(pkg_items)

    def find_item_by_uri_tail(self, uri_tail):
        """
        Return the first item in this package having a uri that ends with
        *uri_tail*. Raises |KeyError| if no matching item is found.
        """


class PkgItem(object):
    """
    Individual item (file, roughly) within an OPC package.
    """
    def __init__(self, root_uri, uri, blob):
        super(PkgItem, self).__init__()
        self._blob = blob
        self._root_uri = root_uri
        self._uri = uri
