=======
rpmvenv
=======

*RPM package helper which support packaging Python virtual environments.*

-   `Basic Usage <#basic-usage>`_

-   `Customizing <#customizing>`_

    -   `Core <#core>`_

    -   `Blocks <#blocks>`_

    -   `File Permissions <#file-permissions>`_

    -   `Additional Files <#additional-files>`_

    -   `Python Virtualenv <#python-virtualenv>`_

    -   `CLI Flags And Environment Variables <#cli-flags-and-environment-variables>`_

    -   `Additional Options <#additional-options>`_

-   `NOTE: manylinux <#note-manylinux>`_

-   `NOTE: unicode <#note-unicode>`_

-   `NOTE: system python <#note-system-python>`_

-   `NOTE: bdist eggs with scripts <#note-bdist-eggs-with-scripts>`_

-   `Testing <#testing>`_

-   `License <#license>`_

-   `Contributing <#contributing>`_

Basic Usage
===========

In order to package a Python project in an RPM containing a virtualenv drop
a file in your repository root with a '.json' extensions and the following
content. Change the values where appropriate.

.. code-block:: javascript

    {
        "extensions": {
            "enabled": [
                "python_venv",
                "blocks"
            ]
        },
        "core": {
            "group": "Application/System",
            "license": "MIT",
            "name": "some-rpm-package-name",
            "summary": "short package summary",
            "version": "1.2.3"
        },
        "python_venv": {
            "name": "name_of_venv_dir_to_create",
            "path": "/path/where/to/install/venv"
        },
        "blocks": {
            "desc": [
                "some long package description",
                "each array element is a new line"
            ]
        }
    }

Make sure `rpmbuild <http://www.rpm.org>`_ is installed.
With the configuration file in place run the command line tool installed with
the package to generate the RPM.

.. code-block:: shell

    rpmvenv path/to/the/config.json

This will generate a new RPM and place it in your current working directory.

Customizing
===========

While the above example will generate an installable RPM it has limitations.
For example, it does not set the user/group ownership of the packaged files,
it does not include non-Python files such as init scripts, and it does not
perform any post install actions. This project uses a plugin system for adding
and enabling extra functionality. For convenience, some features ship with the
project already.

Core
----

The 'core' extension is always enabled. This extension provides the options
for interacting with all the required RPM SPEC file tags like "Version" or
"Url". Current core options:

.. code-block:: javascript

    {"core":{
        // The name of the RPM file which is generated.
        "name": "some-pkg-name",
        // The RPM version to build.
        "version": "1.2.3",
        // The release number for the RPM. Default is 1.
        "release": "1",
        // The short package summary.
        "summary": "a package for code",
        // The RPM package group in which this package belongs.
        "group": "Application/System",
        // The license under which the package is distributed.
        "license": "MIT",
        // The URL of the package source.
        "url": "https://projectsite.com",
        // The path to the package source. Defaults to the parent of the config.
        "source": "/path/to/my/source",
        // The name of the buildroot directory to use. Default is random temp dir.
        "buildroot": "%(mktemp -ud %{_tmppath}/%{SOURCE0}-%{version}-%{release}-XXXXXX)",
        // System dependencies.
        "requires": [],
        // Conflicting packages.
        "conflicts": [],
        // Packages to mark as obsolete.
        "obsoletes": [],
        // Virtual packages satisfied by this RPM.
        "provides": []
    }}

Blocks
------

RPM files contain several sections, or blocks, which can contain multi-line
content. Most blocks contain shell code used to build and install a project.
This extension is enabled by adding 'blocks' to the list of enabled extensions.
Each block configuration item is a list of strings. Each string represents a
line in the body of the block.

.. code-block:: javascript

    {"blocks" {
        // Shell to execute on post-install.
        "post": [],
        // Shell to execute on post-uninstall.
        "postun": [],
        // Shell to execute on pre-install.
        "pre": [],
        // Shell to execute on pre-uninstall.
        "preun": [],
        // Shell to execute during the prep phase.
        "prep": [],
        // Shell to execute during the build phase.
        "build": [],
        // Shell to execute during the install phase.
        "install": [],
        // Shell to execute during the clean phase.
        "clean": [],
        // Long form description of the package.
        "desc": [],
        // A list of files which are included in the package.
        "files": [],
        // A list of the changes that have been done
        "changelog": [],
    }}

File Permissions
----------------

This extension will set the user and group ownership properties of all files
included with the package. It is enabled by adding 'file_permissions' to the
list of enabled extensions.

.. code-block:: javascript

    {"file_permissions": {
        // The name of the user who should own the files.
        "user": "webserver",
        // The name of the group which should own the files.
        "group": "webserver",
        // If true, the user will be created during install if missing.
        "create_user": false,
        // If true, the group will be created during install if missing.
        "create_group": false,
    }}

Additional Files
----------------

This extension will allow for packaging any files even if they are not a part
of the built project. This extension is enabled by adding "file_extras" in the
list of enabled extensions. This extension also requires that
'file_permissions' be enabled. It uses the same user and group to assign
ownership of the extra files. Source paths are relative to the root.

.. code-block:: javascript

    {"file_extras": {
        "files": [
            {
                "src": "somedir/project_init_script",
                "dest": "etc/init.d/project",
            },
            {
                "src": "somedir/readme",
                "dest": "usr/share/doc/project/readme",
                "doc": true
            },
            {
                "src": "somedir/project.conf",
                "dest": "etc/project.conf",
                // valid options include true, "noreplace", and "missingok"
                "config": "noreplace"
            },
            // source:destination pairs (deprecated)
            "somedir/project_init_script:etc/init.d/project"
        ]
    }}

Python Virtualenv
-----------------

This extension automates generating an RPM from a Python virtualenv. It is
enabled by adding 'python_venv' to the list of enabled extensions.

.. code-block:: javascript

    {"python_venv": {
        // The executable to use for creating a venv.
        "cmd": "virtualenv",
        // Flags to pass to the venv during creation.
        "flags": ["--always-copy"],
        // The name of the installed venv.
        "name": "project_venv",
        // The path in which to install the venv.
        "path": "/usr/share/python",
        // The python executable to use in the venv.
        "python": "python2.7",
        // Optional flag to enable building an rpm with, without a setup.py file. Default is true if not present.
        "require_setup_py": true,
        // Names of requirements files to install in the venv.
        "requirements": ["requirements.txt"],
        // Flags to pass to pip during pip install calls.
        "pip_flags": "--index-url https://internal-pypi-server.org",
        // Optional flag to enable, disable binary striping. Default is true if not present.
        "strip_binaries": true,
        // Optional flag to install the distribution into the venv with
        // pip install, rather than setup.py install. Default is false if
        // not present.
        "use_pip_install": false,
        // Optional flag to remove compiled bytecode from venv.
        // It will reduce size of resulting package. Default is false if not present.
        "remove_pycache": false,
    }}

CLI Flags And Environment Variables
-----------------------------------

In addition to adding the above sections to a configuration file, all values
may also be given as command line flags to the 'rpmvenv' command as well as
environment variables.

Command line flags follow a common pattern: '--extension_name_option_name'. A
common use for this feature is setting the RPM package version over the CLI
rather than hard coding it into a configuration file.

.. code-block:: shell

    rpmvenv /path/to/some/config.json --core_version="$(date -u +%Y.%m.%d.%H.%M.%S)"

This CLI argument pattern may be used to set any options. Alternatively,
environment variables can also be set using a similar naming scheme:
'export RPMVENV_EXTENSION_NAME_OPTION_NAME=""'. Setting the version with
environment variables, for example:

.. code-block:: shell

    RPMVENV_CORE_VERSION="$(date -u +%Y.%m.%d.%H.%M.%S)" \
    rpmvenv /path/to/some/config.json

The precedence order for options is configuration file, environment variables,
then CLI flags. That is, environment variables will always override items in
the configuration file and CLI flags will override both the file and the
environment variables.

Additional Options
------------------

In addition to the options for modifying the spec file, the following are also
available as CLI flags:

-   --source

    The path to a Python source repository. By default, this value resolves to
    the directory containing the specified configuration file. It can be
    overridden if the Python source is not adjacent the configuration file.

-   --destination

    The directory in which to place the RPM. The default value is the current
    working directory.

-   --spec

    This flag disables the actual build in favour of printing the spec file
    contents to stdout. Use this option if you need to manually verify the
    spec file before running a build.

-   --verbose

    Normally, the stdout and stderr of the rpmbuild call are captured unless
    there is an exception. Adding this flag enables the real-time output from
    the rpmbuild command.

NOTE: manylinux
===============

As of 2019-05-26, the issue with packages generated as part of the
`manylinux <https://github.com/pypa/manylinux>`_ project appears to have
been resolved. This means wheels containing universal linux binaries should
work as expected without any special options being enabled for `rpmvenv`.

For background, an issue was opened on 2017-02-01 that reported broken builds
when one of the project dependencies was built using manylinux. The root cause
appeared to be an incompatiblity between manylinux binaries and the standard
`strip` system utility. Without being able to `strip` the binaries we were
unable to remove metadata from those files which included the temporary RPM
build root. RPM builds automatically fail if any file within the package
contains a reference to the build root.

A test has been added to this project's suite that will fail if the manylinux
project issue with `strip` regresses. If the issues does regress you can
restore your builds by adding `strip_binaries=false` to the `venv` section of
your configuration and setting the `QA_SKIP_BUILD_ROOT=1` environment variable
before running `rpmvenv`. The `strip_binaries=false` disables the call to
`strip` and the `QA_SKIP_BUILD_ROOT=1` variable disables the RPM tool's check
for build root.

NOTE: unicode
=============

An issue was opened on 2018-09-01 showing a conflict between some Python
packages and some environments. Notably, CentOS (and possibly others) default
to having a global system encoding value set to `ASCII` rather than `UTF-8`.
Python2.X opens files using the system encoding which results in several errors
if any of the source code files contain non-ASCII characters. If you encounter
this issue then the easiest way to resolve it is to set the
`LC_ALL=en_US.UTF-8` variable before running `rpmvenv`. This will adjust the
global setting and enable processing of non-ASCII encoded files.

NOTE: system python
===================

An issue was opened on 2017-05-18 showing a build failure wnen using the
default Python installations for some versions of CentOS, Fedora, and RedHat.
The issue manifests during the creation of the `virtualenv` and appears as
something like `ImportError: No module named \'time\'` or other error messages
referencing Python built-ins. The cause appears to related to an
`unresolved issue <https://github.com/pypa/virtualenv/issues/565>`_ between the
affected system distribution provided Python installations and `virtualenv`.
The only known fix for this issue is to re-build Python from source for any
affected system.

NOTE: bdist eggs with scripts
=============================

An issue was opened on 2019-01-28 showing a build failure whenever the usual
`python setup.py install` line was executed for a project that both contained
scripts and triggered the `bdist` packaging path for an egg. For unknown
reasons, the `bdist` egg package both installs scripts in the relevant `bin`
directory _and_ retrains a copy within the egg directory. `rpmvenv` rewrites
the shebang paths in `bin` but does not account for the second copy in the
`bdist` egg directory. The result is a build failure because the build root is
referenced in a file.

The way to resolve this issue is to use the `"use_pip_install": true` option
which switches the installation method from `python setup.py install` to
`pip install .`. These two methods result in different installation behavior
because `pip` will always generate a wheel rather than an egg which does not
suffer from this issue.

Testing
=======

The included tests are written using py.test. There is also an included tox.ini
which is configured to run the tests in addition to style checks. By default,
the integration tests run using rpmvenv as the target project to build.
However, any project with a requirements.txt file in the repository root can
be specified with the '--python-git-url' flag while running the tests.

License
=======

::

    (MIT License)

    Copyright (C) 2015 Kevin Conway

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to
    deal in the Software without restriction, including without limitation the
    rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
    sell copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
    IN THE SOFTWARE.


Contributing
============

All contributions to this project are protected under the agreement found in
the `CONTRIBUTING` file. All contributors should read the agreement but, as
a summary::

    You give us the rights to maintain and distribute your code and we promise
    to maintain an open source distribution of anything you contribute.
