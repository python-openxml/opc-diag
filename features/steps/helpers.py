# -*- coding: utf-8 -*-
#
# helpers.py
#
# Copyright (C) 2012, 2013 Steve Canny scanny@cisco.com
#
# This module is part of opc-diag and is released under the MIT License:
# http://www.opensource.org/licenses/mit-license.php

"""Acceptance test helpers."""

from __future__ import unicode_literals

import os
import subprocess

from step_data import Manifest


def absjoin(*paths):
    return os.path.abspath(os.path.join(*paths))


def ref_pkg_path(filename):
    ref_pkg_dir = absjoin(test_file_dir, 'reference_pkgs')
    return os.path.relpath(absjoin(ref_pkg_dir, filename))


def scratch_path(name):
    return os.path.relpath(absjoin(scratch_dir, name))


thisdir = os.path.split(__file__)[0]
scratch_dir = absjoin(thisdir, '../_scratch')
test_file_dir = absjoin(thisdir, '../test_files')


def assertPackagesMatch(path1, path2):
    """
    Raise |AssertionError| if manifest of package at *path1* does not exactly
    match that of package at *path2*.
    """
    manifest1, manifest2 = Manifest(path1), Manifest(path2)
    msg = ("Package manifests don't match\n\n%s" %
           manifest1.diff(manifest2, path1, path2))
    assert manifest1 == manifest2, msg


class OpcCommand(object):
    """
    Executes opc-diag command as configured and makes results available.
    """
    def __init__(self, subcommand, *args):
        self.subcommand = subcommand
        self.args = args

    def assert_stderr_empty(self):
        """
        Raise AssertionError if any output was captured on stderr and display
        the captured output.
        """
        tmpl = "Unexpected output on stderr\n'%s'\n"
        assert self.std_err == '', tmpl % self.std_err

    def assert_stdout_empty(self):
        """
        Raise AssertionError if any output was captured on stdout and display
        the captured output.
        """
        tmpl = "Unexpected output on stdout\n'%s'\n"
        assert self.std_out == '', tmpl % self.std_out

    def assert_stdout_matches(self, filename):
        """
        Raise AssertionError with helpful diagnostic message if output
        captured on stdout doesn't match contents of file identified by
        *filename* in known directory.
        """
        expected_stdout = self._expected_output(filename)
        msg = ("\n\nexpected output:\n'%s'\n\nactual output:\n'%s'" %
               (expected_stdout, self.std_out))
        std_out = self.std_out.replace('\r\n', '\n')  # normalize line endings
        assert std_out == expected_stdout, msg

    def execute(self):
        """
        Execute the configured command in a subprocess and capture the
        results.
        """
        args = ['python', 'opc-stub']
        args.append(self.subcommand)
        args.extend(self.args)
        self.proc = subprocess.Popen(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        std_out_bytes, std_err_bytes = self.proc.communicate()
        self.std_out = std_out_bytes.decode('utf-8')
        self.std_err = std_err_bytes.decode('utf-8')
        return self

    @staticmethod
    def _expected_output(filename):
        """
        Return contents of file with *filename* in known directory as text.
        """
        path = absjoin(test_file_dir, 'expected_output', filename)
        with open(path, 'rb') as f:
            expected_bytes = f.read()
        expected_text = expected_bytes.decode('utf-8')
        return expected_text
