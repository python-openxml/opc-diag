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

from opcdiag.cli import BrowseCommand, Command, CommandController, main
from opcdiag.controller import OpcController

import pytest

from mock import ANY, Mock

from .unitutil import class_mock, instance_mock, loose_mock


ARG_PKG_PATH = 'PKG_PATH'
ARG_FILENAME = 'FILENAME'
CMD_WORD_BROWSE = 'browse'


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
def browse_argv_():
    return [CMD_WORD_BROWSE, ARG_PKG_PATH, ARG_FILENAME]


@pytest.fixture
def CommandController_(request, command_controller_):
    CommandController_ = class_mock('opcdiag.cli.CommandController', request)
    CommandController_.return_value = command_controller_
    CommandController_.new.return_value = command_controller_
    return CommandController_


@pytest.fixture
def Command_(request, command_cls_, parser_):
    Command_ = class_mock('opcdiag.cli.Command', request, autospec=False)
    Command_.__subclasses__ = Mock(return_value=[command_cls_])
    Command_.parser.return_value = parser_
    return Command_


@pytest.fixture
def command_(request):
    return instance_mock(Command, request)


@pytest.fixture
def command_cls_(request, command_, command_parser_):
    command_cls_ = loose_mock(request)
    command_cls_.return_value = command_
    command_cls_.add_command_parser_to.return_value = command_parser_
    return command_cls_


@pytest.fixture
def command_controller_(request):
    return instance_mock(CommandController, request)


@pytest.fixture
def command_parser_(request):
    command_parser_ = instance_mock(argparse.ArgumentParser, request)
    return command_parser_


@pytest.fixture
def OpcController_(request, app_controller_):
    OpcController_ = class_mock('opcdiag.cli.OpcController', request)
    OpcController_.return_value = app_controller_
    return OpcController_


@pytest.fixture
def parser():
    return argparse.ArgumentParser()


@pytest.fixture
def parser_(request, args_):
    parser_ = instance_mock(argparse.ArgumentParser, request)
    parser_.parse_args.return_value = args_
    return parser_


@pytest.fixture
def subparsers(parser):
    return parser.add_subparsers()


class DescribeMain(object):

    def it_should_execute_the_command_in_argv(
            self, argv_, CommandController_, command_controller_):
        # exercise ---------------------
        main(argv_)
        # verify -----------------------
        CommandController_.new.assert_called_once_with()
        command_controller_.execute.assert_called_once_with(argv_)


class DescribeCommand(object):

    def it_can_configure_the_command_line_parser(
            self, Command_, command_cls_, command_, command_parser_):
        # exercise ---------------------
        parser = Command.parser()
        # verify -----------------------
        # return value of add_subparsers is a messy tuple, accept ANY
        command_cls_.add_command_parser_to.assert_called_once_with(ANY)
        command_cls_.assert_called_once_with(command_parser_)
        command_parser_.set_defaults.assert_called_once_with(command=command_)
        assert isinstance(parser, argparse.ArgumentParser)


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

    def it_can_execute_a_command_in_argv_form(
            self, parser_, app_controller_, argv_, args_, command_):
        # fixture ----------------------
        command_controller = CommandController(parser_, app_controller_)
        # exercise ---------------------
        command_controller.execute(argv_)
        # verify -----------------------
        command_.validate.assert_called_once_with(args_)
        command_.execute.assert_called_once_with(args_, app_controller_)


class DescribeBrowseCommand(object):

    def it_should_add_a_browse_command_parser(
            self, browse_argv_, parser, subparsers):
        # exercise ---------------------
        subparser = BrowseCommand.add_command_parser_to(subparsers)
        args = parser.parse_args(browse_argv_)
        # verify -----------------------
        assert args.pkg_path == ARG_PKG_PATH
        assert args.filename == ARG_FILENAME
        assert isinstance(subparser, argparse.ArgumentParser)
