# encoding: utf-8

"""
Acceptance test steps for opc-diag package
"""

import os
import shutil

from behave import given, then, when

from helpers import (
    assertManifestsMatch, assertPackagesMatch, OpcCommand, ref_pkg_path,
    scratch_path
)
from step_data import Manifest, _Manifest


SUBCMD_BROWSE = 'browse'
SUBCMD_DIFF = 'diff'
SUBCMD_DIFF_ITEM = 'diff-item'
SUBCMD_EXTRACT = 'extract'
SUBCMD_REPACKAGE = 'repackage'
SUBCMD_SUBSTITUTE = 'substitute'
URI_CONTENT_TYPES = '[Content_Types].xml'
URI_CORE_PROPS = 'docProps/core.xml'
URI_PKG_RELS = '_rels/.rels'
URI_SLIDE_MASTER = 'ppt/slideMasters/slideMaster1.xml'


# commonly used paths ------------------
base_dir_pkg_path = ref_pkg_path('source')
base_zip_pkg_path = ref_pkg_path('base.pptx')
pkg_paths = {'dir': base_dir_pkg_path, 'zip': base_zip_pkg_path}

base_pkg_path = ref_pkg_path('base.pptx')
changed_pkg_path = ref_pkg_path('changed.pptx')
expanded_dir = ref_pkg_path('source')
extract_dir = scratch_path('extracted')
scratch_pkg_path = scratch_path('test_out.pptx')


# given ====================================================

@given('a target directory that does not exist')
def step_remove_target_directory(context):
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)


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


@when('I issue a command to diff the package rels between two packages')
def step_command_diff_pkg_rels_item(context):
    context.cmd = OpcCommand(
        SUBCMD_DIFF_ITEM, base_pkg_path, changed_pkg_path, URI_PKG_RELS
    ).execute()


@when('I issue a command to diff the slide master between two packages')
def step_command_diff_slide_master(context):
    context.cmd = OpcCommand(
        SUBCMD_DIFF_ITEM, base_pkg_path, changed_pkg_path, URI_SLIDE_MASTER
    ).execute()


@when('I issue a command to diff two packages')
def step_command_diff_two_packages(context):
    context.cmd = OpcCommand(
        SUBCMD_DIFF, base_pkg_path, changed_pkg_path
    ).execute()


@when('I issue a command to extract a package')
def step_command_extract_package(context):
    context.cmd = OpcCommand(
        SUBCMD_EXTRACT, base_pkg_path, extract_dir
    ).execute()


@when('I issue a command to repackage an expanded package directory')
def step_command_repackage_expanded_pkg_dir(context):
    context.cmd = OpcCommand(
        SUBCMD_REPACKAGE, expanded_dir, scratch_pkg_path
    ).execute()


@when('I issue a command to substitute a package item')
def step_command_substitute_pkg_item(context):
    context.cmd = OpcCommand(
        SUBCMD_SUBSTITUTE, URI_SLIDE_MASTER, changed_pkg_path, base_pkg_path,
        scratch_pkg_path
    ).execute()


# then =====================================================

@then('a zip package with matching contents appears at the path I specified')
def step_then_matching_zip_pkg_appears_at_specified_path(context):
    context.cmd.assert_stderr_empty()
    context.cmd.assert_stdout_empty()
    assertPackagesMatch(expanded_dir, scratch_pkg_path)


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


@then('the package diff appears on stdout')
def step_then_pkg_diff_appears_on_stdout(context):
    context.cmd.assert_stderr_empty()
    context.cmd.assert_stdout_matches('diff.txt')


@then('the package items appear in the target directory')
def step_then_pkg_appears_in_target_dir(context):
    context.cmd.assert_stderr_empty()
    context.cmd.assert_stdout_empty()
    actual_manifest = Manifest(extract_dir)
    expected_sha1_list = [
        ('b7377d13b945fd27216d02d50277a350c8c4aea6',
         '[Content_Types].xml'),
        ('11a0facc96d560bf07b4691f0526b09229264e20',
         '_rels/.rels'),
        ('c1ae3715531e49808610f18c4810704f70be3767',
         'docProps/app.xml'),
        ('775edccda43956b1e55c8fe668ba817934ee17c8',
         'docProps/core.xml'),
        ('585be5da0832f70b4e71f66f5784cc8acbcc8e88',
         'docProps/thumbnail.jpeg'),
        ('85ff3c93403fee9d07d1f52b08e03e1ad8614343',
         'ppt/_rels/presentation.xml.rels'),
        ('21bbd2e84efc65591a76e8a7811c79ce65a7f389',
         'ppt/presProps.xml'),
        ('8281415d72c1f9f43e2e0b1cdc4a346e7a0545b3',
         'ppt/presentation.xml'),
        ('b0feb4cc107c9b2d135b1940560cf8f045ffb746',
         'ppt/printerSettings/printerSettings1.bin'),
        ('fbccb1d0db1ad72bea6b96449d5033ee7ad3ee3c',
         'ppt/slideLayouts/_rels/slideLayout1.xml.rels'),
        ('fbccb1d0db1ad72bea6b96449d5033ee7ad3ee3c',
         'ppt/slideLayouts/_rels/slideLayout10.xml.rels'),
        ('fbccb1d0db1ad72bea6b96449d5033ee7ad3ee3c',
         'ppt/slideLayouts/_rels/slideLayout11.xml.rels'),
        ('fbccb1d0db1ad72bea6b96449d5033ee7ad3ee3c',
         'ppt/slideLayouts/_rels/slideLayout2.xml.rels'),
        ('fbccb1d0db1ad72bea6b96449d5033ee7ad3ee3c',
         'ppt/slideLayouts/_rels/slideLayout3.xml.rels'),
        ('fbccb1d0db1ad72bea6b96449d5033ee7ad3ee3c',
         'ppt/slideLayouts/_rels/slideLayout4.xml.rels'),
        ('fbccb1d0db1ad72bea6b96449d5033ee7ad3ee3c',
         'ppt/slideLayouts/_rels/slideLayout5.xml.rels'),
        ('fbccb1d0db1ad72bea6b96449d5033ee7ad3ee3c',
         'ppt/slideLayouts/_rels/slideLayout6.xml.rels'),
        ('fbccb1d0db1ad72bea6b96449d5033ee7ad3ee3c',
         'ppt/slideLayouts/_rels/slideLayout7.xml.rels'),
        ('fbccb1d0db1ad72bea6b96449d5033ee7ad3ee3c',
         'ppt/slideLayouts/_rels/slideLayout8.xml.rels'),
        ('fbccb1d0db1ad72bea6b96449d5033ee7ad3ee3c',
         'ppt/slideLayouts/_rels/slideLayout9.xml.rels'),
        ('ec99dfcf6812f8bd0c9e0a2363d38301e8104803',
         'ppt/slideLayouts/slideLayout1.xml'),
        ('8fa04dcb314de8c2321eaec153e6b85263c52fd8',
         'ppt/slideLayouts/slideLayout10.xml'),
        ('7531300ef5c76a217f330d3748c82ce484bcb037',
         'ppt/slideLayouts/slideLayout11.xml'),
        ('7fba92ff7c76a5050fd9c0acbbdc98600def0264',
         'ppt/slideLayouts/slideLayout2.xml'),
        ('ca2c475ce40be637eb271846fbcee05121d61054',
         'ppt/slideLayouts/slideLayout3.xml'),
        ('4ceb2a6391cc08f6883515ecfb117dfe6733daae',
         'ppt/slideLayouts/slideLayout4.xml'),
        ('4764ea1d5afd93497b4e3bf665cd5b09f6684f62',
         'ppt/slideLayouts/slideLayout5.xml'),
        ('3768f6b561eecdfb4530c6a2a939ed4e822f07f5',
         'ppt/slideLayouts/slideLayout6.xml'),
        ('ef830f1b546e799c3ae5a8c3df399d5e3346e70a',
         'ppt/slideLayouts/slideLayout7.xml'),
        ('749ba47dc5497c6bd0d8b0b034e648e47c336491',
         'ppt/slideLayouts/slideLayout8.xml'),
        ('d49c31a3ba055792ca9dd779bb8897795aa46fff',
         'ppt/slideLayouts/slideLayout9.xml'),
        ('4b0a95fbb9e8680c1e766d0ab7080bd854a3f7bc',
         'ppt/slideMasters/_rels/slideMaster1.xml.rels'),
        ('477117c4c1f2189edcfd35a194103bf4fc1245d5',
         'ppt/slideMasters/slideMaster1.xml'),
        ('27bb16052608af395a606ce1de16239bef2d86c3',
         'ppt/tableStyles.xml'),
        ('ea60a5ff9290d9ec08a1546fc38945afb3057226',
         'ppt/theme/theme1.xml'),
        ('5df90b0fdcd12c199b36ae1cd36e7541ab14ed90',
         'ppt/viewProps.xml'),
    ]
    expected_manifest = _Manifest(expected_sha1_list)
    assertManifestsMatch(
        actual_manifest, expected_manifest, 'actual', 'expected'
    )


@then('the package rels diff appears on stdout')
def step_then_pkg_rels_diff_appears_on_stdout(context):
    context.cmd.assert_stderr_empty()
    context.cmd.assert_stdout_matches('diff-item.pkg_rels.txt')


@then('the resulting package contains the substituted item')
def step_then_resulting_pkg_contains_substituted_item(context):
    context.cmd.assert_stderr_empty()
    context.cmd.assert_stdout_matches('substitute.txt')
    subst_sha = Manifest(changed_pkg_path)[URI_SLIDE_MASTER]
    expected_manifest = Manifest(base_pkg_path)
    expected_manifest[URI_SLIDE_MASTER] = subst_sha
    actual_manifest = Manifest(scratch_pkg_path)
    assertManifestsMatch(
        actual_manifest, expected_manifest, 'actual', 'expected')


@then('the slide master diff appears on stdout')
def step_then_slide_master_diff_appears_on_stdout(context):
    context.cmd.assert_stderr_empty()
    context.cmd.assert_stdout_matches('diff-item.slide_master.txt')
