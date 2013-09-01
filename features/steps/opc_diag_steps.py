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
SUBCMD_DIFF_ITEM = 'diff-item'
URI_CONTENT_TYPES = '[Content_Types].xml'
URI_CORE_PROPS = 'docProps/core.xml'
URI_PKG_RELS = '_rels/.rels'


# commonly used paths ------------------
base_dir_pkg_path = ref_pkg_path('source')
base_zip_pkg_path = ref_pkg_path('base.pptx')
pkg_paths = {'dir': base_dir_pkg_path, 'zip': base_zip_pkg_path}

base_pkg_path = ref_pkg_path('base.pptx')
changed_pkg_path = ref_pkg_path('changed.pptx')


# when =====================================================

@when('I issue a command to browse an XML part in a {pkg_type} package')
def step_issue_command_to_browse_pkg_part(context, pkg_type):
    context.cmd = OpcCommand(SUBCMD_BROWSE, pkg_paths[pkg_type],
                             URI_CORE_PROPS).execute()


@when('I issue a command to browse the content types of a {pkg_type} package')
def step_issue_command_to_browse_content_types(context, pkg_type):
    context.cmd = OpcCommand(SUBCMD_BROWSE, pkg_paths[pkg_type],
                             URI_CONTENT_TYPES).execute()


@when('I issue a command to browse the package rels of a {pkg_type} package')
def step_issue_command_to_browse_pkg_rels(context, pkg_type):
    context.cmd = OpcCommand(SUBCMD_BROWSE, pkg_paths[pkg_type],
                             URI_PKG_RELS).execute()


@when('I issue a command to diff the content types between two packages')
def step_command_diff_content_types(context):
    context.cmd = OpcCommand(
        SUBCMD_DIFF_ITEM, base_pkg_path, changed_pkg_path, URI_CONTENT_TYPES
    ).execute()


# then =====================================================

@then('the content types diff appears on stdout')
def step_then_content_types_diff_appears_on_stdout(context):
    context.cmd.assert_stderr_empty()
    context.cmd.assert_stdout_matches('diff-item.content_types.txt')


@then('the formatted content types item appears on stdout')
def step_then_content_types_appear_on_stdout(context):
    context.cmd.assert_stderr_empty()
    context.cmd.assert_stdout_matches('browse.content_types.txt')


@then('the formatted package part XML appears on stdout')
def step_then_pkg_part_xml_appears_on_stdout(context):
    context.cmd.assert_stderr_empty()
    context.cmd.assert_stdout_matches('browse.core_props.txt')


@then('the formatted package rels XML appears on stdout')
def step_then_pkg_rels_xml_appears_on_stdout(context):
    context.cmd.assert_stderr_empty()
    context.cmd.assert_stdout_matches('browse.pkg_rels.txt')
