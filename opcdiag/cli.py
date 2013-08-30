#!/usr/bin/env python
# encoding: utf-8

# opc.py
#
# Command-line interface for operations on one or more Open Packaging
# Convention (OPC) files, such as .docx, .pptx, and .xlsx files.


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

    def execute(self, argv=None):
        """
        Interpret the command indicated by the arguments in *argv* and
        execute it. If *argv* is |None|, ``sys.argv`` is used.
        """


def main(argv=None):
    command_controller = CommandController.new()
    command_controller.execute(argv)
