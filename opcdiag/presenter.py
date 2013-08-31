# -*- coding: utf-8 -*-
#
# presenter.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of opc-diag and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Presenter classes for opc-diag model classes"""

from __future__ import unicode_literals

import re

from lxml import etree


class ItemPresenter(object):
    """
    Base class and factory class for package item presenter classes; also
    serves as presenter for binary classes, e.g. .bin and .jpg.
    """
    def __new__(cls, pkg_item):
        """
        Factory for package item presenter objects, choosing one of
        |ContentTypes|, |RelsItem|, or |Part| based on the characteristics of
        *pkg_item*.
        """
        if pkg_item.is_content_types:
            presenter_class = ContentTypesPresenter
        elif pkg_item.is_rels_item:
            presenter_class = RelsItemPresenter
        elif pkg_item.is_xml_part:
            presenter_class = XmlPartPresenter
        else:
            presenter_class = ItemPresenter
        return super(ItemPresenter, cls).__new__(presenter_class)

    def __init__(self, pkg_item):
        super(ItemPresenter, self).__init__()
        self._pkg_item = pkg_item

    @property
    def text(self):
        """
        Raise |NotImplementedError|; all subclasses must implement a ``text``
        property, returning a text representation of the package item,
        generally a formatted version of the item contents.
        """
        msg = ("'.text' property must be implemented by all subclasses of It"
               "emPresenter")
        raise NotImplementedError(msg)

    @property
    def xml(self):
        """
        Return pretty-printed XML (as unicode text) from this package item's
        blob.
        """
        xml_bytes = etree.tostring(
            self._pkg_item.element, encoding='UTF-8', pretty_print=True,
            standalone=True).strip()
        xml_text = xml_bytes.decode('utf-8')
        return xml_text


class ContentTypesPresenter(ItemPresenter):

    def __init__(self, pkg_item):
        super(ContentTypesPresenter, self).__init__(pkg_item)

    @property
    def text(self):
        """
        Return the <Types ...> XML for this content types item formatted for
        minimal diffs. The <Default> and <Override> child elements are sorted
        to remove arbitrary ordering between package saves.
        """
        lines = self.xml.split('\n')
        defaults = sorted([l for l in lines if l.startswith('  <D')])
        overrides = sorted([l for l in lines if l.startswith('  <O')])
        out_lines = lines[:2] + defaults + overrides + lines[-1:]
        out = '\n'.join(out_lines)
        return out


class RelsItemPresenter(ItemPresenter):

    def __init__(self, pkg_item):
        super(RelsItemPresenter, self).__init__(pkg_item)

    @property
    def text(self):
        """
        Return the <Relationships ...> XML for this rels item formatted for
        minimal diffs. The <Relationship> child elements are sorted to remove
        arbitrary ordering between package saves. rId values are all set to
        'x' so internal renumbering between saves doesn't affect the
        ordering.
        """
        def anon(rel):
            return re.sub(r' Id="[^"]+" ', r' Id="x" ', rel)

        lines = self.xml.split('\n')
        relationships = [l for l in lines if l.startswith('  <R')]
        anon_rels = sorted([anon(r) for r in relationships])
        out_lines = lines[:2] + anon_rels + lines[-1:]
        out = '\n'.join(out_lines)
        return out


class XmlPartPresenter(ItemPresenter):

    def __init__(self, pkg_item):
        super(XmlPartPresenter, self).__init__(pkg_item)
