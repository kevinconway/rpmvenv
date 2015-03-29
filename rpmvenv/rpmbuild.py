"""Functions for running the rpm build commands."""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import glob
import os
import shlex
import shutil
import subprocess
import sys
import tempfile


IGNORED_PATTERNS = (
    '*.pyc',
    '*.pyo',
    '*.pyd',
    '__pycache__',
)


class RpmProcessError(subprocess.CalledProcessError):

    """An exception thrown during the RPM build process.

    This exception extends the subprocess CalledProcessError to add standard
    out and standard error string fields.
    """

    def __init__(self, returncode, cmd, output=None, stdout=None, stderr=None):
        """Initialize the exception with process information."""
        super(RpmProcessError, self).__init__(returncode, cmd)
        self.output = output or ''
        self.stdout = stdout or ''
        self.stderr = stderr or ''


def topdir():
    """Get the absolute path to a valid rpmbuild %_topdir."""
    top = tempfile.mkdtemp(prefix='rpmvenv')
    os.makedirs(os.path.join(top, 'SOURCES'))
    os.makedirs(os.path.join(top, 'SPECS'))
    os.makedirs(os.path.join(top, 'BUILD'))
    os.makedirs(os.path.join(top, 'RPMS'))
    os.makedirs(os.path.join(top, 'SRPMS'))
    return top


def write_spec(top, spec):
    """Write a SPEC file to the SOURCES directory.

    Args:
        top: The absolute path to the %_topdir.
        spec: The contents of the SPEC file.

    Returns:
        The absolute path to the SPEC file.
    """
    path = os.path.join(top, 'SOURCES', 'package.spec')
    with open(path, 'w') as specfile:

        specfile.write(spec)

    return path


def copy_source(top, source, name=None):
    """Copy the source directory into the SOURCES directory.

    Args:
        top: The absolute path to the %_topdir.
        source: The absolute path to the source directory.
        name: The name of the directory to place in SOURCES.

    Returns:
        The absolute path to the copy.
    """
    name = name or os.path.basename(source)
    path = os.path.join(top, 'SOURCES', name)
    shutil.copytree(
        source,
        path,
        ignore=shutil.ignore_patterns(*IGNORED_PATTERNS),
    )
    return path


def verbose_popen(cmd):
    """Run a command with streaming output.

    Args:
        cmd (str): A command to run with popen.

    Raises:
        CalledProcessError: If the returncode is not 0.
    """
    proc = subprocess.Popen(shlex.split(cmd))
    proc.wait()
    if proc.returncode != 0:

        raise subprocess.CalledProcessError(
            returncode=proc.returncode,
            cmd=cmd,
        )


def quiet_popen(cmd):
    """Run a command with captured output.

    Args:
        cmd (str): A command to run with popen.

    Raises:
        RpmProcessError: If the returncode is not 0.
    """
    proc = subprocess.Popen(
        shlex.split(cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()
    if proc.returncode != 0:

        raise RpmProcessError(
            returncode=proc.returncode,
            cmd=cmd,
            output=err,
            stdout=out,
            stderr=err,
        )


def build(specfile, top=None, verbose=False):
    """Run rpmbuild with options.

    Args:
        specfile: The absolute path to the SPEC file to build.
        top: The %_topdir to use during the build. The default is a temporary
            directory which is automatically generated.
        verbose: Whether or not to stream the rpmbuild output in real time
            or only during errors.

    Returns:
        The absolute path to the new RPM.
    """
    top = top or topdir()
    cmd = "rpmbuild -ba --define='_topdir {0}' {1}".format(
        top,
        specfile,
    ).encode('ascii')
    # PY3 shlex only works with unicode strings. Convert as needed.
    if sys.version_info[0] > 2:

        cmd = cmd.decode('utf8')

    if not verbose:

        quiet_popen(cmd)

    else:

        verbose_popen(cmd)

    return glob.glob(os.path.join(top, 'RPMS', '**', '*.rpm')).pop()
