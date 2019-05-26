"""Test suites for the primary entry point of the CLI."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pytest

from rpmvenv import cli


def test_python_cmd_build(
    request,
    python_source_code,
    python_config_file,
    tmpdir,
):
    """Test that a default build works without exception."""
    if not request.config.getvalue("python_git_url"):
        pytest.skip("No --python-git-url option was given")

    with pytest.raises(SystemExit) as exc_info:
        cli.main(
            (
                python_config_file,
                '--source', python_source_code,
                '--destination', str(tmpdir),
            )
        )
    rc = exc_info.value.code if type(exc_info.value) == SystemExit else \
        exc_info.value
    assert rc == 0
