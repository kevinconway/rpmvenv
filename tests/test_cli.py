"""Test suites for the primary entry point of the CLI."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import tempfile

import pytest

from rpmvenv import cli

out_dir = None


@pytest.fixture(scope='function', autouse=True)
def create_tmpdir(request):
    global out_dir
    out_dir = tempfile.mkdtemp(suffix='rpmvenv')

    def delete_tmpdir():
        import shutil
        shutil.rmtree(out_dir)

    request.addfinalizer(delete_tmpdir)


@pytest.mark.skipif(
    not pytest.config.getvalue("python_git_url"),
    reason="No --python-git-url option was given",
)
def test_python_cmd_build(python_source_code, python_config_file):
    """Test that a default build works without exception."""
    with pytest.raises(SystemExit) as exc_info:
        cli.main((python_config_file,
                  '--source', python_source_code,
                  '--destination', out_dir,
                  ))
    rc = exc_info.value.code if type(exc_info.value) == SystemExit else \
        exc_info.value
    assert rc == 0
