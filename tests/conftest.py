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
    parser.addoption(
        "--python",
        help="Python version to use in the test.",
        default="python2.7",
    )


def pytest_generate_tests(metafunc):
    if 'git_url' in metafunc.fixturenames:
        metafunc.parametrize('git_url', (metafunc.config.option.git_url,))

    if 'python' in metafunc.fixturenames:
        metafunc.parametrize('python', (metafunc.config.option.python,))


@pytest.fixture
def source_code(git_url, tmpdir):
    """Generate a source code directory and return the path."""
    # Strip off the '.git' and grap the last URL segment.
    pkg_name = git_url[:-4].split('/')[-1]
    cmd = 'git clone {0} {1}/{2}'.format(
        git_url,
        str(tmpdir),
        pkg_name,
    ).encode('ascii')
    subprocess.check_call(
        shlex.split(cmd),
    )
    return os.path.abspath(str(tmpdir.join(pkg_name)))


@pytest.fixture
def config_file(python):
    """Get a basic config file payload."""
    return {
        "name": "testpkg",
        "version": "1",
        "spec": {
            "python": python,
        },
        "macros": {
            "pkg_name": "testpkg",
            "pkg_rpm_name": "testpkg-rpm-name",
            "pkg_version": "1",
        },
    }
