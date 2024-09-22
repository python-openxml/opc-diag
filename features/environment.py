"""Used by behave to set testing environment before and after running acceptance tests."""

import os

from behave.runner import Context

scratch_dir = os.path.abspath(os.path.join(os.path.split(__file__)[0], "_scratch"))


def before_all(context: Context):
    if not os.path.isdir(scratch_dir):
        os.mkdir(scratch_dir)
