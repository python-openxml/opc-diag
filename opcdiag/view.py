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
    bytes_out = text.encode('utf-8')
    print(bytes_out, end='', file=sys.stdout)


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
        diff_blocks = [content_types_diff] if content_types_diff else []
        diff_blocks.extend(rels_diffs)
        diff_blocks.extend(xml_part_diffs)
        text = '%s\n' % '\n\n'.join(diff_blocks) if diff_blocks else ''
        _write(text)

    @staticmethod
    def pkg_item(pkg_item):
        """
        Display the text value of pkg_item, adding a linefeed at the end to
        make the terminal happy.
        """
        text = '%s\n' % pkg_item.text
        _write(text)

    @staticmethod
    def substitute(uri, src_pkg_path, tgt_pkg_path, new_pkg_path):
        """
        Display a confirmation method detailing the package item substitution
        that was executed.
        """
        msg = ("substituted '%s' from '%s' into '%s' and saved the result as"
               " '%s'\n" %
               (uri, src_pkg_path, tgt_pkg_path, new_pkg_path))
        msg = msg.replace('\\', '/')  # normalize directory separator
        _write(msg)
