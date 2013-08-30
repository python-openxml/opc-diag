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
from opcdiag.presenter import ItemPresenter
from opcdiag.view import OpcView


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
