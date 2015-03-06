=======
rpmvenv
=======

*RPM packager for Python virtualenv.*

Basic Usage
===========

.. code-block:: shell

    # Point the command to a config file.
    rpmvenv someconfig.json --core_version="1.2.3"

The config file should look like:

.. code-block:: javascript

    {
       "extensions": {
            "enabled": [
                "description_text",
                "python_venv",
                "file_extras",
                "file_permissions"
            ]
        },
       "core": {
            "group": "Application/System",
            "license": "MITE",
            "name": "some-rpm-name",
            "release": "1",
            "source": "/some/path/to/source",
            "summary": "short summary",
        },
       "file_extras": {
            "files": ["src:dest"],
            "group": "vagrant",
            "user": "vagrant"
        },
       "file_permissions": {
            "group": "vagrant",
            "user": "vagrant"
        },
       "python_venv": {
            "cmd": "virtualenv",
            "name": "installed_venv_name",
            "path": "/usr/share/python",
            "python": "python2.7"
        },
        "description_text": {
            "text": "some project description"
        }
    }


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
