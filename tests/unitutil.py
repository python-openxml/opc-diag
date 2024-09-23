"""Utility functions for unit testing"""

from __future__ import annotations

import os
from typing import Any
from unittest.mock import ANY as ANY
from unittest.mock import Mock, PropertyMock, create_autospec, patch

from pytest import FixtureRequest  # noqa: PT013


def abspath(relpath: str):
    thisdir = os.path.split(__file__)[0]
    return os.path.abspath(os.path.join(thisdir, relpath))


def relpath(relpath: str):
    thisdir = os.path.split(__file__)[0]
    return os.path.relpath(os.path.join(thisdir, relpath))


def class_mock(q_class_name: str, request: FixtureRequest, autospec: bool = True, **kwargs: Any):
    """Return a mock patching the class with qualified name *q_class_name*.

    The mock is autospec'ed based on the patched class unless the optional
    argument *autospec* is set to False. Any other keyword arguments are
    passed through to Mock(). Patch is reversed after calling test returns.
    """
    _patch = patch(q_class_name, autospec=autospec, **kwargs)
    request.addfinalizer(_patch.stop)
    return _patch.start()


def function_mock(q_function_name: str, request: FixtureRequest):
    """Return a mock patching the function with qualified name *q_function_name*.

    Patch is reversed after calling test returns.
    """
    _patch = patch(q_function_name)
    request.addfinalizer(_patch.stop)
    return _patch.start()


def initializer_mock(Cls: type, request: FixtureRequest):
    """Return a mock for the __init__ method on *Cls*."""
    _patch = patch.object(Cls, "__init__", return_value=None)
    request.addfinalizer(_patch.stop)
    return _patch.start()


def instance_mock(
    Cls: type,
    request: FixtureRequest,
    name: str | None = None,
    spec_set: bool = True,
    **kwargs: Any,
):
    """Return a mock for an instance of *Cls* that draws its spec from the class.

    The mock does not allow new attributes to be set on the instance. If *name* is missing or
    |None|, the name of the returned |Mock| instance is set to *request.fixturename*. Additional
    keyword arguments are passed through to the Mock() call that creates the mock.
    """
    if name is None:
        name = request.fixturename
    return create_autospec(Cls, _name=name, spec_set=spec_set, instance=True, **kwargs)


def loose_mock(request: FixtureRequest, name: str | None = None, **kwargs: Any):
    """Return a "loose" mock, meaning it has no spec to constrain calls on it.

    Additional keyword arguments are passed through to Mock().
    """
    if name is None:
        name = request.fixturename
    return Mock(name=name, **kwargs)


def method_mock(Cls: type, method_name: str, request: FixtureRequest):
    """Return a mock for method `method_name` on `cls`."""
    _patch = patch.object(Cls, method_name)
    request.addfinalizer(_patch.stop)
    return _patch.start()


def property_mock(q_property_name: str, request: FixtureRequest):
    """Return a mock for property with fully qualified name *q_property_name*."""
    _patch = patch(q_property_name, new_callable=PropertyMock)
    request.addfinalizer(_patch.stop)
    return _patch.start()


def var_mock(q_var_name: str, request: FixtureRequest, **kwargs: Any):
    """Return a mock patching the variable with qualified name `q_var_name`."""
    _patch = patch(q_var_name, **kwargs)
    request.addfinalizer(_patch.stop)
    return _patch.start()
