"""Test fixtures and config data."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import shlex
import subprocess

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--git-url",
        help="Git URL for a package to test with.",
        required=True,
    )


def pytest_generate_tests(metafunc):
    if 'git_url' in metafunc.fixturenames:
        metafunc.parametrize('git_url', (metafunc.config.option.git_url,))


@pytest.fixture
def source_code(git_url, tmpdir):
    """Generate a source code directory and return the path."""
    cmd = 'git clone {0} {1}/'.format(git_url, str(tmpdir)).encode('ascii')
    subprocess.check_call(
        shlex.split(cmd),
    )
    # Strip off the '.git' and grap the last URL segment.
    pkg_name = git_url[:-4].split('/')[-1]
    return os.path.abspath(str(tmpdir.join(pkg_name)))


@pytest.fixture
def config_file():
    """Get a basic config file payload."""
    return {
        "name": "testpkg",
        "version": "1",
        "spec": {

        },
        "macros": {
            "pkg_name": "testpkg",
            "pkg_version": "1",
        },
    }
