# -*- coding: utf-8 -*-
#
# model.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of opc-diag and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Package and package items model"""

import os

from lxml import etree

from opcdiag.phys_pkg import PhysPkg


_CONTENT_TYPES_URI = '[Content_Types].xml'


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
        for uri in self._uris:
            if uri.endswith(uri_tail):
                return self._pkg_items[uri]
        raise KeyError("No item with name '%s'" % uri_tail)

    @property
    def _uris(self):
        """
        Return sorted list of item URIs in this package.
        """
        return sorted(self._pkg_items.keys())


class PkgItem(object):
    """
    Individual item (file, roughly) within an OPC package.
    """
    def __init__(self, root_uri, uri, blob):
        super(PkgItem, self).__init__()
        self._blob = blob
        self._root_uri = root_uri
        self._uri = uri

    @property
    def element(self):
        """
        Return an lxml.etree Element obtained by parsing the XML in this
        item's blob.
        """
        return etree.fromstring(self._blob)

    @property
    def is_content_types(self):
        """
        True if this item is the ``[Content_Types].xml`` item in the package,
        False otherwise.
        """
        return self._uri == _CONTENT_TYPES_URI

    @property
    def is_rels_item(self):
        """
        True if this item is a relationships item, i.e. its uri ends with
        ``.rels``, False otherwise.
        """
        return self._uri.endswith('.rels')

    @property
    def is_xml_part(self):
        """
        True if the URI of this item ends with '.xml', except if it is the
        content types item. False otherwise.
        """
        return self._uri.endswith('.xml') and not self.is_content_types

    @property
    def path(self):
        """
        Return the path of this item as though it were extracted into a
        directory at its package path.
        """
        uri_part = os.path.normpath(self._uri)
        return os.path.join(self._root_uri, uri_part)
