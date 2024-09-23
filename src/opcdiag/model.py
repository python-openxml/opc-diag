"""Package and package items model."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import os
from typing import Mapping, Protocol

from lxml import etree

from opcdiag.phys_pkg import BlobCollection, PhysPkg

_CONTENT_TYPES_URI = "[Content_Types].xml"

# ================================================================================================
# DOMAIN MODEL
# ================================================================================================


class PkgItemT(Protocol):
    @property
    def blob(self) -> bytes: ...
    @blob.setter
    def blob(self, value: bytes) -> None: ...
    @property
    def element(self) -> etree._Element: ...
    @property
    def is_content_types(self) -> bool: ...
    @property
    def is_rels_item(self) -> bool: ...
    @property
    def is_xml_part(self) -> bool: ...
    @property
    def path(self) -> str: ...
    def prettify_xml(self) -> None: ...
    @property
    def uri(self) -> str: ...


# ================================================================================================


class Package:
    """Root of package graph and main model API class."""

    def __init__(self, pkg_items: Mapping[str, PkgItemT]):
        super(Package, self).__init__()
        self._pkg_items = pkg_items

    @staticmethod
    def read(path: str) -> Package:
        """Factory method to construct a new |Package| instance from package at *path*.

        The package can be either a zip archive (e.g. .docx file) or a directory containing an
        extracted package.
        """
        phys_pkg = PhysPkg.read(path)
        pkg_items = {uri: PkgItem(phys_pkg.root_uri, uri, blob) for uri, blob in phys_pkg}
        return Package(pkg_items)

    def find_item_by_uri_tail(self, uri_tail: str) -> PkgItemT:
        """
        Return the first item in this package having a uri that ends with
        *uri_tail*. Raises |KeyError| if no matching item is found.
        """
        for uri in self._uris:
            if uri.endswith(uri_tail):
                return self._pkg_items[uri]
        raise KeyError("No item with name '%s'" % uri_tail)

    def prettify_xml(self):
        """Reformat package XML content to human-readable format.

        All package items having XML content are mutated to a multi-line, indented
        format. If viewed after this method is called, the XML appears "pretty printed".
        """
        for pkg_item in self._pkg_items.values():
            pkg_item.prettify_xml()

    @property
    def rels_items(self) -> list[PkgItemT]:
        """Return list of rels items in this package, sorted by pack URI."""
        rels_items: list[PkgItemT] = []
        for uri in self._uris:
            pkg_item = self._pkg_items[uri]
            if pkg_item.is_rels_item:
                rels_items.append(pkg_item)
        return rels_items

    def save(self, path: str):
        """Save this package to a zip archive at *path*."""
        PhysPkg.write_to_zip(self._blobs, path)

    def save_to_dir(self, dirpath: str):
        """Save each of the items in this package as a file in a directory at *dirpath*.

        Uses the pack URI as the relative path of each file. If the directory exists, it is
        deleted (recursively) before being recreated.
        """
        PhysPkg.write_to_dir(self._blobs, dirpath)

    def substitute_item(self, src_pkg_item: PkgItemT):
        """Replace corresponding pkg-item in this package with `src_pkg_item`.

        This allows a diagnotic procedure of subtituting a single package item with one from a
        known working package to narrow down a problematic package part.

        `src_pkg_item` replaces the item with the same URI in this package.
        """
        tgt_pkg_item = self._pkg_items[src_pkg_item.uri]
        tgt_pkg_item.blob = src_pkg_item.blob

    @property
    def xml_parts(self) -> list[PkgItemT]:
        """Return list of XML parts in this package, sorted by partname."""
        return [
            pkg_item
            for pkg_item in (self._pkg_items[uri] for uri in self._uris)
            if pkg_item.is_xml_part
        ]

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


class PkgItem:
    """Individual item (file, roughly) within an OPC package."""

    def __init__(self, root_uri: str, uri: str, blob: bytes):
        self._blob = blob
        self._root_uri = root_uri
        self._uri = uri

    @property
    def blob(self) -> bytes:
        """The binary contents of this package item.

        Frequently but not always XML text.
        """
        return self._blob

    @blob.setter
    def blob(self, value: bytes):
        self._blob = value

    @property
    def element(self) -> etree._Element:
        """Return an lxml.etree Element obtained by parsing the XML in this item's blob."""
        element = etree.fromstring(self._blob)
        # -- this handles some odd cases where the XML was hand edited and some whitespace
        # -- tail-text was left.
        etree.indent(element)
        return element

    @property
    def is_content_types(self) -> bool:
        """True if this item is the ``[Content_Types].xml`` item in the package."""
        return self._uri == _CONTENT_TYPES_URI

    @property
    def is_rels_item(self) -> bool:
        """True if this item is a relationships item, i.e. its uri ends with `.rels`."""
        return self._uri.endswith(".rels")

    @property
    def is_xml_part(self) -> bool:
        """True if the URI of this item ends with '.xml', except if it is the content types item."""
        return self._uri.endswith(".xml") and not self.is_content_types

    @property
    def path(self) -> str:
        """Path of this item as though it were extracted into a directory at its package path."""
        uri_part = os.path.normpath(self._uri)
        return os.path.join(self._root_uri, uri_part)

    def prettify_xml(self) -> None:
        """Reformat XML in this package item to indented, human-readable form.

        Does nothing if this package item does not contain XML.
        """
        if self.is_content_types or self.is_xml_part or self.is_rels_item:
            self._blob = etree.tostring(
                self.element, encoding="UTF-8", standalone=True, pretty_print=True
            )

    @property
    def uri(self) -> str:
        """The pack URI of this package item, e.g. `'/word/document.xml'`."""
        return self._uri  # pragma: no cover
