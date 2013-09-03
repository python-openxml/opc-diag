#!/usr/bin/env python
# encoding: utf-8

# opc.py
#
# Command-line interface for operations on one or more Open Packaging
# Convention (OPC) files, such as .docx, .pptx, and .xlsx files.

from opcdiag.controller import OpcController


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

    def execute(self, args, app_controller):
        """
        Abstract method, each command must implement
        """

    def validate(self, args):
        """
        Abstract method, each command must implement; just pass if there's
        nothing to validate.
        """


def main(argv=None):
    command_controller = CommandController.new()
    command_controller.execute(argv)
