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


class ContentTypesPresenter(ItemPresenter):

    def __init__(self, pkg_item):
        super(ContentTypesPresenter, self).__init__(pkg_item)


class RelsItemPresenter(ItemPresenter):

    def __init__(self, pkg_item):
        super(RelsItemPresenter, self).__init__(pkg_item)


class XmlPartPresenter(ItemPresenter):

    def __init__(self, pkg_item):
        super(XmlPartPresenter, self).__init__(pkg_item)
