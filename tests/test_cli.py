"""Test suites for the primary entry point of the CLI."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pytest

from rpmvenv import cli


@pytest.mark.skipif(
    not pytest.config.getvalue("python_git_url"),
    reason="No --python-git-url option was given",
)
def test_python_cmd_build(python_source_code, python_config_file):
    """Test that a default build works without exception."""
    with pytest.raises(SystemExit) as exc_info:
        cli.main((python_config_file, '--source', python_source_code))
    assert exc_info.value == 0
