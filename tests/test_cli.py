"""Test suite for the `opcdiag.cli` module."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import argparse

import pytest

from opcdiag.cli import (
    BrowseCommand,
    Command,
    CommandController,
    DiffCommand,
    DiffItemCommand,
    ExtractCommand,
    RepackageCommand,
    SubstituteCommand,
    main,
)
from opcdiag.controller import OpcController

from .unitutil import ANY, FixtureRequest, Mock, class_mock, instance_mock, loose_mock, relpath

ARG_DIRPATH = "DIRPATH"
ARG_PKG_PATH = "PKG_PATH"
ARG_PKG_2_PATH = "PKG_2_PATH"
ARG_FILENAME = "FILENAME"
ARG_NEW_PACKAGE = "NEW_PACKAGE"
ARG_SRC_PKG_PATH = "SRC_PKG_PATH"
ARG_TGT_PKG_PATH = "TGT_PKG_PATH"
ARG_RESULT_PKG_PATH = "RESULT_PKG_PATH"
CMD_WORD_BROWSE = "browse"
CMD_WORD_DIFF = "diff"
CMD_WORD_DIFF_ITEM = "diff-item"
CMD_WORD_EXTRACT = "extract"
CMD_WORD_REPACKAGE = "repackage"
CMD_WORD_SUBSTITUTE = "substitute"
MINI_DIR_PKG_PATH = relpath("test-files/mini_pkg")
MINI_ZIP_PKG_PATH = relpath("test-files/mini_pkg.zip")


@pytest.fixture
def app_controller_(request: FixtureRequest):
    return instance_mock(OpcController, request)


@pytest.fixture
def args_(request: FixtureRequest, command_: Mock):
    args_ = loose_mock(request)
    args_.command = command_
    return args_


@pytest.fixture
def argv_(request: FixtureRequest):
    return instance_mock(list, request)


@pytest.fixture
def browse_argv_():
    return [CMD_WORD_BROWSE, ARG_PKG_PATH, ARG_FILENAME]


@pytest.fixture
def CommandController_(request: FixtureRequest, command_controller_: Mock):
    CommandController_ = class_mock("opcdiag.cli.CommandController", request)
    CommandController_.return_value = command_controller_
    CommandController_.new.return_value = command_controller_
    return CommandController_


@pytest.fixture
def Command_(request: FixtureRequest, command_cls_: Mock, parser_: Mock):
    Command_ = class_mock("opcdiag.cli.Command", request, autospec=False)
    Command_.__subclasses__ = Mock(return_value=[command_cls_])
    Command_.parser.return_value = parser_
    return Command_


@pytest.fixture
def command_(request: FixtureRequest):
    return instance_mock(Command, request)


@pytest.fixture
def command_cls_(request: FixtureRequest, command_: Mock, command_parser_: Mock):
    command_cls_ = loose_mock(request)
    command_cls_.return_value = command_
    command_cls_.add_command_parser_to.return_value = command_parser_
    return command_cls_


@pytest.fixture
def command_controller_(request: FixtureRequest):
    return instance_mock(CommandController, request)


@pytest.fixture
def command_parser_(request: FixtureRequest):
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
def OpcController_(request: FixtureRequest, app_controller_: Mock):
    OpcController_ = class_mock("opcdiag.cli.OpcController", request)
    OpcController_.return_value = app_controller_
    return OpcController_


@pytest.fixture
def parser():
    return argparse.ArgumentParser()


@pytest.fixture
def parser_(request: FixtureRequest, args_: Mock):
    parser_ = instance_mock(argparse.ArgumentParser, request)
    parser_.parse_args.return_value = args_
    return parser_


@pytest.fixture
def repackage_argv_():
    return [CMD_WORD_REPACKAGE, ARG_DIRPATH, ARG_NEW_PACKAGE]


@pytest.fixture
def subparsers(parser: argparse.ArgumentParser):
    return parser.add_subparsers()


@pytest.fixture
def substitute_argv_():
    return [
        CMD_WORD_SUBSTITUTE,
        ARG_FILENAME,
        ARG_SRC_PKG_PATH,
        ARG_TGT_PKG_PATH,
        ARG_RESULT_PKG_PATH,
    ]


class DescribeMain:
    def it_should_execute_the_command_in_argv(
        self, argv_: Mock, CommandController_: Mock, command_controller_: Mock
    ):
        # exercise ---------------------
        main(argv_)
        # verify -----------------------
        CommandController_.new.assert_called_once_with()
        command_controller_.execute.assert_called_once_with(argv_)


class DescribeCommandController:
    def it_can_be_constructed_with_its_factory_method(
        self,
        Command_: Mock,
        CommandController_: Mock,
        command_controller_: Mock,
        parser_: Mock,
        OpcController_: Mock,
        app_controller_: Mock,
    ):
        # exercise ---------------------
        command_controller = CommandController.new()
        # verify -----------------------
        Command_.parser.assert_called_once_with()
        OpcController_.assert_called_once_with()
        CommandController_.assert_called_once_with(parser_, app_controller_)
        assert command_controller is command_controller_

    def it_can_execute_a_command_in_argv_form(
        self, parser_: Mock, app_controller_: Mock, argv_: Mock, args_: Mock, command_: Mock
    ):
        # fixture ----------------------
        command_controller = CommandController(parser_, app_controller_)
        argv_.__len__.return_value = 2
        # exercise ---------------------
        command_controller.execute(argv_)
        # verify -----------------------
        command_.validate.assert_called_once_with(args_)
        command_.execute.assert_called_once_with(args_, app_controller_)


class DescribeBrowseCommand:
    def it_should_add_a_browse_command_parser(
        self,
        browse_argv_: Mock,
        parser: argparse.ArgumentParser,
        subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    ):
        # exercise ---------------------
        subparser = BrowseCommand.add_command_parser_to(subparsers)
        args = parser.parse_args(browse_argv_)
        # verify -----------------------
        assert args.pkg_path == ARG_PKG_PATH
        assert args.filename == ARG_FILENAME
        assert isinstance(subparser, argparse.ArgumentParser)

    def it_should_trigger_parser_error_if_pkg_path_does_not_exist(self, args_: Mock, parser_: Mock):
        # fixture ----------------------
        args_.pkg_path = "foobar"
        browse_command = BrowseCommand(parser_)
        # exercise ---------------------
        browse_command.validate(args_)
        # verify -----------------------
        parser_.error.assert_called_once_with(ANY)

    def it_can_dispatch_browse_command_to_app(
        self, args_: Mock, app_controller_: Mock, parser_: Mock
    ):
        # fixture ----------------------
        browse_command = BrowseCommand(parser_)
        # exercise ---------------------
        browse_command.execute(args_, app_controller_)
        # verify -----------------------
        app_controller_.browse.assert_called_once_with(args_.pkg_path, args_.filename)


class DescribeDiffCommand:
    def it_should_add_a_diff_command_parser(
        self,
        subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
        parser: argparse.ArgumentParser,
        diff_argv_: Mock,
    ):
        # exercise ---------------------
        subparser = DiffCommand.add_command_parser_to(subparsers)
        args = parser.parse_args(diff_argv_)
        # verify -----------------------
        assert args.pkg_1_path == ARG_PKG_PATH
        assert args.pkg_2_path == ARG_PKG_2_PATH
        assert isinstance(subparser, argparse.ArgumentParser)

    @pytest.mark.parametrize(
        ("pkg_1_path", "pkg_2_path", "err_frag"),
        [
            ("foobar", MINI_ZIP_PKG_PATH, "PKG_1"),
            (MINI_ZIP_PKG_PATH, "foobar", "PKG_2"),
        ],
    )
    def it_should_trigger_parser_error_if_pkg_path_does_not_exist(
        self, pkg_1_path: str, pkg_2_path: str, err_frag: str, args_: Mock, parser_: Mock
    ):
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
        self, args_: Mock, app_controller_: Mock, parser_: Mock
    ):
        # fixture ----------------------
        diff_command = DiffCommand(parser_)
        # exercise ---------------------
        diff_command.execute(args_, app_controller_)
        # verify -----------------------
        app_controller_.diff_pkg.assert_called_once_with(args_.pkg_1_path, args_.pkg_2_path)


class DescribeDiffItemCommand:
    def it_should_add_a_diff_item_command_parser(
        self,
        diff_item_argv_: Mock,
        parser: argparse.ArgumentParser,
        subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    ):
        # exercise ---------------------
        subparser = DiffItemCommand.add_command_parser_to(subparsers)
        args = parser.parse_args(diff_item_argv_)
        # verify -----------------------
        assert args.pkg_1_path == ARG_PKG_PATH
        assert args.pkg_2_path == ARG_PKG_2_PATH
        assert args.filename == ARG_FILENAME
        assert isinstance(subparser, argparse.ArgumentParser)

    @pytest.mark.parametrize(
        ("pkg_1_path", "pkg_2_path", "err_frag"),
        [
            ("foobar", MINI_ZIP_PKG_PATH, "PKG_1"),
            (MINI_ZIP_PKG_PATH, "foobar", "PKG_2"),
        ],
    )
    def it_should_trigger_parser_error_if_pkg_path_does_not_exist(
        self, pkg_1_path: str, pkg_2_path: str, err_frag: str, args_: Mock, parser_: Mock
    ):
        # fixture ----------------------
        args_.pkg_1_path = pkg_1_path
        args_.pkg_2_path = pkg_2_path
        diff_item_command = DiffItemCommand(parser_)
        # exercise ---------------------
        diff_item_command.validate(args_)
        # verify -----------------------
        parser_.error.assert_called_once_with(ANY)
        assert err_frag in parser_.error.call_args[0][0]

    def it_can_dispatch_diff_item_command_to_app(
        self, args_: Mock, app_controller_: Mock, parser_: Mock
    ):
        # fixture ----------------------
        diff_item_command = DiffItemCommand(parser_)
        # exercise ---------------------
        diff_item_command.execute(args_, app_controller_)
        # verify -----------------------
        app_controller_.diff_item.assert_called_once_with(
            args_.pkg_1_path, args_.pkg_2_path, args_.filename
        )


class DescribeExtractCommand:
    def it_should_add_a_extract_command_parser(
        self,
        extract_argv_: Mock,
        parser: argparse.ArgumentParser,
        subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    ):
        # exercise ---------------------
        subparser = ExtractCommand.add_command_parser_to(subparsers)
        args = parser.parse_args(extract_argv_)
        # verify -----------------------
        assert args.pkg_path == ARG_PKG_PATH
        assert args.dirpath == ARG_DIRPATH
        assert isinstance(subparser, argparse.ArgumentParser)

    def it_should_trigger_parser_error_if_pkg_path_does_not_exist(self, args_: Mock, parser_: Mock):
        # fixture ----------------------
        args_.pkg_path = "foobar"
        extract_command = ExtractCommand(parser_)
        # exercise ---------------------
        extract_command.validate(args_)
        # verify -----------------------
        parser_.error.assert_called_once_with(ANY)
        assert "PKG_PATH" in parser_.error.call_args[0][0]

    def it_can_dispatch_an_extract_command_to_the_app(
        self, args_: Mock, app_controller_: Mock, parser_: Mock
    ):
        # fixture ----------------------
        extract_command = ExtractCommand(parser_)
        # exercise ---------------------
        extract_command.execute(args_, app_controller_)
        # verify -----------------------
        app_controller_.extract_package.assert_called_once_with(args_.pkg_path, args_.dirpath)


class DescribeRepackageCommand:
    def it_should_add_a_repackage_command_parser(
        self,
        repackage_argv_: Mock,
        parser: argparse.ArgumentParser,
        subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    ):
        # exercise ---------------------
        subparser = RepackageCommand.add_command_parser_to(subparsers)
        args = parser.parse_args(repackage_argv_)
        # verify -----------------------
        assert args.dirpath == ARG_DIRPATH
        assert args.new_package == ARG_NEW_PACKAGE
        assert isinstance(subparser, argparse.ArgumentParser)

    def it_should_trigger_parser_error_if_dirpath_not_a_directory(self, args_: Mock, parser_: Mock):
        # fixture ----------------------
        args_.dirpath = "foobar"
        repackage_command = RepackageCommand(parser_)
        # exercise ---------------------
        repackage_command.validate(args_)
        # verify -----------------------
        parser_.error.assert_called_once_with(ANY)
        assert "DIRPATH" in parser_.error.call_args[0][0]
        assert "foobar" in parser_.error.call_args[0][0]

    def it_can_dispatch_a_repackage_command_to_the_app(
        self, args_: Mock, app_controller_: Mock, parser_: Mock
    ):
        # fixture ----------------------
        repackage_command = RepackageCommand(parser_)
        # exercise ---------------------
        repackage_command.execute(args_, app_controller_)
        # verify -----------------------
        app_controller_.repackage.assert_called_once_with(args_.dirpath, args_.new_package)


class DescribeSubstituteCommand:
    def it_should_add_a_substitute_command_parser(
        self,
        substitute_argv_: Mock,
        parser: argparse.ArgumentParser,
        subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    ):
        # exercise ---------------------
        subparser = SubstituteCommand.add_command_parser_to(subparsers)
        args = parser.parse_args(substitute_argv_)
        # verify -----------------------
        assert args.filename == ARG_FILENAME
        assert args.src_pkg_path == ARG_SRC_PKG_PATH
        assert args.tgt_pkg_path == ARG_TGT_PKG_PATH
        assert args.result_pkg_path == ARG_RESULT_PKG_PATH
        assert isinstance(subparser, argparse.ArgumentParser)

    @pytest.mark.parametrize(
        ("src_pkg_path", "tgt_pkg_path", "err_frag"),
        [
            ("foobar", MINI_ZIP_PKG_PATH, "SRC_PKG"),
            (MINI_ZIP_PKG_PATH, "foobar", "TGT_PKG"),
        ],
    )
    def it_should_trigger_parser_error_if_pkg_path_does_not_exist(
        self, src_pkg_path: str, tgt_pkg_path: str, err_frag: str, args_: Mock, parser_: Mock
    ):
        # fixture ----------------------
        args_.src_pkg_path = src_pkg_path
        args_.tgt_pkg_path = tgt_pkg_path
        substitute_command = SubstituteCommand(parser_)
        # exercise ---------------------
        substitute_command.validate(args_)
        # verify -----------------------
        parser_.error.assert_called_once_with(ANY)
        assert err_frag in parser_.error.call_args[0][0]

    def it_can_dispatch_a_substitute_command_to_the_app(
        self, args_: Mock, app_controller_: Mock, parser_: Mock
    ):
        # fixture ----------------------
        substitute_command = SubstituteCommand(parser_)
        # exercise ---------------------
        substitute_command.execute(args_, app_controller_)
        # verify -----------------------
        app_controller_.substitute.assert_called_once_with(
            args_.filename,
            args_.src_pkg_path,
            args_.tgt_pkg_path,
            args_.result_pkg_path,
        )
