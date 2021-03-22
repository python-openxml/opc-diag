# -*- coding: utf-8 -*-
#
# unitutil.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of opc-diag and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Utility functions for unit testing"""

import os

from mock import create_autospec, Mock, patch, PropertyMock


def abspath(relpath):
    thisdir = os.path.split(__file__)[0]
    return os.path.abspath(os.path.join(thisdir, relpath))


def relpath(relpath):
    thisdir = os.path.split(__file__)[0]
    return os.path.relpath(os.path.join(thisdir, relpath))


def class_mock(q_class_name, request, autospec=True, **kwargs):
    """
    Return a mock patching the class with qualified name *q_class_name*.
    The mock is autospec'ed based on the patched class unless the optional
    argument *autospec* is set to False. Any other keyword arguments are
    passed through to Mock(). Patch is reversed after calling test returns.
    """
    _patch = patch(q_class_name, autospec=autospec, **kwargs)
    request.addfinalizer(_patch.stop)
    return _patch.start()


def function_mock(q_function_name, request):
    """
    Return a mock patching the function with qualified name
    *q_function_name*. Patch is reversed after calling test returns.
    """
    _patch = patch(q_function_name)
    request.addfinalizer(_patch.stop)
    return _patch.start()


def initializer_mock(cls, request):
    """
    Return a mock for the __init__ method on *cls* where the patch is
    reversed after pytest uses it.
    """
    _patch = patch.object(cls, "__init__", return_value=None)
    request.addfinalizer(_patch.stop)
    return _patch.start()


def instance_mock(cls, request, name=None, spec_set=True, **kwargs):
    """
    Return a mock for an instance of *cls* that draws its spec from the class
    and does not allow new attributes to be set on the instance. If *name* is
    missing or |None|, the name of the returned |Mock| instance is set to
    *request.fixturename*. Additional keyword arguments are passed through to
    the Mock() call that creates the mock.
    """
    if name is None:
        name = request.fixturename
    return create_autospec(cls, _name=name, spec_set=spec_set, instance=True, **kwargs)


def loose_mock(request, name=None, **kwargs):
    """
    Return a "loose" mock, meaning it has no spec to constrain calls on it.
    Additional keyword arguments are passed through to Mock().
    """
    if name is None:
        name = request.fixturename
    return Mock(name=name, **kwargs)


def method_mock(cls, method_name, request):
    """
    Return a mock for method *method_name* on *cls* where the patch is
    reversed after pytest uses it.
    """
    _patch = patch.object(cls, method_name)
    request.addfinalizer(_patch.stop)
    return _patch.start()


def property_mock(q_property_name, request):
    """
    Return a mock for property with fully qualified name *q_property_name*
    where the patch is reversed after pytest uses it.
    """
    _patch = patch(q_property_name, new_callable=PropertyMock)
    request.addfinalizer(_patch.stop)
    return _patch.start()


def var_mock(q_var_name, request, **kwargs):
    """
    Return a mock patching the variable with qualified name *q_var_name*.
    Patch is reversed after calling test returns.
    """
    _patch = patch(q_var_name, **kwargs)
    request.addfinalizer(_patch.stop)
    return _patch.start()
