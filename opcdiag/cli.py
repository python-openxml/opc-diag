#!/usr/bin/env python
# encoding: utf-8

# opc.py
#
# Command-line interface for operations on one or more Open Packaging
# Convention (OPC) files, such as .docx, .pptx, and .xlsx files.

import argparse
import os


from opcdiag.controller import OpcController


SUBCMD_HELP = "!!! this is the sub-command help string I haven't written yet"


class CommandController(object):
    """
    Orchestrates processing of commands in the form of a list of arguments
    (*argv*). A new instance is created using the :meth:`new` staticmethod.
    Once instantiated, it can process any number of commands by calling its
    :meth:`execute` method, once for each command.
    """
    def __init__(self, parser, app_controller):
        self._parser = parser
        self._app_controller = app_controller

    @staticmethod
    def new():
        """
        Return a newly created instance of |CommandController| fitted with a
        fully configured parser and an instance of the application controller
        to dispatch parsed commands to.
        """
        parser = Command.parser()
        app_controller = OpcController()
        return CommandController(parser, app_controller)

    def execute(self, argv=None):
        """
        Interpret the command indicated by the arguments in *argv* and
        execute it. If *argv* is |None|, ``sys.argv`` is used.
        """
        args = self._parser.parse_args(argv)
        command = args.command
        command.validate(args)
        command.execute(args, self._app_controller)


class Command(object):
    """
    Base class for sub-commands
    """
    def __init__(self, parser):
        super(Command, self).__init__()
        self._parser = parser

    @staticmethod
    def parser():
        """
        Return an instance of :class:`argparse.ArgumentParser` configured
        with a subcommand parser for each of the commands that are a subclass
        of |Command|.
        """
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(help=SUBCMD_HELP)
        for command_cls in Command.__subclasses__():
            command_parser = command_cls.add_command_parser_to(subparsers)
            command = command_cls(command_parser)
            command_parser.set_defaults(command=command)
        return parser

    def execute(self, args, app_controller):
        """
        Abstract method, each command must implement
        """
        msg = 'execute() must be implemented by all subclasses of Command'
        raise NotImplementedError(msg)

    def validate(self, args):
        """
        Abstract method, each command must implement; just pass if there's
        nothing to validate.
        """
        msg = 'validate() must be implemented by all subclasses of Command'
        raise NotImplementedError(msg)


class BrowseCommand(Command):

    def __init__(self, parser):
        super(BrowseCommand, self).__init__(parser)

    @staticmethod
    def add_command_parser_to(subparsers):
        parser = subparsers.add_parser(
            'browse',
            help='List pretty-printed XML for a specified package part')
        parser.add_argument(
            'pkg_path', metavar='PKG_PATH',
            help='Path to OPC package file')
        parser.add_argument(
            'filename', metavar='FILENAME',
            help='Filename portion of the pack URI for the part to browse')
        return parser

    def execute(self, args, app_controller):
        app_controller.browse(args.pkg_path, args.filename)

    def validate(self, args):
        try:
            msg = "PKG_PATH '%s' does not exist" % args.pkg_path
            assert os.path.exists(args.pkg_path), msg
        except AssertionError as e:
            self._parser.error(str(e))


class DiffItemCommand(Command):

    def __init__(self, parser):
        super(DiffItemCommand, self).__init__(parser)

    @staticmethod
    def add_command_parser_to(subparsers):
        parser = subparsers.add_parser(
            'diff-item',
            help='Show differences between a specified item in two OPC '
                 'package files')
        parser.add_argument(
            'pkg_1_path', metavar='PKG_1_PATH',
            help='first package')
        parser.add_argument(
            'pkg_2_path', metavar='PKG_2_PATH',
            help='second package')
        parser.add_argument(
            'filename', metavar='FILENAME',
            help='Filename portion of pack URI for item to browse')
        return parser

    def validate(self, args):
        paths_that_should_exist = (
            (args.pkg_1_path, 'PKG_1_PATH'),
            (args.pkg_2_path, 'PKG_2_PATH'),
        )
        try:
            for path, metavar in paths_that_should_exist:
                msg = "%s '%s' does not exist" % (metavar, path)
                assert os.path.exists(path), msg
        except AssertionError as e:
            self._parser.error(str(e))


def main(argv=None):
    command_controller = CommandController.new()
    command_controller.execute(argv)
