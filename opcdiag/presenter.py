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
    def __init__(self, pkg_item):
        super(ItemPresenter, self).__init__()
        self._pkg_item = pkg_item
