# -*- coding: utf-8 -*-
#
# test_cli.py
#
# Copyright (C) 2013 Steve Canny scanny@cisco.com
#
# This module is part of opc-diag and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Test suite for the cli module."""

import argparse

from opcdiag.cli import Command, CommandController, main
from opcdiag.controller import OpcController

import pytest

from .unitutil import class_mock, instance_mock, loose_mock


@pytest.fixture
def app_controller_(request):
    return instance_mock(OpcController, request)


@pytest.fixture
def args_(request, command_):
    args_ = loose_mock(request)
    args_.command = command_
    return args_


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
def Command_(request, parser_):
    Command_ = class_mock('opcdiag.cli.Command', request)
    Command_.parser.return_value = parser_
    return Command_


@pytest.fixture
def command_(request):
    return instance_mock(Command, request)


@pytest.fixture
def command_controller_(request):
    return instance_mock(CommandController, request)


@pytest.fixture
def OpcController_(request, app_controller_):
    OpcController_ = class_mock('opcdiag.cli.OpcController', request)
    OpcController_.return_value = app_controller_
    return OpcController_


@pytest.fixture
def parser_(request, args_):
    parser_ = instance_mock(argparse.ArgumentParser, request)
    return parser_


class DescribeMain(object):

    def it_should_execute_the_command_in_argv(
            self, argv_, CommandController_, command_controller_):
        # exercise ---------------------
        main(argv_)
        # verify -----------------------
        CommandController_.new.assert_called_once_with()
        command_controller_.execute.assert_called_once_with(argv_)


class DescribeCommandController(object):

    def it_can_be_constructed_with_its_factory_method(
            self, Command_, CommandController_, command_controller_, parser_,
            OpcController_, app_controller_):
        # exercise ---------------------
        command_controller = CommandController.new()
        # verify -----------------------
        Command_.parser.assert_called_once_with()
        OpcController_.assert_called_once_with()
        CommandController_.assert_called_once_with(parser_, app_controller_)
        assert command_controller is command_controller_
