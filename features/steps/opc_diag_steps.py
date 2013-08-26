# -*- coding: utf-8 -*-
#
# opc_diag_steps.py
#
# Copyright (C) 2012, 2013 Steve Canny scanny@cisco.com
#
# This module is part of opc-diag and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Acceptance test steps for opc-diag package."""

from behave import then, when

from helpers import OpcCommand, ref_pkg_path


SUBCMD_BROWSE = 'browse'
URI_CONTENT_TYPES = '[Content_Types].xml'


# commonly used paths ------------------
base_pkg_path = ref_pkg_path('base.pptx')


# when =====================================================

@when('I issue a command to browse the content types of a package')
def step_issue_command_to_browse_content_types(context):
    context.cmd = OpcCommand(SUBCMD_BROWSE, base_pkg_path,
                             URI_CONTENT_TYPES).execute()


# then =====================================================

@then('the formatted content types item appears on stdout')
def step_then_content_types_appear_on_stdout(context):
    context.cmd.assert_stderr_empty()
    context.cmd.assert_stdout_matches('browse.content_types.txt')
