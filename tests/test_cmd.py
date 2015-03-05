"""Test suites for the primary entry point of the CLI."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from rpmvenv import cmd


def test_cmd_build(source_code, config_file):
    """Test that a default build works without exception."""
    pkg = cmd.build(source_code, config_file)
    assert config_file['macros']['pkg_rpm_name'] in pkg
