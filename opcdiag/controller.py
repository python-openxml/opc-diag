# -*- coding: utf-8 -*-
#
# controller.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of opc-diag and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Command-line application controller for opc-diag"""


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
