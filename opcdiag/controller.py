# -*- coding: utf-8 -*-
#
# controller.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of opc-diag and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Command-line application controller for opc-diag"""

from opcdiag.model import Package
from opcdiag.presenter import DiffPresenter, ItemPresenter
from opcdiag.view import OpcView


_CONTENT_TYPES_URI = '[Content_Types].xml'


class OpcController(object):
    """
    Mediate between the command-line interface and the package model
    entities, orchestrating the execution of user commands by creating
    entity objects, delegating work to them, and using the appropriate view
    object to format the results to be displayed.
    """
    def browse(self, pkg_path, uri_tail):
        """
        Display pretty-printed XML contained in package item with URI ending
        with *uri_tail* in package at *pkg_path*.
        """
        pkg = Package.read(pkg_path)
        pkg_item = pkg.find_item_by_uri_tail(uri_tail)
        item_presenter = ItemPresenter(pkg_item)
        OpcView.pkg_item(item_presenter)

    def diff_item(self, package_1_path, package_2_path, uri_tail):
        """
        Display the meaningful differences between the item identified by
        *uri_tail* in the package at *package_1_path* and its counterpart in
        the package at *package_2_path*. Each path can be either a standard
        zip package (e.g. a .pptx file) or a directory containing an extracted
        package.
        """
        package_1 = Package.read(package_1_path)
        package_2 = Package.read(package_2_path)
        diff = DiffPresenter.named_item_diff(package_1, package_2, uri_tail)
        OpcView.item_diff(diff)

    def diff_pkg(self, package_1_path, package_2_path):
        """
        Display the meaningful differences between the packages at
        *package_1_path* and *package_2_path*. Each path can be either a
        standard zip package (e.g. .pptx file) or a directory containing an
        extracted package.
        """
        package_1 = Package.read(package_1_path)
        package_2 = Package.read(package_2_path)
        content_types_diff = DiffPresenter.named_item_diff(
            package_1, package_2, _CONTENT_TYPES_URI)
        rels_diffs = DiffPresenter.rels_diffs(package_1, package_2)
        xml_part_diffs = DiffPresenter.xml_part_diffs(package_1, package_2)
        OpcView.package_diff(content_types_diff, rels_diffs, xml_part_diffs)
