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

from opcdiag.cli import (
    BrowseCommand, Command, CommandController, DiffCommand, DiffItemCommand,
    ExtractCommand, RepackageCommand, SubstituteCommand, main
)
from opcdiag.controller import OpcController

import pytest

from mock import ANY, Mock

from .unitutil import class_mock, instance_mock, loose_mock, relpath


ARG_DIRPATH = 'DIRPATH'
ARG_PKG_PATH = 'PKG_PATH'
ARG_PKG_2_PATH = 'PKG_2_PATH'
ARG_FILENAME = 'FILENAME'
ARG_NEW_PACKAGE = 'NEW_PACKAGE'
ARG_SRC_PKG_PATH = 'SRC_PKG_PATH'
ARG_TGT_PKG_PATH = 'TGT_PKG_PATH'
ARG_RESULT_PKG_PATH = 'RESULT_PKG_PATH'
CMD_WORD_BROWSE = 'browse'
CMD_WORD_DIFF = 'diff'
CMD_WORD_DIFF_ITEM = 'diff-item'
CMD_WORD_EXTRACT = 'extract'
CMD_WORD_REPACKAGE = 'repackage'
CMD_WORD_SUBSTITUTE = 'substitute'
MINI_DIR_PKG_PATH = relpath('test_files/mini_pkg')
MINI_ZIP_PKG_PATH = relpath('test_files/mini_pkg.zip')


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
def diff_argv_():
    return [CMD_WORD_DIFF, ARG_PKG_PATH, ARG_PKG_2_PATH]


@pytest.fixture
def diff_item_argv_():
    return [CMD_WORD_DIFF_ITEM, ARG_PKG_PATH, ARG_PKG_2_PATH, ARG_FILENAME]


@pytest.fixture
def extract_argv_():
    return [CMD_WORD_EXTRACT, ARG_PKG_PATH, ARG_DIRPATH]


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
def repackage_argv_():
    return [CMD_WORD_REPACKAGE, ARG_DIRPATH, ARG_NEW_PACKAGE]


@pytest.fixture
def subparsers(parser):
    return parser.add_subparsers()


@pytest.fixture
def substitute_argv_():
    return [CMD_WORD_SUBSTITUTE, ARG_FILENAME, ARG_SRC_PKG_PATH,
            ARG_TGT_PKG_PATH, ARG_RESULT_PKG_PATH]


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

    def it_should_raise_if_validate_not_implemented_on_subclass(self):
        command = Command(None)
        with pytest.raises(NotImplementedError):
            command.validate(None)

    def it_should_raise_if_execute_not_implemented_on_subclass(self):
        command = Command(None)
        with pytest.raises(NotImplementedError):
            command.execute(None, None)


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

    def it_should_trigger_parser_error_if_pkg_path_does_not_exist(
            self, args_, parser_):
        # fixture ----------------------
        args_.pkg_path = 'foobar'
        browse_command = BrowseCommand(parser_)
        # exercise ---------------------
        browse_command.validate(args_)
        # verify -----------------------
        parser_.error.assert_called_once_with(ANY)

    def it_can_dispatch_browse_command_to_app(self, args_, app_controller_):
        # fixture ----------------------
        browse_command = BrowseCommand(None)
        # exercise ---------------------
        browse_command.execute(args_, app_controller_)
        # verify -----------------------
        app_controller_.browse.assert_called_once_with(args_.pkg_path,
                                                       args_.filename)


class DescribeDiffCommand(object):

    def it_should_add_a_diff_command_parser(
            self, subparsers, parser, diff_argv_):
        # exercise ---------------------
        subparser = DiffCommand.add_command_parser_to(subparsers)
        args = parser.parse_args(diff_argv_)
        # verify -----------------------
        assert args.pkg_1_path == ARG_PKG_PATH
        assert args.pkg_2_path == ARG_PKG_2_PATH
        assert isinstance(subparser, argparse.ArgumentParser)

    @pytest.mark.parametrize(('pkg_1_path', 'pkg_2_path', 'err_frag'), [
        ('foobar', MINI_ZIP_PKG_PATH, 'PKG_1'),
        (MINI_ZIP_PKG_PATH, 'foobar', 'PKG_2'),
    ])
    def it_should_trigger_parser_error_if_pkg_path_does_not_exist(
            self, pkg_1_path, pkg_2_path, err_frag, args_, parser_):
        # fixture ----------------------
        args_.pkg_1_path = pkg_1_path
        args_.pkg_2_path = pkg_2_path
        diff_command = DiffCommand(parser_)
        # exercise ---------------------
        diff_command.validate(args_)
        # verify -----------------------
        parser_.error.assert_called_once_with(ANY)
        assert err_frag in parser_.error.call_args[0][0]

    def it_can_dispatch_a_diff_command_to_the_app(
            self, args_, app_controller_):
        # fixture ----------------------
        diff_command = DiffCommand(None)
        # exercise ---------------------
        diff_command.execute(args_, app_controller_)
        # verify -----------------------
        app_controller_.diff_pkg.assert_called_once_with(
            args_.pkg_1_path, args_.pkg_2_path)


class DescribeDiffItemCommand(object):

    def it_should_add_a_diff_item_command_parser(
            self, diff_item_argv_, parser, subparsers):
        # exercise ---------------------
        subparser = DiffItemCommand.add_command_parser_to(subparsers)
        args = parser.parse_args(diff_item_argv_)
        # verify -----------------------
        assert args.pkg_1_path == ARG_PKG_PATH
        assert args.pkg_2_path == ARG_PKG_2_PATH
        assert args.filename == ARG_FILENAME
        assert isinstance(subparser, argparse.ArgumentParser)

    @pytest.mark.parametrize(('pkg_1_path', 'pkg_2_path', 'err_frag'), [
        ('foobar', MINI_ZIP_PKG_PATH, 'PKG_1'),
        (MINI_ZIP_PKG_PATH, 'foobar', 'PKG_2'),
    ])
    def it_should_trigger_parser_error_if_pkg_path_does_not_exist(
            self, pkg_1_path, pkg_2_path, err_frag, args_, parser_):
        # fixture ----------------------
        args_.pkg_1_path = pkg_1_path
        args_.pkg_2_path = pkg_2_path
        diff_item_command = DiffItemCommand(parser_)
        # exercise ---------------------
        diff_item_command.validate(args_)
        # verify -----------------------
        parser_.error.assert_called_once_with(ANY)
        assert err_frag in parser_.error.call_args[0][0]

    def it_can_dispatch_diff_item_command_to_app(self, args_, app_controller_):
        # fixture ----------------------
        diff_item_command = DiffItemCommand(None)
        # exercise ---------------------
        diff_item_command.execute(args_, app_controller_)
        # verify -----------------------
        app_controller_.diff_item.assert_called_once_with(
            args_.pkg_1_path, args_.pkg_2_path, args_.filename)


class DescribeExtractCommand(object):

    def it_should_add_a_extract_command_parser(
            self, extract_argv_, parser, subparsers):
        # exercise ---------------------
        subparser = ExtractCommand.add_command_parser_to(subparsers)
        args = parser.parse_args(extract_argv_)
        # verify -----------------------
        assert args.pkg_path == ARG_PKG_PATH
        assert args.dirpath == ARG_DIRPATH
        assert isinstance(subparser, argparse.ArgumentParser)

    def it_should_trigger_parser_error_if_pkg_path_does_not_exist(
            self, args_, parser_):
        # fixture ----------------------
        args_.pkg_path = 'foobar'
        extract_command = ExtractCommand(parser_)
        # exercise ---------------------
        extract_command.validate(args_)
        # verify -----------------------
        parser_.error.assert_called_once_with(ANY)
        assert 'PKG_PATH' in parser_.error.call_args[0][0]

    def it_can_dispatch_an_extract_command_to_the_app(
            self, args_, app_controller_):
        # fixture ----------------------
        extract_command = ExtractCommand(None)
        # exercise ---------------------
        extract_command.execute(args_, app_controller_)
        # verify -----------------------
        app_controller_.extract_package.assert_called_once_with(
            args_.pkg_path, args_.dirpath)


class DescribeRepackageCommand(object):

    def it_should_add_a_repackage_command_parser(
            self, repackage_argv_, parser, subparsers):
        # exercise ---------------------
        subparser = RepackageCommand.add_command_parser_to(subparsers)
        args = parser.parse_args(repackage_argv_)
        # verify -----------------------
        assert args.dirpath == ARG_DIRPATH
        assert args.new_package == ARG_NEW_PACKAGE
        assert isinstance(subparser, argparse.ArgumentParser)

    def it_should_trigger_parser_error_if_dirpath_not_a_directory(
            self, args_, parser_):
        # fixture ----------------------
        args_.dirpath = 'foobar'
        repackage_command = RepackageCommand(parser_)
        # exercise ---------------------
        repackage_command.validate(args_)
        # verify -----------------------
        parser_.error.assert_called_once_with(ANY)
        assert 'DIRPATH' in parser_.error.call_args[0][0]
        assert 'foobar' in parser_.error.call_args[0][0]

    def it_can_dispatch_a_repackage_command_to_the_app(
            self, args_, app_controller_):
        # fixture ----------------------
        repackage_command = RepackageCommand(None)
        # exercise ---------------------
        repackage_command.execute(args_, app_controller_)
        # verify -----------------------
        app_controller_.repackage.assert_called_once_with(
            args_.dirpath, args_.new_package)


class DescribeSubstituteCommand(object):

    def it_should_add_a_substitute_command_parser(
            self, substitute_argv_, parser, subparsers):
        # exercise ---------------------
        subparser = SubstituteCommand.add_command_parser_to(subparsers)
        args = parser.parse_args(substitute_argv_)
        # verify -----------------------
        assert args.filename == ARG_FILENAME
        assert args.src_pkg_path == ARG_SRC_PKG_PATH
        assert args.tgt_pkg_path == ARG_TGT_PKG_PATH
        assert args.result_pkg_path == ARG_RESULT_PKG_PATH
        assert isinstance(subparser, argparse.ArgumentParser)

    @pytest.mark.parametrize(('src_pkg_path', 'tgt_pkg_path', 'err_frag'), [
        ('foobar', MINI_ZIP_PKG_PATH, 'SRC_PKG'),
        (MINI_ZIP_PKG_PATH, 'foobar', 'TGT_PKG'),
    ])
    def it_should_trigger_parser_error_if_pkg_path_does_not_exist(
            self, src_pkg_path, tgt_pkg_path, err_frag, args_, parser_):
        # fixture ----------------------
        args_.src_pkg_path = src_pkg_path
        args_.tgt_pkg_path = tgt_pkg_path
        substitute_command = SubstituteCommand(parser_)
        # exercise ---------------------
        substitute_command.validate(args_)
        # verify -----------------------
        parser_.error.assert_called_once_with(ANY)
        assert err_frag in parser_.error.call_args[0][0]
