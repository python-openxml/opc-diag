# -*- coding: utf-8 -*-
#
# view.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of opc-diag and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""
Objects that fulfill the view role in opc-diag, interfacing to the console
"""

from __future__ import print_function, unicode_literals

import sys


def _write(text):
    """
    Write *text* to stdout
    """
    print(text, end='', file=sys.stdout)


class OpcView(object):
    """
    Interfaces to the console by formatting command results for proper
    display.
    """
    @staticmethod
    def item_diff(diff):
        """
        Display *diff*, a standard unified_diff string, on stdout.
        """
        text = ''
        if diff:
            text += '%s\n' % diff
        _write(text)

    @staticmethod
    def package_diff(content_types_diff, rels_diffs, xml_part_diffs):
        """
        Write to stdout a consolidated diff between two packages, including
        its *content_types_diff*, any *rels_diffs*, and any *xml_part_diffs*.
        """

    @staticmethod
    def pkg_item(pkg_item):
        """
        Display the text value of pkg_item, adding a linefeed at the end to
        make the terminal happy.
        """
        text = '%s\n' % pkg_item.text
        _write(text)
