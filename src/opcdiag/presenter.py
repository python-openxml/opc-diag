"""Presenter classes for opc-diag model classes."""

from __future__ import annotations

import re
from difflib import unified_diff
from typing import TYPE_CHECKING, Sequence, cast

from lxml import etree

if TYPE_CHECKING:
    from opcdiag.model import Package, PkgItemT


def diff(text_1: str, text_2: str, filename_1: str, filename_2: str):
    """Return a ``diff`` style unified diff listing between *text_1* and *text_2*."""
    lines_1 = text_1.split("\n")
    lines_2 = text_2.split("\n")
    diff_lines = unified_diff(lines_1, lines_2, filename_1, filename_2)
    # this next bit is needed to work around Python 2.6 difflib bug that left
    # in a trailing space after the filename if no date was provided. The
    # filename lines look like: '--- filename \n' where regular lines look
    # like '+foobar'. The space needs to be removed but the linefeed preserved.
    trimmed_lines: list[str] = []
    for line in diff_lines:
        if line.endswith(" \n"):
            line = "%s\n" % line.rstrip()
        trimmed_lines.append(line)
    return "\n".join(trimmed_lines)


def prettify_nsdecls(xml: str):
    """Wrap and indent attributes on the root element.

    This avoids namespace declarations running off the page in the text editor such that they can
    be more easily inspected. Attributes are sorted such that the default namespace, if present,
    appears first in the list, followed by other namespace declarations, and then remaining
    attributes, both in alphabetical order.
    """

    def parse_attrs(rootline: str):
        """
        Return 3-tuple (head, attributes, tail) looking like
        ('<p:sld', ['xmlns:p="html://..."', 'name="Office Theme>"'], '>').
        """
        attr_re = re.compile(r'([-a-zA-Z0-9_:.]+="[^"]*" *)')
        substrs = [substr.strip() for substr in attr_re.split(rootline) if substr]
        head = substrs[0]
        attrs, tail = (substrs[1:-1], substrs[-1]) if len(substrs) > 1 else ([], "")
        return (head, attrs, tail)

    def sequence_attrs(attributes: Sequence[str]):
        """Sort attributes alphabetically within subgroups.

        The subgroupings are default namespace declaration, other namespace declarations, and
        other attributes.
        """
        def_nsdecls: list[str] = []
        nsdecls: list[str] = []
        attrs: list[str] = []
        for attr in attributes:
            if attr.startswith("xmlns="):
                def_nsdecls.append(attr)
            elif attr.startswith("xmlns:"):
                nsdecls.append(attr)
            else:
                attrs.append(attr)
        return sorted(def_nsdecls) + sorted(nsdecls) + sorted(attrs)

    def pretty_rootline(head: str, attrs: Sequence[str], tail: str):
        """Return string containing prettified XML root line.

        *head* appears on the first line, *attrs* indented on following lines, and *tail* indented
        on the last line.
        """
        indent = 4 * " "
        newrootline = head
        for attr in attrs:
            newrootline += "\n%s%s" % (indent, attr)
        newrootline += "\n%s%s" % (indent, tail) if tail else ""
        return newrootline

    lines = xml.splitlines()
    rootline = lines[1]
    head, attributes, tail = parse_attrs(rootline)
    attributes = sequence_attrs(attributes)
    lines[1] = pretty_rootline(head, attributes, tail)
    return "\n".join(lines)


class DiffPresenter:
    """Forms diffs between packages and their elements."""

    @staticmethod
    def named_item_diff(package_1: Package, package_2: Package, uri_tail: str):
        """Return a diff between the corresponding text of two packages.

        The text item is identified by *uri_tail*, and the version in *package_1* is compared with
        its counterpart in *package_2*.
        """
        pkg_item_1 = package_1.find_item_by_uri_tail(uri_tail)
        pkg_item_2 = package_2.find_item_by_uri_tail(uri_tail)
        return DiffPresenter._pkg_item_diff(pkg_item_1, pkg_item_2)

    @staticmethod
    def rels_diffs(package_1: Package, package_2: Package):
        """Return a list of diffs between the rels items in *package_1* and *package_2*.

        Rels items are compared in alphabetical order by pack URI.
        """
        package_1_rels_items = package_1.rels_items
        return DiffPresenter._pkg_item_diffs(package_1_rels_items, package_2)

    @staticmethod
    def xml_part_diffs(package_1: Package, package_2: Package):
        """
        Return a list of diffs between the XML parts in *package_1* and their
        counterpart in *package_2*. Parts are compared in alphabetical order
        by partname (pack URI).
        """
        package_1_xml_parts = package_1.xml_parts
        return DiffPresenter._pkg_item_diffs(package_1_xml_parts, package_2)

    @staticmethod
    def _pkg_item_diff(pkg_item_1: PkgItemT, pkg_item_2: PkgItemT):
        """Return a diff between the text of *pkg_item_1* and that of *pkg_item_2*."""
        item_presenter_1 = ItemPresenter(pkg_item_1)
        item_presenter_2 = ItemPresenter(pkg_item_2)
        text_1 = item_presenter_1.text
        text_2 = item_presenter_2.text
        filename_1 = item_presenter_1.filename
        filename_2 = item_presenter_2.filename
        return diff(text_1, text_2, filename_1, filename_2)

    @staticmethod
    def _pkg_item_diffs(pkg_items: list[PkgItemT], package_2: Package):
        """Return a list of diffs.

        There is one diff for each item in *pkg_items* that differs from its counterpart in
        *package_2*.
        """
        diffs: list[str] = []
        for pkg_item in pkg_items:
            uri = pkg_item.uri
            pkg_item_2 = package_2.find_item_by_uri_tail(uri)
            diff = DiffPresenter._pkg_item_diff(pkg_item, pkg_item_2)
            if diff:
                diffs.append(diff)
        return diffs


class ItemPresenter:
    """Base class and factory class for package item presenter classes.

    Also serves as presenter for binary classes, e.g. .bin and .jpg.
    """

    def __new__(cls, pkg_item: PkgItemT):
        """Factory for package item presenter objects.

        Chooses one of |ContentTypes|, |RelsItem|, or |Part| based on the characteristics of
        `pkg_item`.
        """
        if pkg_item.is_content_types:
            presenter_class = ContentTypesPresenter
        elif pkg_item.is_rels_item:
            presenter_class = RelsItemPresenter
        elif pkg_item.is_xml_part:
            presenter_class = XmlPartPresenter
        else:
            presenter_class = ItemPresenter
        return super(ItemPresenter, cls).__new__(cast(type, presenter_class))

    def __init__(self, pkg_item: PkgItemT):
        super(ItemPresenter, self).__init__()
        self._pkg_item = pkg_item

    @property
    def filename(self) -> str:
        """Effective path for this package item.

        Normalized to always use forward slashes as the path separator.
        """
        return self._pkg_item.path.replace("\\", "/")

    @property
    def text(self) -> str:
        """
        Raise |NotImplementedError|; all subclasses must implement a ``text``
        property, returning a text representation of the package item,
        generally a formatted version of the item contents.
        """
        msg = "'.text' property must be implemented by all subclasses of It" "emPresenter"
        raise NotImplementedError(msg)

    @property
    def xml(self):
        """
        Return pretty-printed XML (as unicode text) from this package item's
        blob.
        """
        xml_bytes = etree.tostring(
            self._pkg_item.element, encoding="UTF-8", pretty_print=True, standalone=True
        ).strip()
        xml_text = xml_bytes.decode("utf-8")
        return xml_text


class ContentTypesPresenter(ItemPresenter):
    """Presenter for the `[Content_Types].xml` part."""

    @property
    def text(self):
        """Return the <Types ...> XML for this content types item formatted for minimal diffs.

        The <Default> and <Override> child elements are sorted to remove arbitrary ordering
        between package saves.
        """
        lines = self.xml.split("\n")
        defaults = sorted([ln for ln in lines if ln.startswith("  <D")])
        overrides = sorted([ln for ln in lines if ln.startswith("  <O")])
        out_lines = lines[:2] + defaults + overrides + lines[-1:]
        out = "\n".join(out_lines)
        return out


class RelsItemPresenter(ItemPresenter):
    """Presenter for a `*.rels` part, one that holds relationships between XML and binary parts."""

    @property
    def text(self):
        """Return the <Relationships ...> XML for this rels item formatted for minimal diffs.

        The <Relationship> child elements are sorted to remove arbitrary ordering between package
        saves. rId values are all set to 'x' so internal renumbering between saves doesn't affect
        the ordering.
        """

        def anon(rel: str):
            return re.sub(r' Id="[^"]+" ', r' Id="x" ', rel)

        lines = self.xml.split("\n")
        relationships = [ln for ln in lines if ln.startswith("  <R")]
        anon_rels = sorted([anon(r) for r in relationships])
        out_lines = lines[:2] + anon_rels + lines[-1:]
        out = "\n".join(out_lines)
        return out


class XmlPartPresenter(ItemPresenter):
    """Presenter for an XML part, generally ones with a "filename" ending in `.xml`."""

    @property
    def text(self):
        """
        Return pretty-printed XML of this part with the namespace declarations
        aligned and sorted to produce clear and minimal diffs.
        """
        return prettify_nsdecls(self.xml)
