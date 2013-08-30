# -*- coding: utf-8 -*-
#
# test_cli.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of opc-diag and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Test suite for the cli module."""

from opcdiag.cli import CommandController, main

import pytest

from .unitutil import class_mock, instance_mock


@pytest.fixture
def argv_(request):
    return instance_mock(list, request)


@pytest.fixture
def CommandController_(request, command_controller_):
    CommandController_ = class_mock('opcdiag.cli.CommandController', request)
    CommandController_.return_value = command_controller_
    CommandController_.new.return_value = command_controller_
    return CommandController_


@pytest.fixture
def command_controller_(request):
    return instance_mock(CommandController, request)


class DescribeMain(object):

    def it_should_execute_the_command_in_argv(
            self, argv_, CommandController_, command_controller_):
        # exercise ---------------------
        main(argv_)
        # verify -----------------------
        CommandController_.new.assert_called_once_with()
        command_controller_.execute.assert_called_once_with(argv_)
