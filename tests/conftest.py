"""Test fixtures and config data."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import json
import os
import shlex
import subprocess

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--python-git-url",
        help="Git URL for a Python package to test with.",
        default="https://github.com/kevinconway/rpmvenv.git",
    )
    parser.addoption(
        "--python",
        help="Python version to use in the test.",
        default="python2.7",
    )


def pytest_generate_tests(metafunc):
    if 'python_git_url' in metafunc.fixturenames:
        metafunc.parametrize(
            'python_git_url',
            (metafunc.config.option.python_git_url,)
        )

    if 'python' in metafunc.fixturenames:
        metafunc.parametrize('python', (metafunc.config.option.python,))


@pytest.fixture
def python_source_code(python_git_url, tmpdir):
    """Generate a source code directory and return the path."""
    # Strip off the '.git' and grap the last URL segment.
    pkg_name = python_git_url[:-4].split('/')[-1]
    cmd = 'git clone {0} {1}/{2}'.format(
        python_git_url,
        str(tmpdir),
        pkg_name,
    ).encode('ascii')
    subprocess.check_call(
        shlex.split(cmd),
    )
    return os.path.abspath(str(tmpdir.join(pkg_name)))


@pytest.fixture
def python_config_file(python, tmpdir):
    """Get a config file path."""
    json_file = str(tmpdir.join('conf.json'))
    config_body = {
        "extensions": {
            "enabled": [
                "description_text",
                "python_venv",
                "file_permissions",
                "blocks",
            ],
        },
        "core": {
            "group": "Application/System",
            "license": "Apache2",
            "name": "test-pkg",
            "release": "1",
            "source": "test-pkg",
            "summary": "test pkg for testing",
            "version": "1.2.3.4",
        },
        "file_permissions": {
            "group": "vagrant",
            "user": "vagrant",
        },
        "python_venv": {
            "cmd": "virtualenv",
            "name": "test-pkg-venv",
            "path": "/usr/share/python",
            "python": python,
        },
        "blocks": {
            "post": ("echo 'Hello'",),
            "desc": ("test pkg description",),
        }
    }
    with open(json_file, 'w') as conf_file:

        conf_file.write(json.dumps(config_body))

    return json_file
