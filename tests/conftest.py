"""Test fixtures and config data."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import json
import os
import shlex
import subprocess
import sys

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--python-git-url",
        help="Git URL for a Python package to test with.",
        default="https://github.com/kevinconway/rpmvenv.git",
    )
    parser.addoption(
        "--python_ver",
        help="Python version to use in the test.",
        default="python3.9",
    )
    parser.addoption(
        "--skip-binary-strip",
        action="store_true",
        default=False,
        help="Skip the binary strip setp and use the QA_SKIP_BUILD_ROOT.",
    )


def pytest_generate_tests(metafunc):
    if "python_git_url" in metafunc.fixturenames:
        metafunc.parametrize(
            "python_git_url", (metafunc.config.option.python_git_url,)
        )

    if "python" in metafunc.fixturenames:
        metafunc.parametrize("python", (metafunc.config.option.python_ver,))

    if "skip_binary_strip" in metafunc.fixturenames:
        metafunc.parametrize(
            "skip_binary_strip", (metafunc.config.option.skip_binary_strip,)
        )

    if "use_pip_install" in metafunc.fixturenames:
        metafunc.parametrize("use_pip_install", (True, False))

    if "remove_pycache" in metafunc.fixturenames:
        metafunc.parametrize("remove_pycache", (True, False))


@pytest.fixture
def python_source_code(python_git_url, tmpdir):
    """Generate a source code directory and return the path."""
    # Strip off the '.git' and grap the last URL segment.
    pkg_name = python_git_url[:-4].split("/")[-1]
    cmd = "git clone {0} {1}/{2}".format(
        python_git_url,
        str(tmpdir),
        pkg_name,
    ).encode("ascii")
    if sys.version_info[0] > 2:

        cmd = cmd.decode("utf8")

    subprocess.check_call(
        shlex.split(cmd),
    )
    return os.path.abspath(str(tmpdir.join(pkg_name)))


@pytest.fixture(autouse=True)
def qa_skip_buildroot(skip_binary_strip):
    if skip_binary_strip:

        os.environ["QA_SKIP_BUILD_ROOT"] = "1"

    elif "QA_SKIP_BUILD_ROOT" in os.environ:

        os.environ.pop("QA_SKIP_BUILD_ROOT")


@pytest.fixture
def python_config_file(
    python, skip_binary_strip, use_pip_install, remove_pycache, tmpdir
):
    """Get a config file path."""
    extra_filename = "README.rst"
    json_file = str(tmpdir.join("conf.json"))
    config_body = {
        "extensions": {
            "enabled": [
                "description_text",
                "python_venv",
                "file_permissions",
                "file_extras",
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
        "file_extras": {
            "files": [
                extra_filename + ":opt/test-pkg/" + extra_filename + "1",
                {
                    "src": extra_filename,
                    "dest": "opt/test-pkg/" + extra_filename + "2",
                },
                {
                    "src": extra_filename,
                    "dest": "opt/test-pkg/" + extra_filename + "3",
                    "config": True,
                },
                {
                    "src": extra_filename,
                    "dest": "opt/test-pkg/" + extra_filename + "4",
                    "config": "noreplace",
                },
                {
                    "src": extra_filename,
                    "dest": "opt/test-pkg/" + extra_filename + "5",
                    "doc": True,
                },
                {
                    "src": extra_filename,
                    "dest": "opt/test-pkg/" + extra_filename + "6",
                    "doc": False,
                    "config": False,
                },
            ]
        },
        "python_venv": {
            "cmd": "virtualenv",
            "name": "test-pkg-venv",
            "path": "/usr/share/python",
            "python": python,
            "strip_binaries": not skip_binary_strip,
            "use_pip_install": use_pip_install,
            "remove_pycache": remove_pycache,
        },
        "blocks": {
            "post": ("echo 'Hello'",),
            "desc": ("test pkg description",),
        },
    }
    with open(json_file, "w") as conf_file:

        conf_file.write(json.dumps(config_body))

    return json_file
