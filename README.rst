=======
rpmvenv
=======

*RPM packager for Python virtualenv.*

Basic Usage
===========

.. code-block:: shell

    # Run from inside your package root. Right next to the setup.py
    rpmvenv --version="1.2.3"

    # Or run it against some other package root.
    rpmvenv --version="1.2.3" --source="/home/someuser/projects/coolcode"

The standard process which runs is to create a virtualenv with the default
Python interpreter, install the contents of requirements.txt, install the
targeted package, and wrap it all up in an RPM. If the source package does
not contain a requirements.txt it is silently skipped.

The command line tool allows for some configuration of behaviour:

.. code-block:: shell

    $ rpmvenv --help
    usage: rpmvenv [-h] [--source SOURCE] [--version VERSION] [--python PYTHON]
                   [--venv-option VENV_OPTIONS] [--requirement REQUIREMENTS]
                   [--no-requirements]

    Generate an RPM.

    optional arguments:
      -h, --help            show this help message and exit
      --source SOURCE       The path to your Python source.
      --version VERSION     The version of your Python package.
      --python PYTHON       The Python interpreter to use in the virtualenv.
      --venv-option VENV_OPTIONS
                            Extra flags to pass to virtualenv.
      --requirement REQUIREMENTS
                            Requirements files to install. (relative to source
                            root)
      --no-requirements     Disable installation of requirements.txt files.

Configuration Files
===================

.. code-block:: shell

    # Point to a config file within a Python source repository.
    rpmvenv --version="1.2.3" --source="/path/to/config.yml"

For more in-depth customization of the package contents a configuration file
may be used. Configuration files can be either YAML or JSON encoded. The valid
values are as follows::

    -   name => The package name.

    -   version => The package version.

    -   spec => Mapping of spec values.

        -   description => Long form description of the package.

        -   python => Python interpreter to use in virtualenv.

        -   venv_options => Iterable of virtualenv flags to use.

        -   extra_files => Iterable of two-tuples where the first element
                is the path of the source file relative to the source root
                and the second is the path of the installed file relative
                to the system root.

        -   post => Iterable of post-install commands to run.

        -   postun => Iterable post-uninstall commands to run.

    -   macros => RPM macro definitions.

        -   pkg_name => The name of the directory containing the package
                content.

        -   pkg_rpm_name => The name of the RPM.

        -   pkg_version => The version number to assign the RPM.

        -   pkg_release => The number of times this version has been
                released. The default is 1.

        -   pkg_group => The RPM group in which the package belongs. The
                default is Applications/System.

        -   pkg_summary => A short, one line summary of the package
                contents. The default is a copy of the package name.

        -   pkg_license => The license under which the package code is
                distributed. The default is No License.

        -   pkg_url => A URL to the package source contents. The default is
                a copy of the package name.

        -   pkg_source => A URL or path to the project source code. The
                last element in the path must be the pkg_name value. The
                default value is a copy of the package name.

        -   pkg_install_dir => The path, relative to the root directory, in
                which the package content will be installed on a host. The
                default value is /user/share/python.

        -   pkg_user => The system user to create which will have ownership
                of the installed files. The default is root.

        -   pkg_user_group => The system group to create which will have
                ownership of the installed files. The default is root.

Testing
=======

The included tests will run with the default py.test runner. They require a
command line argument for a remote git package which can be cloned and built.

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
