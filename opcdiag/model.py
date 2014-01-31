# -*- coding: utf-8 -*-

"""
Package and package items model
"""

import os

from lxml import etree

from opcdiag.phys_pkg import BlobCollection, PhysPkg


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

    def prettify_xml(self):
        """
        Reformat the XML in all package items having XML content to indented,
        human-readable format. If viewed after this method is called, the XML
        appears "pretty printed".
        """
        for pkg_item in self._pkg_items.itervalues():
            pkg_item.prettify_xml()

    @property
    def rels_items(self):
        """
        Return list of rels items in this package, sorted by pack URI.
        """
        rels_items = []
        for uri in self._uris:
            pkg_item = self._pkg_items[uri]
            if pkg_item.is_rels_item:
                rels_items.append(pkg_item)
        return rels_items

    def save(self, path):
        """
        Save this package to a zip archive at *path*.
        """
        PhysPkg.write_to_zip(self._blobs, path)

    def save_to_dir(self, dirpath):
        """
        Save each of the items in this package as a file in a directory at
        *dirpath*, using the pack URI as the relative path of each file. If
        the directory exists, it is deleted (recursively) before being
        recreated.
        """
        PhysPkg.write_to_dir(self._blobs, dirpath)

    def substitute_item(self, src_pkg_item):
        """
        Locate the item in this package that corresponds with *src_pkg_item*
        and replace its blob with that from *src_pkg_item*.
        """
        tgt_pkg_item = self._pkg_items[src_pkg_item.uri]
        tgt_pkg_item.blob = src_pkg_item.blob

    @property
    def xml_parts(self):
        """
        Return list of XML parts in this package, sorted by partname.
        """
        xml_parts = []
        for uri in self._uris:
            pkg_item = self._pkg_items[uri]
            if pkg_item.is_xml_part:
                xml_parts.append(pkg_item)
        return xml_parts

    @property
    def _blobs(self):
        """
        A |BlobCollection| instance containing a snapshot of the blobs in the
        package.
        """
        blobs = BlobCollection()
        for uri, pkg_item in self._pkg_items.items():
            blobs[uri] = pkg_item.blob
        return blobs

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
    def blob(self):
        """
        The binary contents of this package item, frequently but not always
        XML text.
        """
        return self._blob  # pragma: no cover

    @blob.setter
    def blob(self, value):
        self._blob = value  # pragma: no cover

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

    def prettify_xml(self):
        """
        Reformat the XML in this package item to indented, human-readable
        form. Does nothing if this package item does not contain XML.
        """
        if self.is_content_types or self.is_xml_part or self.is_rels_item:
            self._blob = etree.tostring(
                self.element, encoding='UTF-8', standalone=True,
                pretty_print=True
            )

    @property
    def uri(self):
        """
        The pack URI of this package item, e.g. ``'/word/document.xml'``.
        """
        return self._uri  # pragma: no cover
